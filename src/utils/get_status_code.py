from src.schemas import ErrorStatus


def get_status_code(status: ErrorStatus) -> int:
    match status:
        case ErrorStatus.NOT_FOUND:
            return 404
        case ErrorStatus.CONFLICT:
            return 409
        case ErrorStatus.INTERNAL_SERVER_ERROR:
            return 500
