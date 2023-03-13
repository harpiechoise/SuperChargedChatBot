"""Module for context managers."""


class Conversation:
    """Manage the conversation between the agent and the bot.

    Usage:
    ```python
    conversation = Conversation(limit=10, ia_name="Bob")
    conversation.add_human_message("Hello")
    conversation.make_prompt()
    # {context_string}
    # Human: hello
    ```
    """

    def __init__(self, limit: int = 10, ia_name: str = "Bot"):
        """Init the context manager.

        Args:
            limit (int, optional): Context message limit, the number 10 is a
                good ammount for this parameter. Defaults to 10.
            ia_name (str, optional): The name of the chatbot agent, his will
                self identify as his name. Defaults to "Bot".
        """
        # TODO: Replace the hardcode string
        self.history = [f"Vas a responder como si fueras un asistente virtual, tu nombre será Bot y responderas los mensajes bajo en nombre \"Bot\""]
        self.limit = limit

    def add_human_message(self, message):
        """Add human interaction to the context manager.

        Args:
            message (str): User Input
        """
        if len(self.history) >= self.limit:
            self.history = self.history[1:]
        # TODO: Find a formula to add weight to the interaction roles.
        self.history.append(f"Human: {message}")

    def add_ia_message(self, message):
        """Add Artificial Inteligence interaction to the context manager.

        Args:
            message (str): IA text generator model response
        """
        # We discard values
        # TODO: Make a zero shot context importance rating model.
        self.history.append(f"Bot: {message}")

    def make_prompt(self):
        """Yield the current context and interaction onto a prompt.

        Returns:
            str: Current conversation context and chatbot responses.
        """
        return "\n".join(self.history)

    def reset_context(self):
        """Clean the context of the actual conversational context to the
            initial prompt."""
        # TODO: Replace hardcoded string
        self.history = ["Ahora te vas a comportar como un asistente virtual, \
                        responde como si fueras un bot"]
