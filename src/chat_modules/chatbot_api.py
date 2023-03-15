"""All chatbot classes are coded here."""
from src import Conversation
from youdotcom import Chat
from time import sleep
import re
import requests

class BaseChatBotManager:
    """A base class for managing chatbot queries.

    This class provides an interface for creating chatbot managers that can handle different types of queries using context or not.

    :param use_context: A boolean indicating whether to use context or not.
    :type use_context: bool
    :param locales: A list of locales supported by the chatbot manager.
    :type locales: list
    :param limit: An optional integer specifying the maximum number of messages in the conversation history. Defaults to 10.
    :type limit: int
    :param ia_name: An optional string specifying the name of the chatbot. Defaults to "Bot".
    :type ia_name: str
    :param discard_method: An optional string specifying the method to discard old messages from the conversation history. Defaults to None
    :param discard_beams: An optional integer specifying how many beams to discard when using lifo method. Defaults to 1.
    :type discard_beams: int
    """

    def __init__(self, use_context: bool, locales, limit: int = 10, ia_name="Bot", discard_method=None, discard_beams: int = 1):
        if not use_context:
            raise AttributeError("Use context property is required.")
        self.use_context = use_context

        if self.use_context is None:
            self.context = Conversation(limit=limit, ia_name=ia_name, locales=locales, discard_method=discard_method, discard_beams=discard_beams)

    def chatbot_query(self, message):
        """A method to query the chatbot with a given message.

        This method should be implemented by subclasses to handle different types of queries.

        :param message: A string representing the user input.
        :type message: str
        :return: A string representing the chatbot response.
        :rtype: str
        :raises NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("This is a base class")

    def preprocess(self, response):

        raise NotImplementedError("This is a base class")

    def generate(self, message):
        """A method to preprocess the chatbot response before returning it.

        This method should be implemented by subclasses to perform any necessary preprocessing on the response, such as formatting, spelling correction, etc.

        :param response: A string representing the chatbot response.
        :type response: str
        :return: A string representing the preprocessed chatbot response.
        :rtype: str
        :raises NotImplementedError: If the method is not implemented by a subclass.
        """

        #TODO: catch json decode error
        if self.use_context:
            self.context.add_human_message(message)
            curr_message = self.chatbot_query(self.context.make_prompt())
            message = self.preprocess(curr_message)
            self.context.add_ia_message(message)
            return message
        else:
            curr_message = self.chatbot_query(message)
            return curr_message
        
    
    def dynamic_zero_shot_context_value_discard(self, history, num):
        """A method to discard old messages from the conversation history using a zero-shot classification model.

        This method uses a zero-shot classification model to ask the user which messages are relevant for the current query and discards the rest.

        :param history: A list of strings representing the conversation history.
        :type history: list
        :param num: An integer specifying how many messages to keep in the conversation history.
        :type num: int
        :return: A list of strings representing the updated conversation history.
        :rtype: list
        """

        initial_string = self.locales["base_zero_shot_classification"].format(num=num) + "\n"
        for i, value in enumerate(history):
            # Los tabs agregan mas peso a los mensajes para el modelo 
            initial_string += f"\t{i+1}. {value}\n"
        final_string  = initial_string + "\n" + self.locales["tail_zero_shot_clasification"].format(num=num)
        response = self.chatbot_query(final_string)
        response = self.preprocess(response)
        sleep(1)
        indices = [int(i, 10)-1 for i in set(re.findall(r"\d+", response))]
        if len(indices) > num:
            # Use the fallback 
            history = history[num:]
            return history

        for index in indices:
            history.pop(index)
        return history

class BLOOMInferenceAPI(BaseChatBotManager):
    """A subclass of BaseChatBotManager that uses the BLOOM API for text generation.

    This class inherits from BaseChatBotManager and overrides the chatbot_query and preprocess methods to use the BLOOM API for text generation. The BLOOM API is a wrapper for the bigscience/bloom model on Hugging Face.

    :param api_key: A string representing the Hugging Face API key.
    :type api_key: str
    :param locales: A list of locales supported by the chatbot manager.
    :type locales: list
    :param ia_name: An optional string specifying the name of the chatbot. Defaults to "Beto".
    :type ia_name: str
    :param discard_beams: An optional integer specifying how many beams to discard when using lifo method. Defaults to 1.
    :type discard_beams: int
    """

    def __init__(self, api_key, locales, ia_name="Beto", discard_beams=1):
        """Init YouChat text generator model onto a conversational chatbot instance.

        This method initializes the BLOOMInferenceAPI class with the given parameters and calls the BaseChatBotManager constructor.

        :param api_key: A string representing the Hugging Face API key.
        :type api_key: str
        :param locales: A list of locales supported by the chatbot manager.
        :type locales: list
        :param ia_name: An optional string specifying the name of the chatbot. Defaults to "Beto".
        :type ia_name: str
        :param discard_beams: An optional integer specifying how many beams to discard when using lifo method. Defaults to 1.
        :type discard_beams: int
        """
        use_context = True
        self.locales = locales
        self.api_key = api_key
        self.chat = Chat
        BaseChatBotManager.__init__(self, use_context, 
                                    locales=locales, 
                                    ia_name=ia_name,
                                    limit=3,
                                    discard_method=self.dynamic_zero_shot_context_value_discard, 
                                    discard_beams=discard_beams)

        self.api_url = "https://api-inference.huggingface.co/models/bigscience/bloom"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}


    def preprocess(self, response):
        """A method to preprocess the chatbot response before returning it.

        This method overrides the BaseChatBotManager preprocess method and performs some formatting on the response, such as removing the "Bot:" prefix and any extra whitespace.

        :param response: A dictionary representing the chatbot response from the BLOOM API.
        :type response: dict
        :return: A string representing the preprocessed chatbot response.
        :rtype: str
        """
        message = response['message']
        return message.replace("Bot:", "").strip()

    def chatbot_query(self, message):
        """A method to query the chatbot with a given message.

        This method overrides the BaseChatBotManager chatbot_query method and uses the BLOOM API for text generation. It sends a POST request to the BLOOM API URL with the Hugging Face API key and returns the response.

        :param message: A string representing the user input.
        :type message: str
        :return: A dictionary representing the chatbot response from the BLOOM API.
        :rtype: dict
        :raises ConnectionError: If the BLOOM API is not available.
        """
        try:
            response = requests.post(self.api_url, headers=self.headers)
        except requests.JSONDecodeError:
            return {"message": self.locales['api_error_message']}
        if response == "Service Temporarily Unavailable":
            raise ConnectionError("The You Chat API isn't available")
        return response


class YouChat(BaseChatBotManager):
    """A subclass of BaseChatBotManager that uses the YouChat API for text generation.

    This class inherits from BaseChatBotManager and overrides the chatbot_query and preprocess methods to use the YouChat API for text generation. The YouChat API is a service that provides natural language generation models.

    :param api_key: A string representing the YouChat API key.
    :type api_key: str
    :param locales: A list of locales supported by the chatbot manager.
    :type locales: list
    :param ia_name: An optional string specifying the name of the chatbot. Defaults to "Beto".
    :type ia_name: str
    :param discard_beams: An optional integer specifying how many beams to discard when using lifo method. Defaults to 5.
    :type discard_beams: int
    """

    def __init__(self, api_key, locales, ia_name="Beto", discard_beams=5):
        """Init YouChat text generator model onto a conversational chatbot instance.

        This method initializes the YouChat class with the given parameters and calls the BaseChatBotManager constructor.

        :param api_key: A string representing the YouChat API key.
        :type api_key: str
        :param locales: A list of locales supported by the chatbot manager.
        :type locales: list
        :param ia_name: An optional string specifying the name of the chatbot. Defaults to "Beto".
        :type ia_name: str
        :param discard_beams: An optional integer specifying how many beams to discard when using lifo method. Defaults to 5.
        :type discard_beams: int
        """
        use_context = True
        self.locales = locales
        self.api_key = api_key
        self.chat = Chat
        BaseChatBotManager.__init__(self, use_context, 
                                    locales=locales, 
                                    ia_name=ia_name, 
                                    discard_method=self.dynamic_zero_shot_context_value_discard, 
                                    discard_beams=discard_beams)


    def preprocess(self, response):
        """A method to preprocess the chatbot response before returning it.

        This method overrides the BaseChatBotManager preprocess method and performs some formatting on the response, such as removing the "Bot:" prefix and any extra whitespace.

        :param response: A dictionary representing the chatbot response from the YouChat API.
        :type response: dict
        :return: A string representing the preprocessed chatbot response.
        :rtype: str
        """
        message = response['message']
        return message.replace("Bot:", "").strip()

    def chatbot_query(self, message):
        """A method to query the chatbot with a given message.

        This method overrides the BaseChatBotManager chatbot_query method and uses the YouChat API for text generation. It sends a POST request to the YouChat API URL with the YouChat API key and returns the response.

        :param message: A string representing the user input.
        :type message: str
        :return: A dictionary representing the chatbot response from the YouChat API.
        :rtype: dict
        :raises ConnectionError: If the YouChat API is not available.
        """
        try:
            response = self.chat.send_message(message, api_key=self.api_key)
        except requests.JSONDecodeError:
            return {"message": self.locales['api_error_message']}
        if response == "Service Temporarily Unavailable":
            raise ConnectionError("The You Chat API isn't available")
        return response
