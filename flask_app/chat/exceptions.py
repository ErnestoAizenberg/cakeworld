class ChatServiceError(Exception):
    """Base exception for chat service errors."""

    pass


class ValidationError(ChatServiceError):
    """Exception for validation errors."""

    pass


class ChatCreationError(ChatServiceError):
    """Exception for chat creation failures."""

    pass


class ChatUserCreationError(ChatServiceError):
    """Exception for chat user creation failures."""

    pass
