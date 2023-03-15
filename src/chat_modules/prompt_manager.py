# Here we can code a prompt manager
# The prompt manager gives information to the chatbot
# Of this preimplemented toolkits
from src.chat_modules.module_models import ModuleManager
from src.chat_modules.chatbot_api import BaseChatBotManager
from src.i18n.i18n import I18nManager
from time import sleep

class PromptManager:
    def __init__(self, chatbot, locales):
        self.chatbot: BaseChatBotManager = chatbot
        self.module_manager = ModuleManager()
        self.strings = locales

    def chatbot_cli_mainloop(self):
        command = ""
        print(self.strings['welcome_message'])
        while command != "$exit":
            command = input(self.strings['chatbot_input'])
            prompt_head = ("Imagina que eres un programador profesional de chatbots\n"
                           f"Según el input: ({command}), ¿cual de los siguientes se ajustaria"
                            " de mejor manera para resolver el problema?\n")

            task, module_lenght = self.module_manager.return_descriptions()
            prompt_head += task
            prompt_head += "\nEs muy importante que solo escojas una respuesta, ya que solo una respuesta es correcta."
            response = self.chatbot.chatbot_query(prompt_head)

            print("============ PROMPT HEAD =====================")
            print(prompt_head)
            print("============ PROMPT HEAD =====================")
            print()
            print("============  RESPONSE =====================")
            print(response)
            print("============  RESPONSE =====================")

            sleep(2)
            