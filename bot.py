
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Bot token from Botfather
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8719808324:AAFt-vGpbiy9uEku2xSTJ7SbJbLg9QvfpnU")

# Define states for conversation handler
CHOOSING_SERVICE_CATEGORY, CHOOSING_SUB_SERVICE, ENTERING_RECHARGE_CARD, CHOOSING_VC_OPTION, ENTERING_VC_AMOUNT, ENTERING_VC_PHONE = range(6)

# Define services and their interactive flows or USSD codes
SERVICES = {
    "الرصيد والاستهلاك": {
        "الاستعلام عن الرصيد": "*60#",
        "الاستعلام عن الاستهلاك": "*60*0#",
    },
    "شحن الرصيد": {
        "شحن كارت": "RECHARGE_CARD",  # Special key to trigger a conversation flow
    },
    "فودافون كاش": {
        "تحويل أموال": "VC_SEND_MONEY",
        "سحب أموال": "VC_WITHDRAW",
        "الاستعلام عن الرصيد": "*9*13#",
    },
    "باقات الإنترنت": {
        "الاشتراك في باقة جديدة": "*2000#",
        "تجديد الباقة": "*2000*0#",
    },
    "خدمة العملاء": {
        "الاتصال بخدمة العملاء": "888",
        "الدعم الفني": "https://web.vodafone.com.eg/spa/contact-us",
    },
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends a message with inline buttons attached to choose a service category."""
    keyboard = [
        [InlineKeyboardButton(category, callback_data=category)]
        for category in SERVICES.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "أهلاً بك في بوت خدمات فودافون مصر!\nالرجاء اختيار فئة الخدمة:",
        reply_markup=reply_markup,
    )
    return CHOOSING_SERVICE_CATEGORY

async def choose_sub_service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles user choosing a service category and presents sub-services."""
    query = update.callback_query
    await query.answer()

    category = query.data
    context.user_data["chosen_category"] = category

    if category in SERVICES:
        sub_services = SERVICES[category]
        if sub_services:
            keyboard = []
            for sub_service_name, sub_service_action in sub_services.items():
                if isinstance(sub_service_action, str) and sub_service_action.startswith("http"):
                    keyboard.append([InlineKeyboardButton(sub_service_name, url=sub_service_action)])
                else:
                    keyboard.append([InlineKeyboardButton(sub_service_name, callback_data=sub_service_name)])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=f"اختر الخدمة من فئة {category}:", reply_markup=reply_markup)
            return CHOOSING_SUB_SERVICE
        else:
            await query.edit_message_text(text=f"لا توجد خدمات متاحة في فئة {category} حالياً.")
            return ConversationHandler.END
    else:
        await query.edit_message_text(text="فئة غير معروفة.")
        return ConversationHandler.END

async def handle_sub_service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles user choosing a sub-service."""
    query = update.callback_query
    await query.answer()

    sub_service_name = query.data
    category = context.user_data.get("chosen_category")

    if category and sub_service_name in SERVICES[category]:
        action = SERVICES[category][sub_service_name]

        if action == "RECHARGE_CARD":
            await query.edit_message_text("الرجاء إدخال رقم كارت الشحن (14 رقم):")
            return ENTERING_RECHARGE_CARD
        elif action == "VC_SEND_MONEY":
            await query.edit_message_text("الرجاء إدخال المبلغ الذي تود تحويله (فودافون كاش):")
            context.user_data["vc_operation"] = "send"
            return ENTERING_VC_AMOUNT
        elif action == "VC_WITHDRAW":
            await query.edit_message_text("الرجاء إدخال المبلغ الذي تود سحبه (فودافون كاش):")
            context.user_data["vc_operation"] = "withdraw"
            return ENTERING_VC_AMOUNT
        elif action.startswith("*") or action.isdigit(): # USSD code or phone number
            await query.edit_message_text(f"لتنفيذ خدمة '{sub_service_name}'، اطلب الكود التالي:\n`{action}`\n(يمكنك نسخه ولصقه في لوحة الاتصال)")
            return ConversationHandler.END
        else:
            await query.edit_message_text(f"لا يمكن تنفيذ خدمة '{sub_service_name}' حالياً بشكل مباشر. يرجى زيارة الرابط: {action}")
            return ConversationHandler.END
    else:
        await query.edit_message_text("خدمة فرعية غير معروفة.")
        return ConversationHandler.END

async def enter_recharge_card(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the recharge card number input."""
    card_number = update.message.text
    if card_number.isdigit() and len(card_number) == 14:
        await update.message.reply_text(
            f"لشحن رصيدك، اطلب الكود التالي:\n`*858*{card_number}#`\n(يمكنك نسخه ولصقه في لوحة الاتصال)"
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text("رقم الكارت غير صحيح. الرجاء إدخال 14 رقم فقط.")
        return ENTERING_RECHARGE_CARD

async def enter_vc_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles Vodafone Cash amount input."""
    amount = update.message.text
    if amount.isdigit() and int(amount) > 0:
        context.user_data["vc_amount"] = amount
        operation = context.user_data.get("vc_operation")
        if operation == "send":
            await update.message.reply_text("الرجاء إدخال رقم الهاتف الذي تود التحويل إليه:")
            return ENTERING_VC_PHONE
        elif operation == "withdraw":
            await update.message.reply_text(
                f"لسحب مبلغ {amount} جنيه من فودافون كاش، اطلب الكود التالي:\n`*9*2*{amount}#`\n(ثم اتبع التعليمات لإدخال الرقم السري)"
            )
            return ConversationHandler.END
    else:
        await update.message.reply_text("المبلغ غير صحيح. الرجاء إدخال رقم صحيح أكبر من صفر.")
        return ENTERING_VC_AMOUNT

async def enter_vc_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles Vodafone Cash recipient phone number input."""
    phone_number = update.message.text
    amount = context.user_data.get("vc_amount")

    if phone_number.isdigit() and len(phone_number) == 11: # Assuming 11 digit Egyptian phone numbers
        await update.message.reply_text(
            f"لتحويل مبلغ {amount} جنيه إلى {phone_number} عبر فودافون كاش، اطلب الكود التالي:\n`*9*7*{phone_number}*{amount}#`\n(ثم اتبع التعليمات لإدخال الرقم السري)"
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text("رقم الهاتف غير صحيح. الرجاء إدخال 11 رقم فقط.")
        return ENTERING_VC_PHONE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "تم إلغاء العملية.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_SERVICE_CATEGORY: [CallbackQueryHandler(choose_sub_service)],
            CHOOSING_SUB_SERVICE: [
                CallbackQueryHandler(handle_sub_service, pattern="^(?!http).*$") # Exclude URL callbacks
            ],
            ENTERING_RECHARGE_CARD: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_recharge_card)],
            CHOOSING_VC_OPTION: [CallbackQueryHandler(handle_sub_service)],
            ENTERING_VC_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_vc_amount)],
            ENTERING_VC_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_vc_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
