class RawInfoException(Exception):
    def __init__(self, storage_path: str, exc: Exception, *args: object) -> None:
        msg = f"Info extraction from {storage_path} failed. Reason: {str(exc)}"
        super().__init__(msg)


class StoreDataException(Exception):
    def __init__(self, raw_data: dict, exc: Exception, *args: object) -> None:
        msg = f"Storing data {raw_data} failed. Reason: {str(exc)}"
        super().__init__(msg)


class ServiceMessageException(Exception):
    def __init__(self, entity: dict, exc: Exception, *args: object) -> None:
        msg = f"Sending svc msg for entity {entity} failed. Reason: {str(exc)}"
        super().__init__(msg)


class SupervisorMessageException(Exception):
    def __init__(self, entity: dict, exc: Exception, *args: object) -> None:
        msg = f"Sending supervisor msg for entity {entity} failed. Reason: {str(exc)}"
        super().__init__(msg)
