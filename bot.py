
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

# Define the services from digital.gov.eg
SERVICES = {
    "التموين": {
        "تفعيل بطاقة تموين": "https://digital.gov.eg/services/supply/activate-card",
        "إصدار بدل تالف أو فاقد لبطاقة تموين": "https://digital.gov.eg/services/supply/replace-card",
        "نقل من محافظة إلى أخرى": "https://digital.gov.eg/services/supply/transfer-governorate",
        "فصل نفسي": "https://digital.gov.eg/services/supply/separate-self",
        "ضم أفراد أسرتى": "https://digital.gov.eg/services/supply/add-family-members",
        "الاستعلام عن صرف": "https://digital.gov.eg/services/supply/inquire-disbursement",
    },
    "خدمة الاستعلام الائتماني iscore": {
        "الاستعلام عن التقرير الائتماني": "https://digital.gov.eg/services/iscore/credit-report",
    },
    "السكن البديل": {
        "استمارة تقديم على السكن البديل": "https://digital.gov.eg/services/housing/alternative-housing-form",
    },
    "التوثيق": {
        "استعلام عن سريان محرر مُميكن": "https://digital.gov.eg/services/documentation/inquire-document-validity",
        "تحرير توكيل عام في القضايا (عن نفسه)": "https://digital.gov.eg/services/documentation/general-power-of-attorney-self",
        "تحرير إقرار بالشطب (عن نفسه)": "https://digital.gov.eg/services/documentation/cancellation-declaration-self",
        "تحرير إقرار بعدم وجود تعديلات علي البيانات المساحية (عن نفسه)": "https://digital.gov.eg/services/documentation/no-survey-changes-declaration-self",
        "تحرير إقرار رسمي (عن نفسه)": "https://digital.gov.eg/services/documentation/official-declaration-self",
        "تحرير إقرار تصحيح موثق (عن نفسه)": "https://digital.gov.eg/services/documentation/corrected-document-declaration-self",
        "تحرير توكيل عام رسمي (عن نفسه)": "https://digital.gov.eg/services/documentation/general-official-power-of-attorney-self",
        "تحرير توكيل رسمي شامل (بنوك-عام) (عن نفسه)": "https://digital.gov.eg/services/documentation/comprehensive-official-power-of-attorney-self",
        "تحرير توكيل في الأمور الزوجية (عن نفسه)": "https://digital.gov.eg/services/documentation/marital-affairs-power-of-attorney-self",
        "اكتب محررك": "https://digital.gov.eg/services/documentation/write-your-document",
        "حجز ميعاد": "https://digital.gov.eg/services/documentation/book-appointment",
        "معاملاتي المميكنة": "https://digital.gov.eg/services/documentation/my-digitized-transactions",
        "استعلام عن كثافة فروع المكاتب المميكنة": "https://digital.gov.eg/services/documentation/inquire-office-density",
        "تحرير توكيل عام في القضايا (بصفة)": "https://digital.gov.eg/services/documentation/general-power-of-attorney-capacity",
        "تحرير توكيل عام رسمي (بصفة)": "https://digital.gov.eg/services/documentation/general-official-power-of-attorney-capacity",
        "تحرير توكيل رسمي شامل (بنوك-عام) (بصفة)": "https://digital.gov.eg/services/documentation/comprehensive-official-power-of-attorney-capacity",
        "تحرير توكيل في الأمور الزوجية (بصفة)": "https://digital.gov.eg/services/documentation/marital-affairs-power-of-attorney-capacity",
        "تحرير إقرار بالشطب (بصفة)": "https://digital.gov.eg/services/documentation/cancellation-declaration-capacity",
        "تحرير إقرار تصحيح موثق (بصفة)": "https://digital.gov.eg/services/documentation/corrected-document-declaration-capacity",
        "تحرير إقرار بعدم وجود تعديلات علي البيانات المساحية (بصفة)": "https://digital.gov.eg/services/documentation/no-survey-changes-declaration-capacity",
        "تحرير إقرار رسمي (بصفة)": "https://digital.gov.eg/services/documentation/official-declaration-capacity",
        "تحرير عقد بيع مركبة": "https://digital.gov.eg/services/documentation/vehicle-sale-contract",
        "تحرير توكيل بيع مركبة": "https://digital.gov.eg/services/documentation/vehicle-sale-power-of-attorney",
        "تحرير توكيل إدارة مركبة": "https://digital.gov.eg/services/documentation/vehicle-management-power-of-attorney",
        "تحرير عقد بيع دراجة نارية": "https://digital.gov.eg/services/documentation/motorcycle-sale-contract",
        "تحرير توكيل بيع دراجة نارية": "https://digital.gov.eg/services/documentation/motorcycle-sale-power-of-attorney",
        "تحرير توكيل إدارة دراجة نارية": "https://digital.gov.eg/services/documentation/motorcycle-management-power-of-attorney",
    },
    "السجل التجاري": {
        "طلب مستخرج سجل تجاري": "https://digital.gov.eg/services/commercial-register/extract-request",
        "استعلام عن سجل تجاري": "https://digital.gov.eg/services/commercial-register/inquire",
        "طلب تجديد سجل تجاري": "https://digital.gov.eg/services/commercial-register/renewal-request",
        "طلب شهادة بيانات": "https://digital.gov.eg/services/commercial-register/data-certificate-request",
        "تحديث بيانات الشركة": "https://digital.gov.eg/services/commercial-register/update-company-data",
        "إضافة منشأة مسجله (غير مدرجه داخل شركاتى)": "https://digital.gov.eg/services/commercial-register/add-unlisted-establishment",
        "الاستعلام عن المكاتب": "https://digital.gov.eg/services/commercial-register/inquire-offices",
        "حجز ميعاد": "https://digital.gov.eg/services/commercial-register/book-appointment",
        "استدلال عن سجل تجاري": "https://digital.gov.eg/services/commercial-register/deduce-commercial-register",
        "طلب مستخرج سجل تجاري للاعتماد من وزارة الخارجية": "https://digital.gov.eg/services/commercial-register/extract-foreign-ministry-attestation",
        "حجوزاتي": "https://digital.gov.eg/services/commercial-register/my-reservations",
        "طلب موافقة فحص أمني": "https://digital.gov.eg/services/commercial-register/security-check-approval",
        "طلب شهادة سلبية": "https://digital.gov.eg/services/commercial-register/negative-certificate-request",
        "طلب قيد أفراد": "https://digital.gov.eg/services/commercial-register/individual-registration-request",
        "طلب إنشاء فرع لمنشأة فردية": "https://digital.gov.eg/services/commercial-register/create-individual-establishment-branch",
        "طلب إلغاء فرع لمنشأة فردية": "https://digital.gov.eg/services/commercial-register/cancel-individual-establishment-branch",
        "طلب محو منشأة فردية": "https://digital.gov.eg/services/commercial-register/delete-individual-establishment",
        "طلب نقل قيد سجل تجاري داخل المحافظة": "https://digital.gov.eg/services/commercial-register/transfer-registration-within-governorate",
        "طلب المقاصة": "https://digital.gov.eg/services/commercial-register/offsetting-request",
        "طلب تسجيل وكيل مفوض": "https://digital.gov.eg/services/commercial-register/register-authorized-agent",
        "طلب صورة الكترونية من السجل التجاري": "https://digital.gov.eg/services/commercial-register/electronic-copy-request",
        "طلب الحصول علي صورة الكترونية من العقد": "https://digital.gov.eg/services/commercial-register/electronic-contract-copy-request",
        "طلب صورة طبق الأصل من العقود باعتماد الخارجية": "https://digital.gov.eg/services/commercial-register/certified-contract-copy-foreign-ministry",
        "طلب صوره طبق الأصل من العقود بدون اعتماد الخارجية": "https://digital.gov.eg/services/commercial-register/uncertified-contract-copy",
        "الاستعلام عن بيانات شهادة عدم الالتباس": "https://digital.gov.eg/services/commercial-register/inquire-non-confusion-certificate",
        "الغاء حجز اسم تجاري": "https://digital.gov.eg/services/commercial-register/cancel-trade-name-reservation",
        "طلب حجز اسم تجاري (شهادة عدم التباس)": "https://digital.gov.eg/services/commercial-register/reserve-trade-name",
        "طلب مد حجز اسم تجارى": "https://digital.gov.eg/services/commercial-register/extend-trade-name-reservation",
    },
    "التأمين الإجتماعى": {
        "استعلام عن الرقم التأميني": "https://digital.gov.eg/services/social-insurance/inquire-insurance-number",
        "الاستعلام عن أخر مدة تأمينية": "https://digital.gov.eg/services/social-insurance/inquire-last-insurance-period",
        "الاستعلام عن مدد الاشتراك والأجور الخاصة بكل مدة في التأمين الاجتماعي": "https://digital.gov.eg/services/social-insurance/inquire-subscription-periods-wages",
        "الاستعلام عن الإستقطاعات الخاصة بالمؤمن عليه": "https://digital.gov.eg/services/social-insurance/inquire-insured-deductions",
        "استعلام عن البيانات الأساسية لملف المعاش": "https://digital.gov.eg/services/social-insurance/inquire-pension-file-basic-data",
        "الاستعلام عن المعاش المنصرف للقائم بالصرف": "https://digital.gov.eg/services/social-insurance/inquire-disbursed-pension",
        "استعلام عن الإستقطاعات للقائمين بالصرف": "https://digital.gov.eg/services/social-insurance/inquire-disbursement-deductions",
        "استعراض المعاشات المستحقة للمستفيد": "https://digital.gov.eg/services/social-insurance/view-beneficiary-pensions",
        "استعلام عن بيانات السيارة": "https://digital.gov.eg/services/social-insurance/inquire-car-data",
        "الاستعلام عن كشف حساب السيارة": "https://digital.gov.eg/services/social-insurance/inquire-car-account-statement",
        "الاستعلام عن رصيد العاملين بالخارج": "https://digital.gov.eg/services/social-insurance/inquire-overseas-workers-balance",
        "استعلام عن سدادات العاملين بالخارج": "https://digital.gov.eg/services/social-insurance/inquire-overseas-workers-payments",
        "استعلام عن العمليات المستمرة التابعة للمقاول": "https://digital.gov.eg/services/social-insurance/inquire-contractor-ongoing-operations",
    },
    "مركباتى": {
        "تَظلُم على مخالفات رخص مركبات": "https://digital.gov.eg/services/vehicles/appeal-violations",
        "سداد مخالفات رخص المركبات واستخراج شهادة براءة الذمة": "https://digital.gov.eg/services/vehicles/pay-violations-clearance-certificate",
        "تجديد رخصة مركبة": "https://digital.gov.eg/services/vehicles/renew-license",
        "بدل فاقد رخصة مركبة": "https://digital.gov.eg/services/vehicles/lost-license-replacement",
        "بدل تالف رخصة مركبة": "https://digital.gov.eg/services/vehicles/damaged-license-replacement",
        "تحرير عقد بيع مركبة": "https://digital.gov.eg/services/vehicles/vehicle-sale-contract",
        "تحرير توكيل بيع مركبة": "https://digital.gov.eg/services/vehicles/vehicle-sale-power-of-attorney",
        "تحرير توكيل إدارة مركبة": "https://digital.gov.eg/services/vehicles/vehicle-management-power-of-attorney",
        "استعلام عن مخالفات رخصة مركبة": "https://digital.gov.eg/services/vehicles/inquire-violations",
    },
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with inline buttons attached to choose a service category."""
    keyboard = [
        [InlineKeyboardButton(category, callback_data=category)]
        for category in SERVICES.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("أهلاً بك في بوت خدمات مصر الرقمية!\nالرجاء اختيار فئة الخدمة:", reply_markup=reply_markup)

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
