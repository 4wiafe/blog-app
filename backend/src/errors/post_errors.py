class PostError(Exception):
    pass


class PostNotFoundError(PostError):
    pass


class NotPostOwnerError(PostError):
    pass
