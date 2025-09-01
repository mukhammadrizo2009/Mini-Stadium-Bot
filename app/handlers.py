from telegram import Update , ReplyKeyboardMarkup , KeyboardButton
from telegram.ext import CallbackContext
from sqlalchemy.orm import Session

from .database import LocalSession
from .models import User

def start(update: Update ,  context: CallbackContext):
    user_id = update.effective_user.id
    
    update.message.reply_text("Assalomu alaykum !\n\n" \
        "Bu BOT orqali futbol maydonini band qilishingiz mumkin!")
    
    with LocalSession() as session:
        user = session.query(User).filter(User.telegram_id == user_id).first()
        
        if user:
            send_menu(update , context)
        
        else:
            send_register_message(update , context)
        
        
            
def send_menu(update: Update , context: CallbackContext):
    bot = context.bot
    user = update.effective_user
    
    bot.send_message(
        chat_id = user.id,
        text = "Sahifalar ro'yxati",
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("Stadion Buyurtma qilish!")],
                [KeyboardButton("Yordam"), KeyboardButton("Profilm")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    
def send_register_message(update: Update , context: CallbackContext):
    bot = context.bot
    user = update.effective_user
    
    bot.send_message(
        chat_id = user.id,
        text = "Ro'yhatdan o'ting!",
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("Ro'yhatdan o'tish!")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )