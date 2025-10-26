class ApplicationException(Exception):
    pass


class NotFoundException(ApplicationException):
    pass


class ProductNotFoundException(NotFoundException):
    def __init__(self, id: int):
        super().__init__(f"Product with id '{id}' not found")
        self.id = id
