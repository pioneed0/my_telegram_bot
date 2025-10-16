from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import datetime
import asyncio

# 🔹 توکن رباتت رو اینجا وارد کن
TOKEN = "8062630296:AAFB663zNESmwAYHR9s25nBt8nqio52SBfg"

# 🔹 فایل ذخیره‌سازی داده‌ها (اختیاری)
DATA_FILE = "data.txt"

# ------------------------ دستورات ربات ------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 🌞\nمن ربات یادآور مطالعه‌ات هستم.\n"
        "می‌تونی با دستور /add عنوان مطالعه‌ات رو بنویسی."
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("لطفاً عنوان مطالعه‌ات رو هم بنویس. مثال:\n`/add فیزیک فصل ۲`")
        return

    topic = " ".join(context.args)
    now = datetime.datetime.now()
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(f"{topic}|{now}\n")

    await update.message.reply_text(f"✅ موضوع '{topic}' ثبت شد در {now.strftime('%H:%M:%S')}.\n"
                                    f"من در بازه‌های خاص یادآور مرورش می‌شم 🔁")

async def list_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            await update.message.reply_text("📭 هنوز موضوعی ثبت نکردی.")
            return

        msg = "🗒️ لیست موضوعات ثبت‌شده:\n"
        for line in lines:
            topic, time = line.strip().split("|")
            msg += f"• {topic} — {time}\n"

        await update.message.reply_text(msg)
    except FileNotFoundError:
        await update.message.reply_text("هنوز فایلی برای داده‌ها ایجاد نشده 😅")

# ------------------------ بخش راه‌اندازی ------------------------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_topics))

    print("✅ ربات در حال اجراست...")
    app.run_polling(close_loop=False)  # ✅ اصلاح‌شده برای Render

if __name__ == "__main__":
    main()
