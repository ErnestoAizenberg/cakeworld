class TopicNotFoundError(Exception):
    """Raised when a topic is not found"""

    pass


class DuplicateUrlNameError(Exception):
    """Raised when a URL name is already taken"""

    pass
