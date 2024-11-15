import os
import logging
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.constants import ChatMemberStatus
import nest_asyncio
import asyncio

# Imposta il logging per debug
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token del bot
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Utilizza la variabile d'ambiente per maggiore sicurezza

# Percorso della directory delle immagini
IMAGES_DIR = "./Images"

# Messaggio di benvenuto
WELCOME_MESSAGE = "Benvenuti nella community OSS Uniti ™📚 2.0"

# Percorso per il file della cronologia
HISTORY_FILE = "history.txt"

# Funzione per caricare il numero di utenti dal file
def load_user_count():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return int(f.read().strip())
    return 0

# Funzione per salvare il numero di utenti nel file
def save_user_count(count):
    with open(HISTORY_FILE, "w") as f:
        f.write(str(count))

# Funzione di gestione del comando /benvenuti
async def send_welcome(update: Update, context):
    user = update.effective_user
    chat = update.effective_chat

    # Controlla se l'utente è un amministratore
    member = await chat.get_member(user.id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return

    # Cancella il comando /benvenuti
    try:
        await update.message.delete()
    except Exception as e:
        logger.error(f"Errore nella cancellazione del comando: {e}")

    # Invia il messaggio di benvenuto
    await context.bot.send_message(chat_id=chat.id, text=WELCOME_MESSAGE)

    # Invia le immagini
    for image_name in ["Welcome.png", "CanaleTelegram.png", "ChatTelegram.png", "Rules.png"]:
        image_path = os.path.join(IMAGES_DIR, image_name)
        try:
            with open(image_path, "rb") as image_file:
                await context.bot.send_photo(chat_id=chat.id, photo=image_file)
        except FileNotFoundError:
            logger.error(f"Immagine non trovata: {image_path}")

# Funzione per monitorare il numero di membri e inviare il benvenuto automaticamente
async def check_member_count(update: Update, context):
    chat = update.effective_chat

    # Ottieni il numero di membri nella chat
    chat_members = await chat.get_members_count()

    # Se ci sono almeno 50 membri, invia il benvenuto
    if chat_members >= 50:
        # Salva il numero attuale di utenti per evitare che venga inviato più di una volta
        current_count = load_user_count()
        if current_count < chat_members:
    
