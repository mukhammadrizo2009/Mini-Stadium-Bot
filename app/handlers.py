import datetime
from telegram import (Update , ReplyKeyboardMarkup , KeyboardButton, ReplyKeyboardRemove,
        InlineKeyboardMarkup , InlineKeyboardButton   )
from telegram.ext import CallbackContext
from sqlalchemy.orm import Session

from .database import LocalSession
from .models import User
from .config import register_states

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

def ask_name(update: Update , context: CallbackContext):
    update.message.reply_text(
        "Ismingiz...?",
        reply_markup=ReplyKeyboardRemove()
    )
    
    
def set_name(update: Update , context: CallbackContext):
    name = update.message.text.title()
    
    context.user_data['name'] = name
    
    update.message.reply_text(
        "Telefon raqamingizni yuboring!",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("Yuborish", request_contact=True)]
            ],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    
    return register_states.CONTACT

def set_contact(update: Update , context: CallbackContext):
    contact = update.message.contact
    context.user_data['contact'] = contact.phone_number
    
    user_data = context.user_data
    
    text = "Ro'yhatdan o'tish uchun ma'lumotlaringizni tasdiqlang!\n\n" \
        f"Ismingiz: {user_data['name']}\n"\
            f"Telefon raqamingiz: {user_data['contact']}"
            
    update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("Tasdiqlash") , KeyboardButton("Tahrirlash")]
            ],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    
    return register_states.CONFIRM

def save_user(update: Update , context: CallbackContext):
    user_data = context.user_data
    
    with LocalSession() as session:
        user = User(
            telegram_id = update.effective_user.id,
            name = user_data['name'],
            contact = user_data['contact'] 
        )
        session.add(user)
        session.commit()
        
    context.user_data.clear()
    update.message.reply_text(
        "Siz muvaqqiyatli ro'yhatdan o'tdingiz!",
        reply_markup=ReplyKeyboardRemove()
    )
    send_menu(update , context)
    
def send_date(update: Update , context: CallbackContext):
    months = {
        "January": "Yanvar",
        "February": "Fevral",
        "March": "Mart",
        "April": "Aprel",
        "May": "May",
        "June": "Iyun",
        "July": "Iyul",
        "August": "Avgust",
        "September": "Sentyabr",
        "October": "Oktyabr",
        "November": "Noyabr",
        "December": "Dekabr"
    }
    date = datetime.date.today()
    keyboard = [
        [
            InlineKeyboardButton(
                f'📅 {date.day}-{months[date.strftime("%B")]}',
                callback_data=f"date:{date}"
            )
        ]
    ]
    
    for _ in range(6):
        date += datetime.timedelta(days=1)
        keyboard.append(
            [
                InlineKeyboardButton(
                    f'📅 {date.day}-{months[date.strftime("%B")]}',
                    callback_data=f"date: {date}"
                )
            ]
        )
        
        update.message.reply_text(
            "Sanalardan birini tanlang!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )