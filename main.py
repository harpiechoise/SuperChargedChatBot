"""Entry point for ChatBotProject."""
import os
from src import YouChat
from src import initalize_i18n_manager

locales = initalize_i18n_manager()
print(locales['welcome_message'])



#command = ""
#chat = YouChat(api_key=os.environ['CHATAPI'])
# Chat loop
#while command != "$exit":
#    query = input("Persona: ")
#    response = chat.generate(query)
#    print("Bot:", response)
