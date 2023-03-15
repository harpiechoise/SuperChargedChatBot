"""Entry point for ChatBotProject."""
import os
from src import YouChat, LOCALES
from src.chat_modules.prompt_manager import PromptManager

chat = YouChat(os.environ['CHATAPI'], LOCALES, "Flancisco")
promter = PromptManager(chat, LOCALES)

#promter.chatbot_cli_mainloop()