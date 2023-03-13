"""Custom exceptions."""


class APIError(Exception):
    """API error is for raise an unhandled thirdparty exception in the chatbot
        generator.

    Args:
        Exception (Exception): Python base class.
    """

    def __init__(self, message, errors):
        """Init API Error exception.

        Args:
            message (str): Error message.
            errors (Exception.errors): Traceback and error tree messages.
        """
        super().__init__(message)
        self.errors = errors
