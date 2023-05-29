import telegram
import openai_secret_manager
import openai

# Retrieve your Telegram Bot token and OpenAI API key from the secrets manager

secrets = openai_secret_manager.get_secret("telegram_gpt3_bot")
telegram_token = secrets["5967263507:AAEjcSInnT02ysDUIzfsMvzb_vAU5K2tTwU"]
openai_api_key = secrets["skAi9G5krevyMSmL2tIPnmT3BlbkFJfVf3Oyq40Er4NE3lcqDv"]

# Set up the Telegram bot
bot = telegram.Bot(token=telegram_token)

# Set up the OpenAI API client
openai.api_key = openai_api_key


# Define a function to handle incoming messages
def handle_message(update, context):
  message = update.message.text
  response = openai.Completion.create(
    engine="davinci",
    prompt=message,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
  )
  reply_text = response.choices[0].text.strip()
  context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)


# Start the bot and wait for incoming messages
if __name__ == '__main__':
  updater = telegram.ext.Updater(token=telegram_token, use_context=True)
  dispatcher = updater.dispatcher
  dispatcher.add_handler(
    telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
  updater.start_polling()
  updater.idle()
