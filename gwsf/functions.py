"""File which bounds all business logics. It's not hyper generic
please read the docstrings for clarifications about the
implementation."""

# TODO: Refactor Docstrings
# TODO: Refactor usecase example a bit - specially the part with
#   supervisor needs to be clarified
# TODO: for fun: Rewrite in Scala

from dataclasses import dataclass
from datetime import date
from typing import Callable, TypeVar

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


def http_to_storage(
    request: HttpRequest,
    file_name: str,
    read_image_from_request: Callable[[HttpRequest], bytes],
    write_image_to_storage: Callable[[bytes, str], None],
) -> None:
    """A method to extract an image from a request and load it into
    a cloud storage provider.

    Parameters
    ----------
    request
        Incomming request
    read_image_from_request
        Callable which has `request` in it's signature and returns
        image data as bytes
    write_image_to_storage
        Callable which has `image_bytes` and `file_name` in it's signature
        and stores the image into a blob storage
    """
    image = read_image_from_request(request)
    write_image_to_storage(image, file_name)


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
    get_exception: Callable[[dict, Exception], Exception],
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
    extract_message_data: Callable[[Message], CreditApplication],
    store_application_in_database: Callable[[CreditApplication], None],
    send_data_to_service_department: Callable[[CreditApplication], None],
    exception_handler: Callable[[Message, Exception], None],
):
    """A method to extract credit application from a received message
    of a message broker send a credit application to service department.

    Parameters:
    -----------
    message
        Entity which was consumed from a message broker
    extract_message_data
        Callable to parse the message object into a CreditApplication
        object with `message` in it's signature
    store_application_in_database
        Callable to store extracted CreditApplication into a database
        with `credit_application` in it's signature
    send_data_to_service_department
        Callable to send extracted CreditApplication to service
        department with `credit_application` in it's signature
    exception_handler
        Method to handle any kind of upcomming exception with `message`
        and `exc` in it's signature.
    """
    try:
        data = extract_message_data(message)
        store_application_in_database(data)
        send_data_to_service_department(data)
    except Exception as exc:
        exception_handler(message, exc)


def send_application_to_supervisor_if_required(
    message: Message,
    extract_message_data: Callable[[Message], CreditApplication],
    fetch_entities_from_db: Callable[[CreditApplication], list[CreditApplication]],
    send_data_to_supervisor: Callable[[CreditApplication, list[CreditApplication]], None],
    exception_handler: Callable[[Message, Exception], None],
):
    """A method to extract credit application from a received message
    of a message broker send a credit application to a supervisor if the requester has
    already other active credits.

    Parameters:
    -----------
    message
        Entity which was consumed from a message broker
    extract_message_data
        Callable to parse the message object into a CreditApplication
        object with `message` in it's signature
    fetch_entities_from_db
        Callable to fetch approved and currently active credit applciations
        from a database with `credit_application` in it's signature
    send_data_to_supervisor
        Callable to send current credit_application and earlier credit applications
        to a supervisor with `current_credit_application` and
        `previous_credit_applications` in it's signature
    exception_handler
        Method to handle any kind of upcomming exception with `message`
        and `exc` in it's signature.
    """
    try:
        current_credit_application = extract_message_data(message)
        previous_credit_applications = fetch_entities_from_db(current_credit_application)
        if previous_credit_applications:
            send_data_to_supervisor(
                current_credit_application,
                previous_credit_applications,
            )
    except Exception as exc:
        exception_handler(message, exc)
