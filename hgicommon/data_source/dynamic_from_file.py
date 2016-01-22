import logging
import os
from abc import ABCMeta
from collections import defaultdict
from importlib.util import module_from_spec, spec_from_file_location
from multiprocessing import Lock
from typing import Any, Iterable

from hgicommon.data_source.basic import DataSourceType
from hgicommon.data_source.static_from_file import SynchronisedFilesDataSource
from hgicommon.mixable import Listenable
from hgicommon.models import RegistrationEvent

# Map where the key is the type of object the listener is interested is and the value is the listenable that will get
# updates of registration events
registration_event_listenable_map = defaultdict(Listenable)    # type: defaultdict[type, RegistrationEvent]


def register(registerable: Any):
    """
    Registers an object, notifying any listeners that may be interested in it.
    :param registerable: the object to register
    """
    listenable = registration_event_listenable_map[type(registerable)]
    event = RegistrationEvent(registerable, RegistrationEvent.Type.REGISTERED)
    listenable.notify_listeners(event)


def unregister(registerable: Any):
    """
    Unregisters an object, notifying any listeners that may be interested in it.
    :param registerable: the object to unregister
    """
    listenable = registration_event_listenable_map[type(registerable)]
    event = RegistrationEvent(registerable, RegistrationEvent.Type.UNREGISTERED)
    listenable.notify_listeners(event)


# TODO: signature should be:
# class RegisteringDataSource(SynchronisedFilesDataSource[DataSourceType]):
# However, Python's current implementation of generics does not like this (see problem with subclass signature).
class RegisteringDataSource(SynchronisedFilesDataSource):
    """
    Data source where data are defined pragmatically in Python modules. After their definition, data are registered
    using `register`, which this class listens to in order to capture the definitions. The modules are put in a
    directory and are able to be changed on-the-fly.
    """
    __metaclass__ = ABCMeta

    # Global lock to allow multiple instances that source data of the same type to work (i.e. they do not capture
    # definitions loaded by other sources
    _load_locks = defaultdict(Lock)  # type: defaultdict[type, Lock]

    def __init__(self, directory_location: str, data_type: type):
        """
        Constructor.
        :param directory_location: the location of the directory
        :param data_type: the type of data that is loaded from files in the given directory
        """
        super().__init__(directory_location)
        self._data_type = data_type

    def extract_data_from_file(self, file_path: str) -> Iterable[DataSourceType]:
        assert self.is_data_file(file_path)
        logging.info("Loading `%s` from: %s" % (self._data_type, file_path))

        if file_path.rsplit(".")[-1] != "py":
            raise RuntimeError("Can only import uncompiled python modules that have the extension \".py\"")

        loaded = None

        def registration_event_listener(event: RegistrationEvent):
            assert event.event_type == RegistrationEvent.Type.REGISTERED
            nonlocal loaded
            loaded = event.target

        RegisteringDataSource._load_locks[self._data_type].acquire()
        registration_event_listenable_map[self._data_type].add_listener(registration_event_listener)

        try:
            RegisteringDataSource._load_module(file_path)
        finally:
            RegisteringDataSource._load_locks[self._data_type].release()
            registration_event_listenable_map[self._data_type].remove_listener(registration_event_listener)

        if loaded is None:
            raise RuntimeError(
                    "Module \"%s\" failed to register an object of the type `%s`" % (file_path, self._data_type))
        else:
            return [loaded]

    @staticmethod
    def _load_module(path: str):
        """
        Dynamically loads the python module at the given path.
        :param path: the path to load the module from
        """
        spec = spec_from_file_location(os.path.basename(path), path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
