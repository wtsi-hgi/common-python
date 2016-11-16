import socket
from uuid import uuid4


def create_random_string(postfix: str= "", prefix: str="") -> str:
    """
    Creates a random string.
    :param postfix: optional postfix
    :param prefix: optional prefix
    :return: created string
    """
    return "%s%s%s" % (prefix, uuid4(), postfix)


def get_open_port() -> int:
    """
    Gets a PORT that will (probably) be available on the machine.
    It is possible that in-between the time in which the open PORT of found and when it is used, another process may
    bind to it instead.
    :return: the (probably) available PORT
    """
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind(("", 0))
    free_socket.listen(1)
    port = free_socket.getsockname()[1]
    free_socket.close()
    return port
