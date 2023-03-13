"""Module for context managers."""
from typing import Callable

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

    def __init__(self, locales, limit: int = 10, ia_name: str = "Bot", discard_method: Callable = None, discard_beams: int = 5):
        """Init the context manager.

        Args:
            limit (int, optional): Context message limit, the number 10 is a
                good ammount for this parameter. Defaults to 10.
            ia_name (str, optional): The name of the chatbot agent, his will
                self identify as his name. Defaults to "Bot".
        """
        self.discard_beams = discard_beams
        self.locales = locales 
        self.initial_story = self.locales["base_prompt"]["default_assistant_prompt"].format(bot_name=ia_name)
        self.history = [self.initial_story]
        self.limit = limit
        self.discard_method = discard_method

    def add_human_message(self, message):
        """Add human interaction to the context manager.

        Args:
            message (str): User Input
        """
        # Vamos a hacer un experimento
        if len(self.history) >= self.limit:
            
            if not self.discard_method:
                self.history = self.history[1:]
            else:
                print("Ola soy un metodo")
                self.discard_method(self.history, self.discard_beams)
        # TODO: Find a formula to add weight to the interaction roles.
        self.history.append(f"{self.locales['user_input']}: {message}")

    def add_ia_message(self, message):
        """Add Artificial Inteligence interaction to the context manager.

        Args:
            message (str): IA text generator model response
        """
        # We discard values
        # TODO: Make a zero shot context importance rating model.
        self.history.append(f"{self.locales['bot_output']}: {message}")

    def make_prompt(self):
        """Yield the current context and interaction onto a prompt.

        Returns:
            str: Current conversation context and chatbot responses.
        """
        return "\n".join(self.history)

    def reset_context(self):
        """Clean the context of the actual conversational context to the
            initial prompt.
        """
        # TODO: Replace hardcoded string
        self.history = [self.initial_story]
