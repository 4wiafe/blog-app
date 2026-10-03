class UserError(Exception):
    pass


class UserNotFoundError(UserError):
    pass


class UserNameTakenError(UserError):
    pass


class EmailTakenError(UserError):
    pass


class NotUserOwnerError(UserError):
    pass
