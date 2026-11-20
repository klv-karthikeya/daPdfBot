import telebot
import os 
from gemini import pdf_summarize_gemini
from pdf_generator import  generate_pdf
import shutil
bot = telebot.TeleBot(os.environ['TELEGRAM_KEY'])
PDF_FOLDER = "working_dir"
COMPLETE_PATH = None
MODEL = None


## Using this module to handle the operating system functions
def file_operations(operation=None):
    if operation == None: 
        if not os.path.exists(PDF_FOLDER):
            os.makedirs("working_dir")
    elif operation == "clean":
        shutil.rmtree(PDF_FOLDER,ignore_errors=True)
        os.remove("output.pdf")
    else:
        return None
@bot.message_handler(func=lambda message: not message.text.startswith('/'),content_types=['text'])
def pre_login(message):
    bot.send_message(message.chat.id,"Hey use the /auth $username $password")

@bot.message_handler(commands=['auth'],content_types=["text"]) 
def authenticate(message): 
    auth = message.text.split()
    username = auth[1]
    password = auth[2]
    if username == os.environ.get("BOT_USERNAME") and password == os.environ.get("BOT_PASSWORD"):
        bot.send_message(message.chat.id,"Welcome")
        @bot.message_handler(content_types=["document"])
        def save_pdf_files(message):
            file_operations()
            global COMPLETE_PATH
            bot.reply_to(message,"this is a being used as a source")
            file_id = message.document.file_id
            file_info = bot.get_file(file_id)
            file_path = file_info.file_path
            file_name = message.document.file_name  # Get the file name
            downloaded_file = bot.download_file(file_path)
            complete_file_path = os.path.join(PDF_FOLDER, file_name)
            with open(complete_file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
                bot.reply_to(message, f"PDF '{message.document.file_name}' has been saved successfully!")
            COMPLETE_PATH = complete_file_path

        @bot.message_handler(commands=["model"])
        def model_generator(message):
            global MODEL
            arr = message.text.split()
            model = arr[1]
            if model in ["gemini"]:
                bot.reply_to(message,f"selected {arr[1]} as model")
                MODEL = model
            else:
                bot.reply_to(message,"please select a valid model")

        @bot.message_handler(commands=["gen"],content_types = ['text'])
        def process(message):
            if COMPLETE_PATH is not None or MODEL is not None:
                bot.send_message(message.chat.id,"processing") 
            if MODEL == "gemini":
                print("gemini")
                data = pdf_summarize_gemini(COMPLETE_PATH)
                generate_pdf(data,"working_dir")
                with open("output.pdf","rb") as output:
                    bot.send_document(message.chat.id,output)
                file_operations("clean")
            else:
                bot.send_message(message.chat.id,"please enter all parameters")
    else:
        bot.send_message(message.chat.id,"please enter valid creds")



bot.infinity_polling()
