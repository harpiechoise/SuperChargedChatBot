"""Entry point for ChatBotProject."""
import os
from src import YouChat, LOCALES

print(LOCALES['welcome_message'])
command = ""
chat = YouChat(api_key=os.environ['CHATAPI'], locales=LOCALES, ia_name="Flancisco")
# Chat loop
while command != "$exit":
    query = input(LOCALES['user_input'])
    response = chat.generate(query)
    print("Bot:", response)
# ESTOY SUFRIENDO !