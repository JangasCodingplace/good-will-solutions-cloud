"""File which bounds all business logics. It's not hyper generic
please read the docstrings for clarifications about the
implementation."""

# TODO: Refactor Docstrings
# TODO: Refactor usecase example a bit - specially the part with
#   supervisor needs to be clarified
# TODO: for fun: Rewrite in Scala

from dataclasses import dataclass
from datetime import date
from typing import Any, Callable, TypeVar

from . import exceptions

HttpRequest = TypeVar("HttpRequest")
Message = TypeVar("Message")
SendDataReturn = TypeVar("SendDataReturn")


@dataclass
class CreditApplication:
    first_name: str
    last_name: str
    street: str
    city: str
    zip_code: str
    country: str
    application_date: date
    amount: int
    reason: str
    phone: str
    email: str
    timestamp: int


def get_raw_data(
    storage_path: str,
    get: Callable[[str], dict],
    send_data: Callable[[dict], SendDataReturn],
    get_exception: Callable[[str, Exception], exceptions.RawInfoException],
) -> SendDataReturn:
    """A method to extract info from credit application as soon as one
    is stored into a cloud storage provider.

    Parameters
    ----------
    storage_path
        Path to image in cloud storage
    get
        Callable for extracting the image info with `storage_path` in
        it's signature. It should return the raw info as a dictionary
    send_data
        Callable to write data to a message broker with `raw_data` in
        it's signature
    get_exception
        Method get upcomming exception with `storage_path` and `exc`
        in it's signature.
    """
    try:
        raw_data = get(storage_path)
        return send_data(raw_data)
    except Exception as exc:
        raise get_exception(storage_path, exc)


def store_raw_data(
    raw_data: dict,
    parse: Callable[[dict], CreditApplication],
    store: Callable[[CreditApplication], None],
    get_exception: Callable[[dict, Exception], exceptions.StoreDataException],
):
    """A method to parse a raw_data dict to a dataclass and store it
    into a database.

    Parameters
    ----------
    raw_data
        Raw info dictionary containing the credit application info
    parse
        Callable to parse raw data into a data class. It should have
        `raw_data` in it's signature and should return the parsed
        data as CreditApplication
    store
        Callable to store the parsed CreditApplication object into
        a database.
    get_exception
        Method to handle any kind of upcomming exception with
        `raw_data` and `exc` in it's signature.
    """
    try:
        credit_application = parse(raw_data)
        store(credit_application)
    except Exception as exc:
        raise get_exception(raw_data, exc)


def send_application_to_service_department(
    message: Message,
    parse_db_entity: Callable[[Message], CreditApplication],
    get_message: Callable[[CreditApplication], str],
    send_message: Callable[[str], Any],
    get_exception: Callable[[Message, Exception], exceptions.ServiceMessageException],
):
    """A method to extract credit application from a received message
    of a message broker send a credit application to service department.

    Parameters:
    -----------
    message
        Entity which was consumed from a message broker
    parse_db_entity
        Callable to parse the db object into a CreditApplication
        object with `message` in it's signature
    get_message
        Callable to parse a CreditApplication Object into a message
        which will be sent to the service department
    send_message
        Callable to send extracted CreditApplication to service
        department with `message` in it's signature
    get_exception
        Method to handle any kind of upcomming exception with `message`
        and `exc` in it's signature.
    """
    try:
        credit_application = parse_db_entity(message)
        msg = get_message(credit_application)
        return send_message(msg)
    except Exception as exc:
        raise get_exception(message, exc)


def send_application_to_supervisor_if_required(
    message: Message,
    parse_db_entity: Callable[[Message], CreditApplication],
    fetch_from_db: Callable[[CreditApplication], list[CreditApplication]],
    get_message: Callable[[list[CreditApplication]], str],
    send_message: Callable[[str], Any],
    get_exception: Callable[[Message, Exception], exceptions.SupervisorMessageException],
):
    """A method to extract credit application from a received message
    of a message broker send a credit application to a supervisor if the requester has
    already other active credits.

    Parameters:
    -----------
    message
        Entity which was consumed from a message broker
    parse_db_entity
        Callable to parse the message object into a CreditApplication
        object with `message` in it's signature
    fetch_from_db
        Callable to fetch approved and currently active credit applciations
        from a database with `credit_application` in it's signature
    get_message
        Callable to parse a CreditApplication Object into a message
        which will be sent to the supervisor. It should have `all_credit_applications`
        in it's signature
    send_message
        Callable to send extracted CreditApplication to supervisor
        with `message` in it's signature
    get_exception
        Method to handle any kind of upcomming exception with `message`
        and `exc` in it's signature.
    """
    try:
        credit_application = parse_db_entity(message)
        all_credit_applications = fetch_from_db(credit_application)
        if len(all_credit_applications) > 1:
            msg = get_message(all_credit_applications)
            return send_message(msg)
    except Exception as exc:
        raise get_exception(message, exc)
