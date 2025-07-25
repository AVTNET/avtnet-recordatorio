import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from telegram import Bot
from telegram.error import TelegramError
import pytz

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TIMEZONE = pytz.timezone("Europe/Madrid")
scheduler = BlockingScheduler(timezone=TIMEZONE)

bot = Bot(token=TOKEN)
logging.basicConfig(level=logging.INFO)

# Lunes, miércoles y viernes a las 08:45
def send_mw_f_message():
    try:
        bot.send_message(
            chat_id=CHAT_ID,
            text=(
                "Buenos días, recordaros que es de obligado cumplimiento el registro horario "
                "desde la app de iaccesos. La entrada se efectúa al llegar a la primera instalación "
                "y la salida cuando se termine la última instalación."
            )
        )
        logging.info("Mensaje LMX enviado correctamente.")
    except TelegramError as e:
        logging.error(f"Error al enviar mensaje LMX: {e}")

# Viernes a las 17:00 – Recordatorio de stock
def send_stock_reminder():
    try:
        bot.send_message(
            chat_id=CHAT_ID,
            text=(
                "El próximo lunes tenéis que enviar el control de stock de los materiales a través de la aplicación, "
                "tanto de los equipos, acometidas y material fungible. "
                "Llevar un control del material es bueno para todos e importante para poder atender "
                "todas las averías e instalaciones en tiempo y forma, y sobre todo plegar a una hora razonable."
            )
        )
        logging.info("Mensaje de stock enviado correctamente.")
    except TelegramError as e:
        logging.error(f"Error al enviar mensaje de stock: {e}")

# Programar tareas
scheduler.add_job(send_mw_f_message, 'cron', day_of_week='mon,wed,fri', hour=8, minute=45)
scheduler.add_job(send_stock_reminder, 'cron', day_of_week='fri', hour=17, minute=0)

if __name__ == "__main__":
    logging.info("Bot iniciado. Enviando mensaje de prueba...")
    send_stock_reminder()  # Envío inmediato para prueba
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler detenido.")
