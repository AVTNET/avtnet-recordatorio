import os
import logging
import pytz
from datetime import datetime, time
from telegram import Bot
from telegram.error import TelegramError
from apscheduler.schedulers.blocking import BlockingScheduler

# --- CONFIGURACIÓN ---
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")  # Pega aquí el token si no usas variables de entorno
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # ID del grupo donde enviar el mensaje
TIMEZONE = pytz.timezone("Europe/Madrid")
SEND_HOUR = 19
SEND_MINUTE = 10

MESSAGE = (
    "Buenos días, recordaros que es de obligado cumplimiento el registro horario desde la app de iaccesos. "
    "La entrada se efectúa al llegar a la primera instalación y la salida cuando se termine la última instalación."
)

# --- LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
scheduler = BlockingScheduler(timezone=TIMEZONE)

def send_daily_message():
    try:
        bot.send_message(chat_id=CHAT_ID, text=MESSAGE)
        logger.info("Mensaje enviado correctamente.")
    except TelegramError as e:
        logger.error(f"Error al enviar el mensaje: {e}")

scheduler.add_job(send_daily_message, 'cron', hour=SEND_HOUR, minute=SEND_MINUTE)

if __name__ == "__main__":
    logging.info("Bot iniciado. Esperando para enviar mensajes...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler detenido.")

