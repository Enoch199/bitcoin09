"""Bot Telegram pour interagir avec bitcoin09 : Scan, Compte et Transfère."""
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import fp_client

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")
if not TOKEN or not ADMIN_USER_ID:
    raise RuntimeError("TELEGRAM_TOKEN ou ADMIN_USER_ID manquant")
ADMIN_USER_ID = int(ADMIN_USER_ID)

menu_keyboard = [["1️⃣ Scan", "2️⃣ Compte", "3️⃣ Transfère"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Affiche le menu principal du bot."""
    await update.message.reply_text(
        "👋 Bienvenue ! Choisis une option :",
        reply_markup=ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True),
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les messages reçus du bot Telegram."""
    user_id = update.effective_user.id
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("⛔ Accès refusé")
        return

    text = update.message.text.strip()

    if context.user_data.get("awaiting_email"):
        email = text
        context.user_data["email"] = email
        context.user_data["awaiting_email"] = False
        context.user_data["awaiting_amount"] = True
        await update.message.reply_text("💸 Montant à transférer :")
        return

    if context.user_data.get("awaiting_amount"):
        try:
            amount = float(text)
        except ValueError:
            await update.message.reply_text("Montant invalide. Annulé")
            context.user_data.clear()
            return
        email = context.user_data.get("email")
        res = fp_client.transfer(amount, email)
        if res.get("ok"):
            await update.message.reply_text("✅ Transfert réussi\n" + str(res.get("result")))
        else:
            await update.message.reply_text("❌ Erreur : " + str(res.get("error")))
        context.user_data.clear()
        return

    if "Scan" in text or "1️⃣" in text:
        await update.message.reply_text("🔍 Lancement scan...")
        res = fp_client.scan()
        await update.message.reply_text(f"Résultat : found {len(res.get('found', []))}, total {res.get('total')}")
        return

    if "Compte" in text or "2️⃣" in text:
        res = fp_client.get_account()
        if res.get("ok"):
            await update.message.reply_text(f"💰 Solde : {res.get('balance')} {res.get('currency')}")
        else:
            await update.message.reply_text("Erreur compte : " + str(res.get("error")))
        return

    if "Transfère" in text or "3️⃣" in text:
        context.user_data["awaiting_email"] = True
        await update.message.reply_text("✉️ Entre ton email FaucetPay :")
        return

    await update.message.reply_text("Choisis une option du menu")

def main():
    """Démarre le bot Telegram en mode polling."""
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot démarré (production)")
    app.run_polling()

if __name__ == "__main__":
    main()
