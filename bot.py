
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Bot token from Botfather
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8719808324:AAFt-vGpbiy9uEku2xSTJ7SbJbLg9QvfpnU")

# Define the services from web.vodafone.com.eg
SERVICES = {
    "عالم RED الجديد": {
        "اشترك الآن": "https://web.vodafone.com.eg/en/vodafone-red1",
    },
    "باقة فيها كل اللي أنت محتاجه": {
        "اشترك الآن": "https://web.vodafone.com.eg/ar/vodafone-flex",
    },
    "مكالمات الواي فاي": {
        "اعرف اكثر": "https://web.vodafone.com.eg/ar/wifi-calling",
    },
    "إدارة الحساب": {
        "إدارة حسابي": "https://web.vodafone.com.eg/spa/myHome",
    },
    "تسوق": {
        "المتجر الإلكتروني": "https://eshop.vodafone.com.eg/ar/?channelId=organicGoogle&c_id=DACS0367&c_medium=Organic&c_source=Google&c_type=Anonymous",
    },
    "الفروع": {
        "محدد مواقع الفروع": "https://web.vodafone.com.eg/spa/storeLocator",
    },
    "اتصل بنا": {
        "صفحة اتصل بنا": "https://web.vodafone.com.eg/spa/contact-us",
    },
    "خطط أسعار ڤودافون": {
        "أعرف أكتر عن الخطط": "https://web.vodafone.com.eg/ar/home", # Link to home page as no specific plans page found
    },
    "ڤودافون كاش": {
        "أعرف أكتر عن ڤودافون كاش": "https://web.vodafone.com.eg/ar/home", # Link to home page as no specific cash page found
    },
    "DSL ڤودافون": {
        "أعرف أكتر عن DSL": "https://eshop.vodafone.com.eg/ar/internetServices/dsl/dsl-bundles",
    },
    "تطبيق أنا ڤودافون": {
        "حمل التطبيق": "https://web.vodafone.com.eg/ar/home", # Link to home page as no specific app download page found
    },
    "Home Wireless": {
        "أعرف أكتر عن Home Wireless": "https://web.vodafone.com.eg/ar/home", # Link to home page as no specific home wireless page found
    },
    "باقات الانترنت": {
        "اختار باقات اكستريم": "https://web.vodafone.com.eg/ar/home", # Link to home page as no specific internet bundles page found
    },
    "4G": {
        "هل أنت مستعد لشبكة 4G الجديدة؟": "https://eshop.vodafone.com.eg/ar/lines/red/numbers",
    },
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with inline buttons attached to choose a service category."""
    keyboard = [
        [InlineKeyboardButton(category, callback_data=category)]
        for category in SERVICES.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("أهلاً بك في بوت خدمات فودافون مصر!\nالرجاء اختيار فئة الخدمة:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()

    category = query.data
    if category in SERVICES:
        sub_services = SERVICES[category]
        if sub_services:
            keyboard = [
                [InlineKeyboardButton(sub_service_name, url=sub_service_url)]
                for sub_service_name, sub_service_url in sub_services.items()
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=f"اختر الخدمة من فئة {category}:", reply_markup=reply_markup)
        else:
            await query.edit_message_text(text=f"لا توجد خدمات متاحة في فئة {category} حالياً.")
    else:
        await query.edit_message_text(text="فئة غير معروفة.")

def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
