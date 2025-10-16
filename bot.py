from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime, timedelta
import asyncio

# 🔹 توکن ربات خودت رو اینجا بذار
TOKEN = "اینجا_توکن_ربات_تو_قرار_بده"

# حافظه موقتی برای ذخیره یادداشت‌ها
notes = []
user_id = None  # بعداً ذخیره می‌کنیم تا بتونیم پیام بفرستیم

# ✅ دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_id
    user_id = update.message.chat_id
    await update.message.reply_text("سلام پیشرو 👋\nمن ربات یادآور مطالعه‌ات هستم!\nبا دستور /add یه موضوع جدید اضافه کن تا مرورش رو یادآوری کنم.")

# ✅ دستور add
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("مثلاً بنویس:\n`/add فصل ۲ فیزیولوژی`", parse_mode="Markdown")
        return

    title = " ".join(context.args)
    now = datetime.now()
    reminder_times = [now + timedelta(minutes=m) for m in [1, 3, 5, 10]]
    notes.append({"title": title, "times": reminder_times})

    await update.message.reply_text(
        f"✅ موضوع '{title}' ثبت شد.\n⏰ زمان‌های یادآوری در {', '.join([t.strftime('%H:%M:%S') for t in reminder_times])}"
    )

# ✅ بررسی زمان یادآوری‌ها
async def check_reminders(app):
    while True:
        now = datetime.now()
        for note in notes:
            for t in note["times"]:
                if abs((now - t).total_seconds()) < 5:  # اختلاف کمتر از ۵ ثانیه
                    if user_id:
                        await app.bot.send_message(chat_id=user_id, text=f"📚 زمان مرور موضوع: {note['title']}")
                        note["times"].remove(t)
        await asyncio.sleep(5)

# ✅ راه‌اندازی ربات
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))

    asyncio.create_task(check_reminders(app))
    print("✅ ربات در حال اجراست...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())