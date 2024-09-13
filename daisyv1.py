import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import telegram
from datetime import datetime, timedelta

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace 'YOUR_BOT_TOKEN' with the token you got from BotFather
TOKEN = '7322487785:AAFshCuUmVA8-YJNz55pYamOcmr0aeBFq2Y'

# Store user data (you might want to use a database for a production bot)
user_data = {}

# Bot owner details
OWNER_ID = 6008343239
OWNER_USERNAME = "@rundilundlegamera"

def is_owner(user_id: int) -> bool:
    """Check if the user is the bot owner."""
    return user_id == OWNER_ID

def is_admin(update: Update, context: CallbackContext) -> bool:
    """Check if the user is an admin, the bot owner, or if the bot itself is an admin."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    if is_owner(user_id):
        return True
    
    try:
        chat_member = context.bot.get_chat_member(chat_id, user_id)
        return chat_member.status in ['creator', 'administrator']
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return False

def bot_has_admin_rights(context: CallbackContext, chat_id: int) -> bool:
    """Check if the bot has admin rights in the chat."""
    try:
        bot_member = context.bot.get_chat_member(chat_id, context.bot.id)
        return bot_member.status in ['creator', 'administrator']
    except Exception as e:
        logger.error(f"Error checking bot admin status: {e}")
        return False

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
        [InlineKeyboardButton("🔊 Unmute", callback_data='unmute'),
         InlineKeyboardButton("⚠️ Warn", callback_data='warn')],
        [InlineKeyboardButton("🔄 Unwarn", callback_data='unwarn'),
         InlineKeyboardButton("🎖️ Promote", callback_data='promote')],
        [InlineKeyboardButton("⬇️ Demote", callback_data='demote'),
         InlineKeyboardButton("🧹 Purge", callback_data='purge')],
        [InlineKeyboardButton("🔍 Filter", callback_data='filter'),
         InlineKeyboardButton("🛑 Stop Filter", callback_data='stop')],
        [InlineKeyboardButton("📋 Filter List", callback_data='filterlist'),
         InlineKeyboardButton("🌐🚫 Global Ban", callback_data='gban')],
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

def ban(update: Update, context: CallbackContext) -> None:
    """Ban a user."""
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    
    chat_id = update.effective_chat.id
    
    if not bot_has_admin_rights(context, chat_id):
        update.message.reply_text("❌ I don't have admin rights in this chat. I can't ban users.")
        return
    
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        try:
            context.bot.ban_chat_member(chat_id, user_id)
            update.message.reply_text(f"🚫 User {user_id} has been banned.")
        except telegram.error.TelegramError as e:
            update.message.reply_text(f"❌ Failed to ban user: {str(e)}")
    else:
        update.message.reply_text("Please reply to a message to ban the user.")

def unban(update: Update, context: CallbackContext) -> None:
    """Unban a user."""
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    
    chat_id = update.effective_chat.id
    
    if not bot_has_admin_rights(context, chat_id):
        update.message.reply_text("❌ I don't have admin rights in this chat. I can't unban users.")
        return
    
    if context.args:
        user_id = int(context.args[0])
        try:
            context.bot.unban_chat_member(chat_id, user_id)
            update.message.reply_text(f"✅ User {user_id} has been unbanned.")
        except telegram.error.TelegramError as e:
            update.message.reply_text(f"❌ Failed to unban user: {str(e)}")
    else:
        update.message.reply_text("Please provide a user ID to unban.")

def kick(update: Update, context: CallbackContext) -> None:
    """Kick a user."""
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    
    chat_id = update.effective_chat.id
    
    if not bot_has_admin_rights(context, chat_id):
        update.message.reply_text("❌ I don't have admin rights in this chat. I can't kick users.")
        return
    
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        try:
            context.bot.kick_chat_member(chat_id, user_id)
            context.bot.unban_chat_member(chat_id, user_id)
            update.message.reply_text(f"👢 User {user_id} has been kicked.")
        except telegram.error.TelegramError as e:
            update.message.reply_text(f"❌ Failed to kick user: {str(e)}")
    else:
        update.message.reply_text("Please reply to a message to kick the user.")

def mute(update: Update, context: CallbackContext) -> None:
    """Mute a user."""
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    
    chat_id = update.effective_chat.id
    
    if not bot_has_admin_rights(context, chat_id):
        update.message.reply_text("❌ I don't have admin rights in this chat. I can't mute users.")
        return
    
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        try:
            context.bot.restrict_chat_member(
                chat_id, 
                user_id, 
                permissions=ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False
                )
            )
            update.message.reply_text(f"🔇 User {user_id} has been muted.")
        except telegram.error.TelegramError as e:
            update.message.reply_text(f"❌ Failed to mute user: {str(e)}")
    else:
        update.message.reply_text("Please reply to a message to mute the user.")

def unmute(update: Update, context: CallbackContext) -> None:
    """Unmute a user."""
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    
    chat_id = update.effective_chat.id
    
    if not bot_has_admin_rights(context, chat_id):
        update.message.reply_text("❌ I don't have admin rights in this chat. I can't unmute users.")
        return
    
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        try:
            context.bot.restrict_chat_member(
                chat_id, 
                user_id, 
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                )
            )
            update.message.reply_text(f"🔊 User {user_id} has been unmuted.")
        except telegram.error.TelegramError as e:
            update.message.reply_text(f"❌ Failed to unmute user: {str(e)}")
    else:
        update.message.reply_text("Please reply to a message to unmute the user.")

def warn(update: Update, context: CallbackContext) -> None:
    """Warn a user."""
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
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
            except telegram.error.TelegramError as e:
                update.message.reply_text(f"❌ Failed to ban user: {str(e)}")
    else:
        update.message.reply_text("Please reply to a message to warn the user.")

def unwarn(update: Update, context: CallbackContext) -> None:
    """Remove a warning from a user."""
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
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

def promote(update: Update, context: CallbackContext) -> None:
    """Promote a user to admin with an optional custom tag."""
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    
    chat_id = update.effective_chat.id
    
    if not bot_has_admin_rights(context, chat_id):
        update.message.reply_text("❌ I don't have admin rights in this chat. I can't promote users.")
        return
    
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        custom_title = ' '.join(context.args) if context.args else "Admin"
        
        try:
            context.bot.promote_chat_member(chat_id, user_id,
                                            can_change_info=True,
                                            can_delete_messages=True,
                                            can_invite_users=True,
                                            can_restrict_members=True,
                                            can_pin_messages=True,
                                            can_promote_members=False)
            
            context.bot.set_chat_administrator_custom_title(chat_id, user_id, custom_title)
            
            update.message.reply_text(f"🎖️ User {user_id} has been promoted to admin with the title: {custom_title}")
        except telegram.error.TelegramError as e:
            if "Chat_admin_required" in str(e):
                update.message.reply_text("❌ I don't have sufficient rights to promote users in this chat.")
            else:
                update.message.reply_text(f"❌ Failed to promote user: {str(e)}")
    else:
        update.message.reply_text("Please reply to a message to promote the user.")

def demote(update: Update, context: CallbackContext) -> None:
    """Demote an admin to regular user."""
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    
    chat_id = update.effective_chat.id
    
    if not bot_has_admin_rights(context, chat_id):
        update.message.reply_text("❌ I don't have admin rights in this chat. I can't demote users.")
        return
    
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        try:
            context.bot.promote_chat_member(chat_id, user_id,
                                            can_change_info=False,
                                            can_delete_messages=False,
                                            can_invite_users=False,
                                            can_restrict_members=False,
                                            can_pin_messages=False,
                                            can_promote_members=False)
            update.message.reply_text(f"⬇️ User {user_id} has been demoted to regular user.")
        except telegram.error.TelegramError as e:
            update.message.reply_text(f"❌ Failed to demote user: {str(e)}")
    else:
        update.message.reply_text("Please reply to a message to demote the user.")

def purge(update: Update, context: CallbackContext) -> None:
    """Purge a specified number of messages."""
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    
    chat_id = update.effective_chat.id
    if not context.args:
        update.message.reply_text("Please specify the number of messages to purge.")
        return
    
    try:
        num_messages = int(context.args[0])
    except ValueError:
        update.message.reply_text("Please provide a valid number of messages to purge.")
        return
    
    if update.message.reply_to_message:
        message_id = update.message.reply_to_message.message_id
        deleted_count = 0
        
        for i in range(message_id, message_id + num_messages + 1):
            try:
                context.bot.delete_message(chat_id=chat_id, message_id=i)
                deleted_count += 1
            except telegram.error.BadRequest:
                pass
        
        update.message.reply_text(f"🧹 Purged {deleted_count} messages.")
    else:
        update.message.reply_text("Please reply to the message from where you want to start purging.")

def gban(update: Update, context: CallbackContext) -> None:
    """Global ban a user from all chats where the bot is present."""
    if not is_owner(update.effective_user.id):
        update.message.reply_text("🚫 Only the bot owner can use this command.")
        return
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        try:
            # Get all chats where the bot is a member
            chats = context.bot.get_updates()
            chat_ids = set(update.message.chat.id for update in chats if update.message)
            
            for chat_id in chat_ids:
                try:
                    context.bot.ban_chat_member(chat_id, user_id)
                except Exception:
                    continue
            
            update.message.reply_text(f"🌐🚫 User {user_id} has been globally banned from all chats.")
        except Exception as e:
            update.message.reply_text(f"❌ Failed to globally ban user: {str(e)}")
    else:
        update.message.reply_text("Please reply to a message to globally ban the user.")

def announcement(update: Update, context: CallbackContext) -> None:
    """Send an announcement to all chats where the bot is present."""
    if not is_owner(update.effective_user.id):
        update.message.reply_text("🚫 Only the bot owner can use this command.")
        return
    if not context.args:
        update.message.reply_text("Please provide an announcement message.")
        return
    
    announcement_text = ' '.join(context.args)
    chats = context.bot.get_updates()
    chat_ids = set(update.message.chat.id for update in chats if update.message)
    
    for chat_id in chat_ids:
        try:
            context.bot.send_message(chat_id, f"📢 New announcement:\n\n{announcement_text}")
        except Exception:
            continue
    
    update.message.reply_text("Announcement sent to all chats.")

def filter_message(update: Update, context: CallbackContext) -> None:
    """Save a message as a filter."""
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    
    chat_id = update.effective_chat.id
    if update.message.reply_to_message:
        if not context.args:
            update.message.reply_text("Please provide a keyword for the filter.")
            return
        
        keyword = context.args[0].lower()
        message = update.message.reply_to_message
        
        if chat_id not in user_data:
            user_data[chat_id] = {}
        if "filters" not in user_data[chat_id]:
            user_data[chat_id]["filters"] = {}
        
        user_data[chat_id]["filters"][keyword] = {
            "text": message.text,
            "photo": message.photo[-1].file_id if message.photo else None,
            "document": message.document.file_id if message.document else None,
            "sticker": message.sticker.file_id if message.sticker else None,
            "animation": message.animation.file_id if message.animation else None,
            "video": message.video.file_id if message.video else None,
            "voice": message.voice.file_id if message.voice else None,
            "audio": message.audio.file_id if message.audio else None,
        }
        
        update.message.reply_text(f"Filter '{keyword}' has been saved.")
    else:
        update.message.reply_text("Please reply to a message to save it as a filter.")

def stop_filter(update: Update, context: CallbackContext) -> None:
    """Remove a filter."""
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
        update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    
    chat_id = update.effective_chat.id
    if not context.args:
        update.message.reply_text("Please specify the filter keyword to remove.")
        return
    
    keyword = context.args[0].lower()
    
    if chat_id in user_data and "filters" in user_data[chat_id] and keyword in user_data[chat_id]["filters"]:
        del user_data[chat_id]["filters"][keyword]
        update.message.reply_text(f"Filter '{keyword}' has been removed.")
    else:
        update.message.reply_text(f"Filter '{keyword}' does not exist.")

def filter_list(update: Update, context: CallbackContext) -> None:
    """Show all active filters in the chat."""
    chat_id = update.effective_chat.id
    
    if chat_id in user_data and "filters" in user_data[chat_id] and user_data[chat_id]["filters"]:
        filter_list = "Active filters in this chat:\n\n"
        for keyword in user_data[chat_id]["filters"].keys():
            filter_list += f"- {keyword}\n"
        update.message.reply_text(filter_list)
    else:
        update.message.reply_text("There are no active filters in this chat.")

def handle_filters(update: Update, context: CallbackContext) -> None:
    """Check incoming messages for filters and respond accordingly."""
    chat_id = update.effective_chat.id
    message_text = update.message.text.lower() if update.message.text else ""
    
    if chat_id in user_data and "filters" in user_data[chat_id]:
        for keyword, filter_data in user_data[chat_id]["filters"].items():
            if keyword in message_text:
                if filter_data["text"]:
                    update.message.reply_text(filter_data["text"])
                if filter_data["photo"]:
                    update.message.reply_photo(filter_data["photo"])
                if filter_data["document"]:
                    update.message.reply_document(filter_data["document"])
                if filter_data["sticker"]:
                    update.message.reply_sticker(filter_data["sticker"])
                if filter_data["animation"]:
                    update.message.reply_animation(filter_data["animation"])
                if filter_data["video"]:
                    update.message.reply_video(filter_data["video"])
                if filter_data["voice"]:
                    update.message.reply_voice(filter_data["voice"])
                if filter_data["audio"]:
                    update.message.reply_audio(filter_data["audio"])
                break

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
                "/unmute - Unmute a user (admin only)\n" \
                "/warn - Warn a user (admin only)\n" \
                "/unwarn - Remove a warning from a user (admin only)\n" \
                "/promote - Promote a user to admin (admin only)\n" \
                "/demote - Demote an admin to regular user (admin only)\n" \
                "/purge - Delete a specified number of messages (admin only)\n" \
                "/filter - Save a message as a filter (admin only)\n" \
                "/stop - Remove a filter (admin only)\n" \
                "/filterlist - Show all active filters in the chat\n" \
                "/gban - Globally ban a user (bot owner only)\n" \
                "/announcement - Send an announcement to all chats (bot owner only)\n" \
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
"The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
"The best way to predict the future is to create it. - Peter Drucker",
"In the end, we will remember not the words of our enemies, but the silence of our friends. - Martin Luther King Jr.",
"You miss 100% of the shots you don't take. - Wayne Gretzky",
"The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
"Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
"Do not wait to strike till the iron is hot, but make it hot by striking. - William Butler Yeats",
"The journey of a thousand miles begins with one step. - Lao Tzu",
"We are what we repeatedly do. Excellence, then, is not an act, but a habit. - Aristotle",
"The best revenge is massive success. - Frank Sinatra",
"Your time is limited, don't waste it living someone else's life. - Steve Jobs",
"Do what you can, with what you have, where you are. - Theodore Roosevelt",
"To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment. - Ralph Waldo Emerson",
"The purpose of our lives is to be happy. - Dalai Lama",
"To succeed in life, you need two things: ignorance and confidence. - Mark Twain",
"The only impossible journey is the one you never begin. - Tony Robbins",
"Act as if what you do makes a difference. It does. - William James",
"If you tell the truth, you don't have to remember anything. - Mark Twain",
"It does not matter how slowly you go as long as you do not stop. - Confucius",
"Everything you’ve ever wanted is on the other side of fear. - George Addair",
"Opportunities don't happen. You create them. - Chris Grosser",
"Believe you can and you're halfway there. - Theodore Roosevelt",
"To live is the rarest thing in the world. Most people exist, that is all. - Oscar Wilde",
"Your life does not get better by chance, it gets better by change. - Jim Rohn",
"The only way to achieve the impossible is to believe it is possible. - Charles Kingsleigh",
"Everything has beauty, but not everyone can see. - Confucius",
"Success usually comes to those who are too busy to be looking for it. - Henry David Thoreau",
"Don’t watch the clock; do what it does. Keep going. - Sam Levenson",
"Hardships often prepare ordinary people for an extraordinary destiny. - C.S. Lewis",
"Do not go where the path may lead, go instead where there is no path and leave a trail. - Ralph Waldo Emerson",
"Success is not how high you have climbed, but how you make a positive difference to the world. - Roy T. Bennett",
"Challenges are what make life interesting and overcoming them is what makes life meaningful. - Joshua J. Marine",
"Life isn’t about finding yourself. Life is about creating yourself. - George Bernard Shaw",
"Whatever you are, be a good one. - Abraham Lincoln",
"The only person you are destined to become is the person you decide to be. - Ralph Waldo Emerson",
"Start where you are. Use what you have. Do what you can. - Arthur Ashe",
"The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
"Success doesn’t just find you. You have to go out and get it. - Marva Collins",
"Don’t be pushed around by the fears in your mind. Be led by the dreams in your heart. - Roy T. Bennett",
"Everything you can imagine is real. - Pablo Picasso",
"Dream it. Wish it. Do it. - Unknown",
"Success is not in what you have, but who you are. - Bo Bennett",
"Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle. - Christian D. Larson",
"Push yourself, because no one else is going to do it for you. - Unknown",
"Great things never come from comfort zones. - Unknown",
"Dream bigger. Do bigger. - Unknown",
"Don’t stop when you’re tired. Stop when you’re done. - Unknown",
"Wake up with determination. Go to bed with satisfaction. - Unknown",
"Do something today that your future self will thank you for. - Unknown",
"Little things make big days. - Unknown",
"It’s going to be hard, but hard does not mean impossible. - Unknown",
"Don’t wait for opportunity. Create it. - Unknown",
"Success doesn’t just find you. You have to go out and get it. - Unknown",
"Believe in yourself and all that you are. - Unknown"

    ]
    chosen_quote = random.choice(quotes)
    update.message.reply_text(f"📜 {chosen_quote}")

def set_welcome(update: Update, context: CallbackContext) -> None:
    """Set welcome message."""
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
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
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
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
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
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
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
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
    if not is_admin(update, context) and not is_owner(update.effective_user.id):
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
    
    # Check for filters
    handle_filters(update, context)

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
    elif query.data in ['ban', 'unban', 'kick', 'mute', 'unmute', 'warn', 'unwarn', 'promote', 'demote', 'gban', 'purge', 'filter', 'stop', 'filterlist']:
        query.edit_message_text(f"Use /{query.data} command to {query.data} a user or manage filters.")
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
    dispatcher.add_handler(CommandHandler("unmute", unmute))
    dispatcher.add_handler(CommandHandler("warn", warn))
    dispatcher.add_handler(CommandHandler("unwarn", unwarn))
    dispatcher.add_handler(CommandHandler("promote", promote))
    dispatcher.add_handler(CommandHandler("demote", demote))
    dispatcher.add_handler(CommandHandler("gban", gban))
    dispatcher.add_handler(CommandHandler("announcement", announcement))
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
    dispatcher.add_handler(CommandHandler("purge", purge))
    dispatcher.add_handler(CommandHandler("filter", filter_message))
    dispatcher.add_handler(CommandHandler("stop", stop_filter))
    dispatcher.add_handler(CommandHandler("filterlist", filter_list))
    
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