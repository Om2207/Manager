import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import json
from datetime import datetime, timedelta

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace 'YOUR_BOT_TOKEN' with the token you got from BotFather
TOKEN = '6972425077:AAG1-KTOtuR-qVO6siEP1sOnyilWbds8Sy4'

# Store user data (you might want to use a database for a production bot)
user_data = {}

# Bot owner details
OWNER_ID = 6008343239
OWNER_USERNAME = "@rundilundlegamera"

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_message = (
        f"🌼 Welcome to DaisyBot, {user.mention_markdown_v2()}\! 🌼\n\n"
        f"I'm here to help manage your chat and make it bloom with fun and order\. 🌺\n\n"
        f"🔧 Managed by: {OWNER_USERNAME}\n"
        f"🚀 Version: 1\.0\n"
        f"💡 Use /help to see available commands\n\n"
        f"Let's make this chat a beautiful garden together\! 🌻"
    )
    update.message.reply_markdown_v2(welcome_message)
    main_menu(update, context)

def main_menu(update: Update, context: CallbackContext) -> None:
    """Show the main menu."""
    keyboard = [
        [InlineKeyboardButton("👮 Admin Commands", callback_data='admin_commands')],
        [InlineKeyboardButton("👥 User Commands", callback_data='user_commands')],
        [InlineKeyboardButton("🎉 Fun Commands", callback_data='fun_commands')],
        [InlineKeyboardButton("⚙️ Settings", callback_data='settings')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        update.message.reply_text('Please choose a category:', reply_markup=reply_markup)
    else:
        query = update.callback_query
        query.answer()
        query.edit_message_text('Please choose a category:', reply_markup=reply_markup)

def admin_commands(update: Update, context: CallbackContext) -> None:
    """Show admin commands."""
    keyboard = [
        [InlineKeyboardButton("🚫 Ban", callback_data='ban'),
         InlineKeyboardButton("✅ Unban", callback_data='unban')],
        [InlineKeyboardButton("👢 Kick", callback_data='kick'),
         InlineKeyboardButton("🔇 Mute", callback_data='mute')],
        [InlineKeyboardButton("⚠️ Warn", callback_data='warn'),
         InlineKeyboardButton("🔄 Unwarn", callback_data='unwarn')],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text('Admin Commands:', reply_markup=reply_markup)

def user_commands(update: Update, context: CallbackContext) -> None:
    """Show user commands."""
    keyboard = [
        [InlineKeyboardButton("ℹ️ Info", callback_data='info'),
         InlineKeyboardButton("🆔 IDs", callback_data='id')],
        [InlineKeyboardButton("📜 Rules", callback_data='rules'),
         InlineKeyboardButton("❓ Help", callback_data='help')],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text('User Commands:', reply_markup=reply_markup)

def fun_commands(update: Update, context: CallbackContext) -> None:
    """Show fun commands."""
    keyboard = [
        [InlineKeyboardButton("🎲 Roll Dice", callback_data='roll_dice'),
         InlineKeyboardButton("🪙 Flip Coin", callback_data='flip_coin')],
        [InlineKeyboardButton("🔢 Random Number", callback_data='random_number'),
         InlineKeyboardButton("💬 Quote", callback_data='quote')],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text('Fun Commands:', reply_markup=reply_markup)

def settings(update: Update, context: CallbackContext) -> None:
    """Show settings."""
    keyboard = [
        [InlineKeyboardButton("👋 Welcome Message", callback_data='set_welcome'),
         InlineKeyboardButton("👋 Goodbye Message", callback_data='set_goodbye')],
        [InlineKeyboardButton("📜 Chat Rules", callback_data='set_rules'),
         InlineKeyboardButton("🛡️ Anti-Spam", callback_data='set_antispam')],
        [InlineKeyboardButton("🌊 Anti-Flood", callback_data='set_antiflood')],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text('Settings:', reply_markup=reply_markup)

def is_admin(update: Update, context: CallbackContext) -> bool:
    """Check if the user is an admin or the bot owner."""
    user_id = update.effective_user.id
    if user_id == OWNER_ID:
        return True
    chat_id = update.effective_chat.id
    user_status = context.bot.get_chat_member(chat_id, user_id).status
    return user_status in ['creator', 'administrator']

def ban(update: Update, context: CallbackContext) -> None:
    """Ban a user."""
    if not is_admin(update, context):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    if update.message.reply_to_message:
        chat_id = update.effective_chat.id
        user_id = update.message.reply_to_message.from_user.id
        try:
            context.bot.ban_chat_member(chat_id, user_id)
            update.message.reply_text(f"🚫 User {user_id} has been banned.")
        except Exception as e:
            update.message.reply_text(f"❌ Failed to ban user: {str(e)}")
    else:
        update.message.reply_text("Please reply to a message to ban the user.")

def unban(update: Update, context: CallbackContext) -> None:
    """Unban a user."""
    if not is_admin(update, context):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    if context.args:
        chat_id = update.effective_chat.id
        user_id = int(context.args[0])
        try:
            context.bot.unban_chat_member(chat_id, user_id)
            update.message.reply_text(f"✅ User {user_id} has been unbanned.")
        except Exception as e:
            update.message.reply_text(f"❌ Failed to unban user: {str(e)}")
    else:
        update.message.reply_text("Please provide a user ID to unban.")

def kick(update: Update, context: CallbackContext) -> None:
    """Kick a user."""
    if not is_admin(update, context):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    if update.message.reply_to_message:
        chat_id = update.effective_chat.id
        user_id = update.message.reply_to_message.from_user.id
        try:
            context.bot.kick_chat_member(chat_id, user_id)
            context.bot.unban_chat_member(chat_id, user_id)
            update.message.reply_text(f"👢 User {user_id} has been kicked.")
        except Exception as e:
            update.message.reply_text(f"❌ Failed to kick user: {str(e)}")
    else:
        update.message.reply_text("Please reply to a message to kick the user.")

def mute(update: Update, context: CallbackContext) -> None:
    """Mute a user."""
    if not is_admin(update, context):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    if update.message.reply_to_message:
        chat_id = update.effective_chat.id
        user_id = update.message.reply_to_message.from_user.id
        try:
            context.bot.restrict_chat_member(
                chat_id, 
                user_id, 
                permissions=telegram.ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False
                )
            )
            update.message.reply_text(f"🔇 User {user_id} has been muted.")
        except Exception as e:
            update.message.reply_text(f"❌ Failed to mute user: {str(e)}")
    else:
        update.message.reply_text("Please reply to a message to mute the user.")

def warn(update: Update, context: CallbackContext) -> None:
    """Warn a user."""
    if not is_admin(update, context):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    if update.message.reply_to_message:
        warned_user = update.message.reply_to_message.from_user
        user_id = warned_user.id
        chat_id = update.effective_chat.id
        
        if chat_id not in user_data:
            user_data[chat_id] = {}
        if user_id not in user_data[chat_id]:
            user_data[chat_id][user_id] = {"warnings": 0}
        
        user_data[chat_id][user_id]["warnings"] += 1
        warn_count = user_data[chat_id][user_id]["warnings"]
        
        update.message.reply_text(f"⚠️ User {warned_user.mention_markdown_v2()} has been warned\. "
                                  f"Warning count: {warn_count}", parse_mode='MarkdownV2')
        
        if warn_count >= 3:
            try:
                context.bot.kick_chat_member(chat_id, user_id)
                update.message.reply_text(f"🚫 User {warned_user.mention_markdown_v2()} has been banned due to excessive warnings\.", 
                                          parse_mode='MarkdownV2')
            except Exception as e:
                update.message.reply_text(f"❌ Failed to ban user: {str(e)}")
    else:
        update.message.reply_text("Please reply to a message to warn the user.")

def unwarn(update: Update, context: CallbackContext) -> None:
    """Remove a warning from a user."""
    if not is_admin(update, context):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        user_id = user.id
        chat_id = update.effective_chat.id
        
        if chat_id in user_data and user_id in user_data[chat_id]:
            if user_data[chat_id][user_id]["warnings"] > 0:
                user_data[chat_id][user_id]["warnings"] -= 1
                warn_count = user_data[chat_id][user_id]["warnings"]
                update.message.reply_text(f"🔄 One warning has been removed from {user.mention_markdown_v2()}\. "
                                          f"Current warning count: {warn_count}", parse_mode='MarkdownV2')
            else:
                update.message.reply_text(f"{user.mention_markdown_v2()} has no warnings to remove\.", parse_mode='MarkdownV2')
        else:
            update.message.reply_text(f"{user.mention_markdown_v2()} has no warnings\.", parse_mode='MarkdownV2')
    else:
        update.message.reply_text("Please reply to a message to remove a warning from the user.")

def info(update: Update, context: CallbackContext) -> None:
    """Show user and chat information."""
    user = update.effective_user
    chat = update.effective_chat
    
    if chat.type == 'private':
        info_text = f"👤 User Information:\n\n" \
                    f"Name: {user.full_name}\n" \
                    f"Username: @{user.username}\n" \
                    f"User ID: {user.id}\n"
    else:
        member_count = context.bot.get_chat_member_count(chat.id)
        info_text = f"👤 User Information:\n\n" \
                    f"Name: {user.full_name}\n" \
                    f"Username: @{user.username}\n" \
                    f"User ID: {user.id}\n\n" \
                    f"💬 Chat Information:\n\n" \
                    f"Title: {chat.title}\n" \
                    f"Type: {chat.type}\n" \
                    f"Chat ID: {chat.id}\n" \
                    f"Member Count: {member_count}\n"
    
    if chat.id in user_data and user.id in user_data[chat.id]:
        warnings = user_data[chat.id][user.id].get("warnings", 0)
        info_text += f"\nWarnings: {warnings}"
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(info_text, reply_markup=reply_markup)

def id_command(update: Update, context: CallbackContext) -> None:
    """Show user and chat IDs in an easy-to-copy format."""
    user = update.effective_user
    chat = update.effective_chat
    
    id_text = f"User ID: `{user.id}`\n"
    if chat.type != 'private':
        id_text += f"Chat ID: `{chat.id}`"
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(id_text, parse_mode='Markdown', reply_markup=reply_markup)

def rules(update: Update, context: CallbackContext) -> None:
    """Show chat rules."""
    chat_id = update.effective_chat.id
    
    if chat_id in user_data and "rules" in user_data[chat_id]:
        rules_text = f"📜 Chat Rules:\n\n{user_data[chat_id]['rules']}"
    else:
        rules_text = "No rules have been set for this chat."
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(rules_text, reply_markup=reply_markup)

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    help_text = "🌼 DaisyBot Help 🌼\n\n" \
                "Here are some available commands:\n\n" \
                "/start - Start the bot\n" \
                "/help - Show this help message\n" \
                "/info - Show user and chat information\n" \
                "/id - Show user and chat IDs\n" \
                "/rules - Show chat rules\n" \
                "/ban - Ban a user (admin only)\n" \
                "/unban - Unban a user (admin only)\n" \
                "/kick - Kick a user (admin only)\n" \
                "/mute - Mute a user (admin only)\n" \
                "/warn - Warn a user (admin only)\n" \
                "/unwarn - Remove a warning from a user (admin only)\n" \
                "/roll_dice - Roll a dice\n" \
                "/flip_coin - Flip a coin\n" \
                "/random_number - Generate a random number\n" \
                "/quote - Get a random quote\n\n" \
                f"Bot managed by: {OWNER_USERNAME}"
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(help_text, reply_markup=reply_markup)

def roll_dice(update: Update, context: CallbackContext) -> None:
    """Roll a dice."""
    result = random.randint(1, 6)
    update.message.reply_text(f"🎲 You rolled a {result}!")

def flip_coin(update: Update, context: CallbackContext) -> None:
    """Flip a coin."""
    result = random.choice(["Heads", "Tails"])
    update.message.reply_text(f"🪙 The coin landed on: {result}!")

def random_number(update: Update, context: CallbackContext) -> None:
    """Generate a random number between 1 and 100."""
    result = random.randint(1, 100)
    update.message.reply_text(f"🔢 Your random number is: {result}")

def quote(update: Update, context: CallbackContext) -> None:
    """Send a random quote."""
    quotes = [
        "Be the change you wish to see in the world. - Mahatma Gandhi",
        "Stay hungry, stay foolish. - Steve Jobs",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Life is what happens when you're busy making other plans. - John Lennon",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt"
    ]
    chosen_quote = random.choice(quotes)
    update.message.reply_text(f"📜 {chosen_quote}")

def set_welcome(update: Update, context: CallbackContext) -> None:
    """Set welcome message."""
    if not is_admin(update, context):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    chat_id = update.effective_chat.id
    if not context.args:
        update.message.reply_text("Please provide a welcome message.")
        return
    
    welcome_message = ' '.join(context.args)
    if chat_id not in user_data:
        user_data[chat_id] = {}
    user_data[chat_id]["welcome_message"] = welcome_message
    update.message.reply_text("👋 Welcome message has been set.")

def set_goodbye(update: Update, context: CallbackContext) -> None:
    """Set goodbye message."""
    if not is_admin(update, context):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    chat_id = update.effective_chat.id
    if not context.args:
        update.message.reply_text("Please provide a goodbye message.")
        return
    
    goodbye_message = ' '.join(context.args)
    if chat_id not in user_data:
        user_data[chat_id] = {}
    user_data[chat_id]["goodbye_message"] = goodbye_message
    update.message.reply_text("👋 Goodbye message has been set.")

def set_rules(update: Update, context: CallbackContext) -> None:
    """Set chat rules."""
    if not is_admin(update, context):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    chat_id = update.effective_chat.id
    if not context.args:
        update.message.reply_text("Please provide the chat rules.")
        return
    
    rules = ' '.join(context.args)
    if chat_id not in user_data:
        user_data[chat_id] = {}
    user_data[chat_id]["rules"] = rules
    update.message.reply_text("📜 Chat rules have been set.")

def set_antispam(update: Update, context: CallbackContext) -> None:
    """Set anti-spam settings."""
    if not is_admin(update, context):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    chat_id = update.effective_chat.id
    if not context.args or len(context.args) != 2:
        update.message.reply_text("Please provide the number of messages and time frame in seconds.")
        return
    
    try:
        msg_limit = int(context.args[0])
        time_frame = int(context.args[1])
    except ValueError:
        update.message.reply_text("Please provide valid numbers for message limit and time frame.")
        return
    
    if chat_id not in user_data:
        user_data[chat_id] = {}
    user_data[chat_id]["antispam"] = {"msg_limit": msg_limit, "time_frame": time_frame}
    update.message.reply_text(f"🛡️ Anti-spam settings updated. "
                              f"Users sending more than {msg_limit} messages in {time_frame} seconds will be warned.")

def set_antiflood(update: Update, context: CallbackContext) -> None:
    """Set anti-flood settings."""
    if not is_admin(update, context):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    chat_id = update.effective_chat.id
    if not context.args or len(context.args) != 2:
        update.message.reply_text("Please provide the number of messages and time frame in seconds.")
        return
    
    try:
        msg_limit = int(context.args[0])
        time_frame = int(context.args[1])
    except ValueError:
        update.message.reply_text("Please provide valid numbers for message limit and time frame.")
        return
    
    if chat_id not in user_data:
        user_data[chat_id] = {}
    user_data[chat_id]["antiflood"] = {"msg_limit": msg_limit, "time_frame": time_frame}
    update.message.reply_text(f"🌊 Anti-flood settings updated. "
                              f"Users sending more than {msg_limit} messages in {time_frame} seconds will be muted.")

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming messages and check for spam and flood."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    if chat_id in user_data:
        # Anti-spam check
        if "antispam" in user_data[chat_id]:
            antispam = user_data[chat_id]["antispam"]
            check_spam(update, context, antispam["msg_limit"], antispam["time_frame"])
        
        # Anti-flood check
        if "antiflood" in user_data[chat_id]:
            antiflood = user_data[chat_id]["antiflood"]
            check_flood(update, context, antiflood["msg_limit"], antiflood["time_frame"])

def check_spam(update: Update, context: CallbackContext, msg_limit: int, time_frame: int) -> None:
    """Check for spam messages."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    if user_id not in user_data[chat_id]:
        user_data[chat_id][user_id] = {"messages": []}
    
    user_data[chat_id][user_id]["messages"].append(datetime.now())
    
    # Remove messages older than the time frame
    user_data[chat_id][user_id]["messages"] = [
        msg_time for msg_time in user_data[chat_id][user_id]["messages"]
        if (datetime.now() - msg_time).total_seconds() <= time_frame
    ]
    
    if len(user_data[chat_id][user_id]["messages"]) > msg_limit:
        warn(update, context)
        user_data[chat_id][user_id]["messages"] = []  # Reset message count after warning

def check_flood(update: Update, context: CallbackContext, msg_limit: int, time_frame: int) -> None:
    """Check for flood messages."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    if user_id not in user_data[chat_id]:
        user_data[chat_id][user_id] = {"flood_messages": []}
    
    user_data[chat_id][user_id]["flood_messages"].append(datetime.now())
    
    # Remove messages older than the time frame
    user_data[chat_id][user_id]["flood_messages"] = [
        msg_time for msg_time in user_data[chat_id][user_id]["flood_messages"]
        if (datetime.now() - msg_time).total_seconds() <= time_frame
    ]
    
    if len(user_data[chat_id][user_id]["flood_messages"]) > msg_limit:
        mute(update, context)
        user_data[chat_id][user_id]["flood_messages"] = []  # Reset message count after muting

def button(update: Update, context: CallbackContext) -> None:
    """Handle button presses."""
    query = update.callback_query
    query.answer()
    
    if query.data == 'main_menu':
        main_menu(update, context)
    elif query.data == 'admin_commands':
        admin_commands(update, context)
    elif query.data == 'user_commands':
        user_commands(update, context)
    elif query.data == 'fun_commands':
        fun_commands(update, context)
    elif query.data == 'settings':
        settings(update, context)
    elif query.data in ['ban', 'unban', 'kick', 'mute', 'warn', 'unwarn']:
        query.edit_message_text(f"Use /{query.data} command to {query.data} a user.")
    elif query.data == 'info':
        info_text = "Use /info command to get user and chat information."
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='user_commands')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(info_text, reply_markup=reply_markup)
    elif query.data == 'id':
        id_text = "Use /id command to get user and chat IDs in an easy-to-copy format."
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='user_commands')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(id_text, reply_markup=reply_markup)
    elif query.data in ['rules', 'help']:
        query.edit_message_text(f"Use /{query.data} command to get {query.data}.")
    elif query.data in ['roll_dice', 'flip_coin', 'random_number', 'quote']:
        query.edit_message_text(f"Use /{query.data} command to {query.data.replace('_', ' ')}.")
    elif query.data in ['set_welcome', 'set_goodbye', 'set_rules', 'set_antispam', 'set_antiflood']:
        query.edit_message_text(f"Use /{query.data} command to set {query.data.replace('set_', '')}.")

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("ban", ban))
    dispatcher.add_handler(CommandHandler("unban", unban))
    dispatcher.add_handler(CommandHandler("kick", kick))
    dispatcher.add_handler(CommandHandler("mute", mute))
    dispatcher.add_handler(CommandHandler("warn", warn))
    dispatcher.add_handler(CommandHandler("unwarn", unwarn))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("id", id_command))
    dispatcher.add_handler(CommandHandler("rules", rules))
    dispatcher.add_handler(CommandHandler("roll_dice", roll_dice))
    dispatcher.add_handler(CommandHandler("flip_coin", flip_coin))
    dispatcher.add_handler(CommandHandler("random_number", random_number))
    dispatcher.add_handler(CommandHandler("quote", quote))
    dispatcher.add_handler(CommandHandler("set_welcome", set_welcome))
    dispatcher.add_handler(CommandHandler("set_goodbye", set_goodbye))
    dispatcher.add_handler(CommandHandler("set_rules", set_rules))
    dispatcher.add_handler(CommandHandler("set_antispam", set_antispam))
    dispatcher.add_handler(CommandHandler("set_antiflood", set_antiflood))

    # on non command i.e message - check for spam and handle message
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # on button press
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    print(f"🌼 DaisyBot is starting up! Managed by {OWNER_USERNAME}")
    main()
