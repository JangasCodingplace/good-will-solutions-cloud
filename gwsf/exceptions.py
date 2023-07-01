class RawInfoException(Exception):
    def __init__(self, exc: Exception, storage_path: str, *args: object) -> None:
        msg = f"Info extraction from {storage_path} failed. Reason: {str(exc)}"
        super().__init__(msg)
