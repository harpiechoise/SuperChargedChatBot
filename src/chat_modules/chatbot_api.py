"""All chatbot classes are coded here."""
from src import Conversation
from youdotcom import Chat
from time import sleep
import re


class BaseChatBotManager:
    """Base class for Chatbot classes.

    Raises:
        AttributeError: You need to set `use_context` parameter in the class
            initialization.
        NotImplemented: Base classes doesn't allow you to call basemethods.
        NotImplemented: Base classes doesn't allow you to call basemethods.

    Returns:
        _type_: _description_
    """

    def __init__(self, use_context: bool, locales, limit: int = 2, ia_name="Bot", discard_method=None, discard_beams: int = 1):
        """Initialize to create Chatbots from a text generator API or bot.

        Args:
            use_context (bool): If conversation context is required for
                language model this allows you to set
            limit (int, optional): Context lenght limit. Defaults to 10.
            ia_name (str, optional): The name of your chatbot. Defaults to
                "Bot".

        Raises:
            AttributeError: `use_context` parameter is required for this class.
                solution: YouChat(use_context=true)
        """
        if not use_context:
            raise AttributeError("Use context property is required.")
        self.use_context = use_context

        if self.use_context:
            self.context = Conversation(limit=limit, ia_name=ia_name, locales=locales, discard_method=discard_method, discard_beams=discard_beams)

    def chatbot_query(self, message):
        """Make query to chatbot, you send a message and return a chatbot api response.

        Args:
            message (str): User message.

        Raises:
            NotImplemented: You cannot call the method from the base class.
        """
        raise NotImplementedError("This is a base class")

    def preprocess(self, response):
        """Preprocess the chatbot query to transform to the final user response.

        Example:
        ```python

        ...
        def preprocess(self, response):
        return response['message'].replace("Bot:")....
        ```
        Args:
            response (any): Object yielded from the text generation model.

        Raises:
            NotImplemented: Cannot call from base class.
        """
        raise NotImplementedError("This is a base class")

    def generate(self, message):
        """Send message, get response and, and manage context for
            Chatbot if the context is enabled.

        Args:
            message (str): Message  to send to the IA model or API
            ia_name (str, optional): Is the name of your chatbot.  Defaults to
                "Bot:".

        Returns:
            str: Text generator model.
        """
        if self.use_context:
            self.context.add_human_message(message)
            curr_message = self.chatbot_query(self.context.make_prompt())
            message = self.preprocess(curr_message)
            self.context.add_ia_message(message)
            return message
        else:
            curr_message = self.chatbot_query(message)
            return curr_message


class YouChat(BaseChatBotManager):
    """Turns YouChat text generation model onto a conversational ChatBot.

    Args:
        BaseChatBotManager (BaseChatBotManager): Base class for all text
            generation models to make it conversational
    """

    def __init__(self, api_key, locales, ia_name="Beto"):
        """Init YouChat text generator model onto a conversational chatbot instance.

        Args:
            api_key (str): YouChat text generator API Key
        """
        use_context = True
        self.locales = locales
        self.api_key = api_key
        self.chat = Chat
        BaseChatBotManager.__init__(self, use_context, locales=locales, ia_name=ia_name, discard_method=self.dynamic_zero_shot_context_value_discard, discard_beams=1)

    def dynamic_zero_shot_context_value_discard(self, history, num):
        # Esta es la implementación de un algoritmo para rankear
        # Todos los mensajes y saber cualquier excuir sin modificar
        # La idea del zero Shot learning es preguntarle al modelo del lenguaje para 
        # Que resulva la tarea por mi :v 

        # Perfecto!
        # TODO: Terminar el algoritmo
        initial_string = self.locales["base_zero_shot_classification"].format(num=num) + "\n"
        for i, value in enumerate(history):
            # Los tabs agregan mas peso a los mensajes para el modelo 
            initial_string += f"\t{i+1}. {value}\n"
        final_string  = initial_string + "\n" + self.locales["tail_zero_shot_clasification"].format(num=num)
        print(final_string)
        response = self.chat.send_message(final_string, api_key=self.api_key)
        response = self.preprocess(response)
        sleep(0.5)
        return [int(i, 10)-1 for i in set(re.findall(r"\d+", response))]

    def preprocess(self, response):
        """Take a YouChat API response and returns a clean string.

        Args:
            response (any): Response from YouChat text generation API.

        Returns:
            str: A clean message.
        """
        message = response['message']
        return message.replace("Bot:", "").strip()

    def chatbot_query(self, message):
        """Make a query to YouChat text generation API.

        Args:
            message (str): User message to the chatbot
        """
        response = self.chat.send_message(message, api_key=self.api_key)
        if response == "Service Temporarily Unavailable":
            raise ConnectionError("The You Chat API isn't available")
        return response
