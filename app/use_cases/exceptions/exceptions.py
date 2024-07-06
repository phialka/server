
class UseCaseException(Exception):
    '''
    Base exception for use cases
    '''
    def __init__(self, msg: str) -> None:
        super().__init__()
        self.msg: str = msg



class IncorrectValueException(UseCaseException):
    '''
    Raises if any use case gets an incorrect value
    '''
    def __init__(self, msg: str) -> None:
        super().__init__(msg)



class AccessDeniedException(UseCaseException):
    '''
    Raises if access to the use case is denied
    '''
    def __init__(self, msg: str) -> None:
        super().__init__(msg)



class AlreadyExistsException(UseCaseException):
    '''
    Raises if any unique value try duplicated
    '''
    def __init__(self, msg: str) -> None:
        super().__init__(msg)



class NotFoundException(UseCaseException):
    '''
    Raises if any entity is not found
    '''
    def __init__(self, msg: str) -> None:
        super().__init__(msg)



