"""
╔══════════════════════════════════════════════════════════╗
║         🌹 MISS ROSE STYLE TELEGRAM BOT 🌹              ║
║         Sirf BOT TOKEN daalo — Sab Ready Hai!           ║
╠══════════════════════════════════════════════════════════╣
║  INSTALL:  pip install python-telegram-bot==20.7         ║
║  RUN:      python rose_bot.py                            ║
║  OWNER:    @tanmayjain2015                                  ║
╚══════════════════════════════════════════════════════════╝
"""

import logging, re, time
from datetime import datetime, timedelta
from telegram import Update, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)
from telegram.constants import ParseMode

# ╔══════════════════════════════════════════════╗
# ║   🔑 YAHAN APNA BOT TOKEN DAALO             ║
BOT_TOKEN = "8889366370:AAEiMfjQXOVHnir7J25FVe3AYabZ0_jxyTw"
# ╠══════════════════════════════════════════════╣
# ║   👑 OWNER (change mat karna)                ║
OWNER_USERNAME = "tanmayjain2015"
OWNER_ID       = None   # Optional: apna numeric ID daalo
# ╚══════════════════════════════════════════════╝

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ══════════════════════════════════
#  In-Memory Database
# ══════════════════════════════════
notes_db    = {}
filters_db  = {}
warns_db    = {}
rules_db    = {}
welcome_db  = {}
goodbye_db  = {}
locked_db   = {}
afk_db      = {}
flood_db    = {}
linkban_db  = {}
spamban_db  = {}
spam_track  = {}

MAX_WARNS   = 3
FLOOD_LIMIT = 5
SPAM_LIMIT  = 8

LINK_PATTERN = re.compile(
    r"(https?://|www\.|t\.me/|telegram\.me/|bit\.ly/|tinyurl\.com/|"
    r"youtu\.be/|youtube\.com/|instagram\.com/|facebook\.com/|"
    r"twitter\.com/|x\.com/|wa\.me/|whatsapp\.com/)",
    re.IGNORECASE
)

# ════════════════════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════════════════════

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    try:
        m = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return m.status in ["administrator", "creator"]
    except:
        return False

async def get_target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if msg.reply_to_message:
        return msg.reply_to_message.from_user
    if context.args:
        try:
            q = context.args[0]
            return await context.bot.get_chat(q if q.startswith("@") else int(q))
        except:
            pass
    return None

def parse_time(s):
    try:
        n, u = int(s[:-1]), s[-1]
        return {"m": timedelta(minutes=n), "h": timedelta(hours=n), "d": timedelta(days=n)}.get(u)
    except:
        return None

# ════════════════════════════════════════════════════════
#  📌 START / HELP / OWNER
# ════════════════════════════════════════════════════════

HELP_TEXT = """
🌹 *MISS ROSE BOT — ALL COMMANDS*
👑 *Owner:* @tanmayjain2015

👮 *Admin Commands:*
/ban — User ban karo
/unban — Unban karo
/kick — Kick karo
/tban [time] — Temp ban (10m/1h/1d)
/mute — Mute karo
/unmute — Unmute karo
/tmute [time] — Temp mute
/promote — Admin banao
/demote — Admin hatao
/pin — Message pin karo
/unpin — Pin hatao
/unpinall — Sare pin hatao
/purge — Messages delete karo
/del — Ek message delete karo

⚠️ *Warn System:*
/warn — Warn do
/unwarn — Warn hatao
/warns — Warns dekho
/resetwarns — Sare warns reset karo

📝 *Notes:*
/save [name] [text] — Note save karo
/get [name] — Note pao
#notename — Shortcut
/notes — Sare notes
/clear [name] — Note hatao
/clearall — Sare notes hatao

🔍 *Filters:*
/filter [word] [reply] — Filter add
/filters — Sare filters
/stop [word] — Filter hatao
/stopall — Sare filters hatao

📜 *Rules:*
/setrules [text] — Rules set karo
/rules — Rules dekho
/clearrules — Rules hatao

👋 *Welcome/Goodbye:*
/setwelcome [msg] — Welcome set
/welcome — Welcome dekho
/clearwelcome — Welcome hatao
/setgoodbye [msg] — Goodbye set
/goodbye — Goodbye dekho
/cleargoodbye — Goodbye hatao

🔒 *Lock System:*
/lock — Chat lock (messages band)
/unlock — Chat unlock
/lockall — SAB KUCH lock (messages+media+stickers+polls)
/unlockall — SAB KUCH unlock
/locks — Lock status dekho

🔗 *Link Ban:*
/linkban on — Links auto-delete + warn
/linkban off — Link ban hatao
/linkban — Status dekho

🛡️ *Spam Ban:*
/spamban on — Spam karne par auto-mute
/spamban off — Spam ban hatao
/spamban — Status dekho

🌊 *Anti-Flood:*
/setflood [n] — Flood limit set
/flood — Flood setting
/noflood — Flood off karo

😴 *AFK:*
/afk [reason] — AFK mode on
/brb [reason] — Same as AFK

📊 *Info:*
/id — User/Chat ID
/info — User info
/adminlist — Admin list
/chatinfo — Group info
/stats — Bot stats
/owner — Owner ka naam

📢 /report — Admins ko report (reply karke)

🔧 *Utility:*
/ping — Response time
/time — Current time
/calc [math] — Calculator
/echo [text] — Text repeat
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Group mein Add Karo", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("📋 Commands", callback_data="help_main"),
         InlineKeyboardButton("👑 Owner", url=f"https://t.me/{OWNER_USERNAME}")]
    ])
    await update.message.reply_text(
        f"🌹 *Namaste {user.first_name}!*\n\n"
        f"Main ek powerful *Group Management Bot* hoon.\n"
        f"Mujhe group mein add karo aur admin banao!\n\n"
        f"👑 Owner: @{OWNER_USERNAME}\n"
        f"📋 /help — Sari commands dekho",
        parse_mode=ParseMode.MARKDOWN, reply_markup=kb
    )

async def btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "help_main":
        await q.message.reply_text(HELP_TEXT, parse_mode=ParseMode.MARKDOWN)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, parse_mode=ParseMode.MARKDOWN)

async def owner_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👑 *Bot Owner:*\n\n"
        f"📛 Username: @{OWNER_USERNAME}\n"
        f"🔗 Link: [Click Here](https://t.me/{OWNER_USERNAME})\n\n"
        f"_Kisi bhi problem ke liye owner se contact karo!_",
        parse_mode=ParseMode.MARKDOWN
    )

# ════════════════════════════════════════════════════════
#  🚫 BAN / UNBAN / KICK / TBAN
# ════════════════════════════════════════════════════════

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins ban kar sakte hain!")
    t = await get_target(update, context)
    if not t: return await update.message.reply_text("⚠️ Reply karo ya mention karo!")
    reason = " ".join(context.args[1:]) if context.args and len(context.args) > 1 else "Reason nahi diya"
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, t.id)
        await update.message.reply_text(f"🚫 *Banned!*\n👤 [{t.first_name}](tg://user?id={t.id})\n📝 {reason}", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins unban kar sakte hain!")
    t = await get_target(update, context)
    if not t: return await update.message.reply_text("⚠️ Reply karo ya mention karo!")
    try:
        await context.bot.unban_chat_member(update.effective_chat.id, t.id)
        await update.message.reply_text(f"✅ [{t.first_name}](tg://user?id={t.id}) unban ho gaya!", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins kick kar sakte hain!")
    t = await get_target(update, context)
    if not t: return await update.message.reply_text("⚠️ Reply karo ya mention karo!")
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, t.id)
        await context.bot.unban_chat_member(update.effective_chat.id, t.id)
        await update.message.reply_text(f"👢 [{t.first_name}](tg://user?id={t.id}) kick ho gaya!", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def tban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins tban kar sakte hain!")
    t = await get_target(update, context)
    if not t or not context.args: return await update.message.reply_text("⚠️ /tban 10m (reply karke)")
    targ = context.args[0] if not context.args[0].startswith("@") else (context.args[1] if len(context.args)>1 else "")
    delta = parse_time(targ)
    if not delta: return await update.message.reply_text("⚠️ Format: 10m / 2h / 1d")
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, t.id, until_date=datetime.now()+delta)
        await update.message.reply_text(f"⏳ [{t.first_name}](tg://user?id={t.id}) ko {targ} ke liye ban kiya!", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

# ════════════════════════════════════════════════════════
#  🔇 MUTE / UNMUTE / TMUTE
# ════════════════════════════════════════════════════════

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins mute kar sakte hain!")
    t = await get_target(update, context)
    if not t: return await update.message.reply_text("⚠️ Reply karo ya mention karo!")
    try:
        await context.bot.restrict_chat_member(update.effective_chat.id, t.id, ChatPermissions(can_send_messages=False))
        await update.message.reply_text(f"🔇 [{t.first_name}](tg://user?id={t.id}) mute ho gaya!", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins unmute kar sakte hain!")
    t = await get_target(update, context)
    if not t: return await update.message.reply_text("⚠️ Reply karo ya mention karo!")
    try:
        await context.bot.restrict_chat_member(update.effective_chat.id, t.id,
            ChatPermissions(can_send_messages=True, can_send_media_messages=True,
                            can_send_other_messages=True, can_add_web_page_previews=True))
        await update.message.reply_text(f"🔊 [{t.first_name}](tg://user?id={t.id}) unmute ho gaya!", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def tmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins tmute kar sakte hain!")
    t = await get_target(update, context)
    if not t or not context.args: return await update.message.reply_text("⚠️ /tmute 10m (reply karke)")
    targ = context.args[0] if not context.args[0].startswith("@") else (context.args[1] if len(context.args)>1 else "")
    delta = parse_time(targ)
    if not delta: return await update.message.reply_text("⚠️ Format: 10m / 2h / 1d")
    try:
        await context.bot.restrict_chat_member(update.effective_chat.id, t.id,
            ChatPermissions(can_send_messages=False), until_date=datetime.now()+delta)
        await update.message.reply_text(f"🔇 [{t.first_name}](tg://user?id={t.id}) ko {targ} ke liye mute kiya!", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

# ════════════════════════════════════════════════════════
#  ⚠️ WARN SYSTEM
# ════════════════════════════════════════════════════════

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins warn de sakte hain!")
    t = await get_target(update, context)
    if not t: return await update.message.reply_text("⚠️ Reply karo ya mention karo!")
    cid = update.effective_chat.id
    reason = " ".join(context.args[1:]) if context.args and len(context.args)>1 else "Reason nahi diya"
    warns_db.setdefault(cid, {})
    warns_db[cid][t.id] = warns_db[cid].get(t.id, 0) + 1
    cnt = warns_db[cid][t.id]
    if cnt >= MAX_WARNS:
        try:
            await context.bot.ban_chat_member(cid, t.id)
            warns_db[cid][t.id] = 0
            await update.message.reply_text(f"⛔ [{t.first_name}](tg://user?id={t.id}) ko {MAX_WARNS} warns mile — *BAN!*", parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await update.message.reply_text(f"❌ {e}")
    else:
        await update.message.reply_text(
            f"⚠️ *Warn diya!*\n👤 [{t.first_name}](tg://user?id={t.id})\n📝 {reason}\n🔢 {cnt}/{MAX_WARNS}",
            parse_mode=ParseMode.MARKDOWN)

async def unwarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins unwarn kar sakte hain!")
    t = await get_target(update, context)
    if not t: return await update.message.reply_text("⚠️ Reply karo ya mention karo!")
    cid = update.effective_chat.id
    if warns_db.get(cid, {}).get(t.id, 0) > 0:
        warns_db[cid][t.id] -= 1
        await update.message.reply_text(f"✅ Warn hata diya! Ab: {warns_db[cid][t.id]}/{MAX_WARNS}")
    else:
        await update.message.reply_text("ℹ️ Koi warn nahi!")

async def warns_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = await get_target(update, context) or update.effective_user
    cnt = warns_db.get(update.effective_chat.id, {}).get(t.id, 0)
    await update.message.reply_text(f"⚠️ [{t.first_name}](tg://user?id={t.id}): *{cnt}/{MAX_WARNS}* warns", parse_mode=ParseMode.MARKDOWN)

async def resetwarns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins kar sakte hain!")
    t = await get_target(update, context)
    if not t: return await update.message.reply_text("⚠️ Reply karo ya mention karo!")
    warns_db.setdefault(update.effective_chat.id, {})[t.id] = 0
    await update.message.reply_text(f"✅ [{t.first_name}](tg://user?id={t.id}) ke sare warns reset!", parse_mode=ParseMode.MARKDOWN)

# ════════════════════════════════════════════════════════
#  📌 PIN / UNPIN / PURGE / DEL
# ════════════════════════════════════════════════════════

async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins pin kar sakte hain!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Kisi message ko reply karo!")
    try:
        await context.bot.pin_chat_message(update.effective_chat.id, update.message.reply_to_message.message_id)
        await update.message.reply_text("📌 Message pin ho gaya!")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def unpin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins unpin kar sakte hain!")
    try:
        await context.bot.unpin_chat_message(update.effective_chat.id)
        await update.message.reply_text("✅ Pin hata diya!")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def unpinall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins kar sakte hain!")
    try:
        await context.bot.unpin_all_chat_messages(update.effective_chat.id)
        await update.message.reply_text("✅ Sare pins hata diye!")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def purge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins purge kar sakte hain!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Jahan se delete karna ho wahan reply karo!")
    deleted = 0
    for mid in range(update.message.reply_to_message.message_id, update.message.message_id+1):
        try:
            await context.bot.delete_message(update.effective_chat.id, mid)
            deleted += 1
        except: pass
    import asyncio
    m = await update.effective_chat.send_message(f"🗑️ {deleted} messages delete ho gaye!")
    await asyncio.sleep(3)
    try: await m.delete()
    except: pass

async def del_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins delete kar sakte hain!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply karo!")
    try:
        await update.message.reply_to_message.delete()
        await update.message.delete()
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

# ════════════════════════════════════════════════════════
#  👑 PROMOTE / DEMOTE
# ════════════════════════════════════════════════════════

async def promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins promote kar sakte hain!")
    t = await get_target(update, context)
    if not t: return await update.message.reply_text("⚠️ Reply karo ya mention karo!")
    try:
        await context.bot.promote_chat_member(update.effective_chat.id, t.id,
            can_change_info=True, can_delete_messages=True, can_invite_users=True,
            can_restrict_members=True, can_pin_messages=True, can_promote_members=False)
        await update.message.reply_text(f"⭐ [{t.first_name}](tg://user?id={t.id}) admin ban gaya!", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def demote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins demote kar sakte hain!")
    t = await get_target(update, context)
    if not t: return await update.message.reply_text("⚠️ Reply karo ya mention karo!")
    try:
        await context.bot.promote_chat_member(update.effective_chat.id, t.id,
            can_change_info=False, can_delete_messages=False, can_invite_users=False,
            can_restrict_members=False, can_pin_messages=False, can_promote_members=False)
        await update.message.reply_text(f"🔽 [{t.first_name}](tg://user?id={t.id}) demote ho gaya!", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

# ════════════════════════════════════════════════════════
#  📝 NOTES
# ════════════════════════════════════════════════════════

async def save_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins note save kar sakte hain!")
    if len(context.args) < 2: return await update.message.reply_text("⚠️ /save [name] [text]")
    cid = update.effective_chat.id
    notes_db.setdefault(cid, {})[context.args[0].lower()] = " ".join(context.args[1:])
    await update.message.reply_text(f"✅ Note *{context.args[0]}* save ho gaya!", parse_mode=ParseMode.MARKDOWN)

async def get_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ /get [name]")
    name = context.args[0].lower()
    note = notes_db.get(update.effective_chat.id, {}).get(name)
    if note: await update.message.reply_text(f"📝 *{name}*\n\n{note}", parse_mode=ParseMode.MARKDOWN)
    else: await update.message.reply_text(f"❌ '{name}' note nahi mila!")

async def list_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    notes = notes_db.get(update.effective_chat.id, {})
    if not notes: return await update.message.reply_text("📭 Koi note nahi!")
    await update.message.reply_text("📝 *Sare Notes:*\n\n" + "\n".join([f"• `#{k}`" for k in notes]), parse_mode=ParseMode.MARKDOWN)

async def clear_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins note delete kar sakte hain!")
    if not context.args: return await update.message.reply_text("⚠️ /clear [name]")
    cid = update.effective_chat.id
    name = context.args[0].lower()
    if name in notes_db.get(cid, {}):
        del notes_db[cid][name]
        await update.message.reply_text(f"🗑️ Note *{name}* delete ho gaya!", parse_mode=ParseMode.MARKDOWN)
    else: await update.message.reply_text(f"❌ '{name}' note nahi mila!")

async def clearall_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins kar sakte hain!")
    notes_db[update.effective_chat.id] = {}
    await update.message.reply_text("🗑️ Sare notes delete ho gaye!")

async def hashtag_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text: return
    cid = update.effective_chat.id
    for word in msg.text.split():
        if word.startswith("#") and len(word) > 1:
            note = notes_db.get(cid, {}).get(word[1:].lower())
            if note:
                await msg.reply_text(f"📝 *{word[1:]}*\n\n{note}", parse_mode=ParseMode.MARKDOWN)

# ════════════════════════════════════════════════════════
#  🔍 FILTERS
# ════════════════════════════════════════════════════════

async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins filter add kar sakte hain!")
    if len(context.args) < 2: return await update.message.reply_text("⚠️ /filter [word] [reply]")
    cid = update.effective_chat.id
    filters_db.setdefault(cid, {})[context.args[0].lower()] = " ".join(context.args[1:])
    await update.message.reply_text(f"✅ Filter *{context.args[0]}* add ho gaya!", parse_mode=ParseMode.MARKDOWN)

async def list_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    f = filters_db.get(update.effective_chat.id, {})
    if not f: return await update.message.reply_text("📭 Koi filter nahi!")
    await update.message.reply_text("🔍 *Sare Filters:*\n\n" + "\n".join([f"• `{k}`" for k in f]), parse_mode=ParseMode.MARKDOWN)

async def stop_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins filter hatao!")
    if not context.args: return await update.message.reply_text("⚠️ /stop [word]")
    cid = update.effective_chat.id
    kw = context.args[0].lower()
    if kw in filters_db.get(cid, {}):
        del filters_db[cid][kw]
        await update.message.reply_text(f"✅ Filter *{kw}* hata diya!", parse_mode=ParseMode.MARKDOWN)
    else: await update.message.reply_text(f"❌ '{kw}' filter nahi mila!")

async def stopall_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins kar sakte hain!")
    filters_db[update.effective_chat.id] = {}
    await update.message.reply_text("🗑️ Sare filters hata diye!")

async def check_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text: return
    txt = msg.text.lower()
    for kw, reply in filters_db.get(update.effective_chat.id, {}).items():
        if kw in txt:
            await msg.reply_text(reply)
            break

# ════════════════════════════════════════════════════════
#  📜 RULES
# ════════════════════════════════════════════════════════

async def setrules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins rules set kar sakte hain!")
    if not context.args: return await update.message.reply_text("⚠️ /setrules [text]")
    rules_db[update.effective_chat.id] = " ".join(context.args)
    await update.message.reply_text("✅ Rules set ho gaye!")

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = rules_db.get(update.effective_chat.id)
    if r: await update.message.reply_text(f"📜 *Group Rules:*\n\n{r}", parse_mode=ParseMode.MARKDOWN)
    else: await update.message.reply_text("❌ Koi rules set nahi hue!")

async def clearrules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins kar sakte hain!")
    rules_db.pop(update.effective_chat.id, None)
    await update.message.reply_text("✅ Rules hata diye!")

# ════════════════════════════════════════════════════════
#  👋 WELCOME / GOODBYE
# ════════════════════════════════════════════════════════

async def setwelcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins kar sakte hain!")
    if not context.args: return await update.message.reply_text("⚠️ /setwelcome [msg]\nVariables: {name} {chat}")
    welcome_db[update.effective_chat.id] = " ".join(context.args)
    await update.message.reply_text("✅ Welcome set ho gaya!")

async def show_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    w = welcome_db.get(update.effective_chat.id, "Default: 🌹 Welcome to *{chat}*, [{name}]!")
    await update.message.reply_text(f"👋 *Welcome:*\n\n{w}", parse_mode=ParseMode.MARKDOWN)

async def clearwelcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins kar sakte hain!")
    welcome_db.pop(update.effective_chat.id, None)
    await update.message.reply_text("✅ Welcome hata diya!")

async def setgoodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins kar sakte hain!")
    if not context.args: return await update.message.reply_text("⚠️ /setgoodbye [msg]")
    goodbye_db[update.effective_chat.id] = " ".join(context.args)
    await update.message.reply_text("✅ Goodbye set ho gaya!")

async def show_goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    g = goodbye_db.get(update.effective_chat.id, "Default: 👋 Goodbye {name}!")
    await update.message.reply_text(f"👋 *Goodbye:*\n\n{g}", parse_mode=ParseMode.MARKDOWN)

async def cleargoodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins kar sakte hain!")
    goodbye_db.pop(update.effective_chat.id, None)
    await update.message.reply_text("✅ Goodbye hata diya!")

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    for member in update.message.new_chat_members:
        if member.is_bot: continue
        w = welcome_db.get(cid, "🌹 Welcome to *{chat}*, [{name}](tg://user?id={id})!")
        await update.message.reply_text(
            w.replace("{name}", member.first_name)
             .replace("{chat}", update.effective_chat.title or "group")
             .replace("{id}", str(member.id)),
            parse_mode=ParseMode.MARKDOWN)

async def left_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    m = update.message.left_chat_member
    if m and not m.is_bot:
        g = goodbye_db.get(cid, "👋 [{name}](tg://user?id={id}) ne group chod diya!")
        await update.message.reply_text(g.replace("{name}", m.first_name).replace("{id}", str(m.id)), parse_mode=ParseMode.MARKDOWN)

# ════════════════════════════════════════════════════════
#  🔒 LOCK / UNLOCK / LOCKALL / UNLOCKALL
# ════════════════════════════════════════════════════════

async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins lock kar sakte hain!")
    cid = update.effective_chat.id
    locked_db[cid] = True
    try:
        await context.bot.set_chat_permissions(cid, ChatPermissions(can_send_messages=False))
        await update.message.reply_text("🔒 *Chat lock ho gaya!*\nSirf admins bol sakte hain.", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins unlock kar sakte hain!")
    cid = update.effective_chat.id
    locked_db[cid] = False
    try:
        await context.bot.set_chat_permissions(cid, ChatPermissions(
            can_send_messages=True, can_send_media_messages=True,
            can_send_other_messages=True, can_add_web_page_previews=True, can_send_polls=True))
        await update.message.reply_text("🔓 *Chat unlock ho gaya!*\nSab bol sakte hain.", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def lockall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins lockall kar sakte hain!")
    cid = update.effective_chat.id
    locked_db[cid] = True
    try:
        await context.bot.set_chat_permissions(cid, ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_send_polls=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
        ))
        await update.message.reply_text(
            "🔒🔒 *LOCKALL — Sab kuch lock!*\n\n"
            "❌ Messages — Band\n"
            "❌ Media / Photos / Videos — Band\n"
            "❌ Stickers / GIFs — Band\n"
            "❌ Polls — Band\n"
            "❌ Links — Band\n"
            "❌ Invite — Band\n\n"
            "✅ Sirf admins active hain.\n"
            "Unlock: /unlockall",
            parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def unlockall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins unlockall kar sakte hain!")
    cid = update.effective_chat.id
    locked_db[cid] = False
    try:
        await context.bot.set_chat_permissions(cid, ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_send_polls=True,
            can_change_info=False,
            can_invite_users=True,
            can_pin_messages=False,
        ))
        await update.message.reply_text(
            "🔓✅ *UNLOCKALL — Sab kuch unlock!*\n\n"
            "✅ Messages — On\n"
            "✅ Media / Photos / Videos — On\n"
            "✅ Stickers / GIFs — On\n"
            "✅ Polls — On\n"
            "✅ Invite — On\n\n"
            "Ab sab normal hai!",
            parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def locks_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    await update.message.reply_text(
        f"🔒 *Lock Status:*\n\n"
        f"Chat Lock: *{'🔒 ON' if locked_db.get(cid) else '🔓 OFF'}*\n"
        f"Link Ban: *{'✅ ON' if linkban_db.get(cid) else '❌ OFF'}*\n"
        f"Spam Ban: *{'✅ ON' if spamban_db.get(cid) else '❌ OFF'}*",
        parse_mode=ParseMode.MARKDOWN)

# ════════════════════════════════════════════════════════
#  🔗 LINK BAN
# ════════════════════════════════════════════════════════

async def linkban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    if not context.args:
        status = "✅ ON" if linkban_db.get(cid) else "❌ OFF"
        return await update.message.reply_text(
            f"🔗 *Link Ban:* {status}\n\n`/linkban on` — On karo\n`/linkban off` — Off karo",
            parse_mode=ParseMode.MARKDOWN)
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins kar sakte hain!")
    arg = context.args[0].lower()
    if arg == "on":
        linkban_db[cid] = True
        await update.message.reply_text(
            "🔗✅ *Link Ban ON!*\n\n"
            "Koi bhi link bhejega to:\n"
            "• Link auto-delete hoga\n"
            "• Warn milega\n"
            f"• {MAX_WARNS} warns = Ban!",
            parse_mode=ParseMode.MARKDOWN)
    elif arg == "off":
        linkban_db[cid] = False
        await update.message.reply_text("🔗❌ *Link Ban OFF ho gaya!*", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("⚠️ Use: /linkban on ya /linkban off")

async def check_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text: return
    cid = update.effective_chat.id
    if not linkban_db.get(cid): return
    user = update.effective_user
    if not user or await is_admin(update, context, user.id): return
    if LINK_PATTERN.search(msg.text):
        try: await msg.delete()
        except: pass
        warns_db.setdefault(cid, {})
        warns_db[cid][user.id] = warns_db[cid].get(user.id, 0) + 1
        cnt = warns_db[cid][user.id]
        if cnt >= MAX_WARNS:
            try:
                await context.bot.ban_chat_member(cid, user.id)
                warns_db[cid][user.id] = 0
                await context.bot.send_message(cid,
                    f"🚫 [{user.first_name}](tg://user?id={user.id}) link bhejta raha — *BAN!*",
                    parse_mode=ParseMode.MARKDOWN)
            except: pass
        else:
            try:
                await context.bot.send_message(cid,
                    f"🔗❌ [{user.first_name}](tg://user?id={user.id}) *Link mana hai!*\n⚠️ Warn: {cnt}/{MAX_WARNS}",
                    parse_mode=ParseMode.MARKDOWN)
            except: pass

# ════════════════════════════════════════════════════════
#  🛡️ SPAM BAN
# ════════════════════════════════════════════════════════

async def spamban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    if not context.args:
        status = "✅ ON" if spamban_db.get(cid) else "❌ OFF"
        return await update.message.reply_text(
            f"🛡️ *Spam Ban:* {status}\n\n`/spamban on` — On karo\n`/spamban off` — Off karo",
            parse_mode=ParseMode.MARKDOWN)
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins kar sakte hain!")
    arg = context.args[0].lower()
    if arg == "on":
        spamban_db[cid] = True
        await update.message.reply_text(
            f"🛡️✅ *Spam Ban ON!*\n\n{SPAM_LIMIT}+ messages 5 second mein = 10 min mute!",
            parse_mode=ParseMode.MARKDOWN)
    elif arg == "off":
        spamban_db[cid] = False
        await update.message.reply_text("🛡️❌ *Spam Ban OFF ho gaya!*", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("⚠️ Use: /spamban on ya /spamban off")

async def check_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    user = update.effective_user
    cid = update.effective_chat.id
    if not user or not spamban_db.get(cid): return
    if await is_admin(update, context, user.id): return
    now = time.time()
    spam_track.setdefault(cid, {}).setdefault(user.id, [])
    spam_track[cid][user.id] = [t for t in spam_track[cid][user.id] if now - t < 5]
    spam_track[cid][user.id].append(now)
    if len(spam_track[cid][user.id]) >= SPAM_LIMIT:
        spam_track[cid][user.id] = []
        try:
            await context.bot.restrict_chat_member(cid, user.id,
                ChatPermissions(can_send_messages=False),
                until_date=datetime.now() + timedelta(minutes=10))
            await context.bot.send_message(cid,
                f"🛡️ [{user.first_name}](tg://user?id={user.id}) *Spam detect hua!* 10 min mute.",
                parse_mode=ParseMode.MARKDOWN)
        except: pass

# ════════════════════════════════════════════════════════
#  🌊 FLOOD
# ════════════════════════════════════════════════════════

async def setflood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins kar sakte hain!")
    if not context.args or not context.args[0].isdigit():
        return await update.message.reply_text("⚠️ /setflood [number]")
    flood_db.setdefault(update.effective_chat.id, {})["limit"] = int(context.args[0])
    await update.message.reply_text(f"✅ Flood limit {context.args[0]} set ho gaya!")

async def flood_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limit = flood_db.get(update.effective_chat.id, {}).get("limit", FLOOD_LIMIT)
    await update.message.reply_text(f"🌊 Flood limit: *{limit}* msg/5sec", parse_mode=ParseMode.MARKDOWN)

async def noflood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins kar sakte hain!")
    flood_db.setdefault(update.effective_chat.id, {})["limit"] = 0
    await update.message.reply_text("✅ Flood protection off ho gaya!")

async def check_flood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    cid = update.effective_chat.id
    if not user or await is_admin(update, context, user.id): return
    limit = flood_db.get(cid, {}).get("limit", FLOOD_LIMIT)
    if limit == 0: return
    now = time.time()
    flood_db.setdefault(cid, {}).setdefault(user.id, [])
    flood_db[cid][user.id] = [t for t in flood_db[cid].get(user.id, []) if now - t < 5]
    flood_db[cid][user.id].append(now)
    if len(flood_db[cid][user.id]) >= limit:
        flood_db[cid][user.id] = []
        try:
            await context.bot.restrict_chat_member(cid, user.id, ChatPermissions(can_send_messages=False))
            await update.effective_message.reply_text(
                f"🌊 [{user.first_name}](tg://user?id={user.id}) flood — *Mute!*", parse_mode=ParseMode.MARKDOWN)
        except: pass

# ════════════════════════════════════════════════════════
#  😴 AFK
# ════════════════════════════════════════════════════════

async def afk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    reason = " ".join(context.args) if context.args else "Koi reason nahi"
    afk_db[user.id] = reason
    await update.message.reply_text(f"😴 *{user.first_name}* AFK!\n📝 {reason}", parse_mode=ParseMode.MARKDOWN)

async def check_afk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    user = update.effective_user
    if user.id in afk_db:
        del afk_db[user.id]
        await msg.reply_text(f"👋 *{user.first_name}* wapas aa gaya!", parse_mode=ParseMode.MARKDOWN)
        return
    if msg.reply_to_message:
        ru = msg.reply_to_message.from_user
        if ru and ru.id in afk_db:
            await msg.reply_text(f"😴 *{ru.first_name}* AFK hai!\n📝 {afk_db[ru.id]}", parse_mode=ParseMode.MARKDOWN)

# ════════════════════════════════════════════════════════
#  📊 INFO / ID / ADMINLIST / STATS / REPORT
# ════════════════════════════════════════════════════════

async def user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if msg.reply_to_message:
        u = msg.reply_to_message.from_user
        await msg.reply_text(f"👤 *{u.full_name}*\n🆔 `{u.id}`\n🔗 @{u.username or 'N/A'}", parse_mode=ParseMode.MARKDOWN)
    else:
        u = update.effective_user
        await msg.reply_text(f"👤 *Tumhara ID:* `{u.id}`\n💬 *Chat ID:* `{update.effective_chat.id}`", parse_mode=ParseMode.MARKDOWN)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = await get_target(update, context) or update.effective_user
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, t.id)
        u = member.user
        smap = {"creator":"👑 Owner","administrator":"⭐ Admin","member":"👤 Member",
                "restricted":"🚫 Restricted","left":"🚶 Left","kicked":"🔨 Banned"}
        await update.message.reply_text(
            f"ℹ️ *User Info:*\n\n"
            f"👤 [{u.full_name}](tg://user?id={u.id})\n"
            f"🆔 `{u.id}`\n🔗 @{u.username or 'N/A'}\n"
            f"🤖 Bot: {'Yes' if u.is_bot else 'No'}\n"
            f"📊 {smap.get(member.status, member.status)}",
            parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def adminlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        text = "👮 *Admins:*\n\n"
        for a in admins:
            role = "👑" if a.status == "creator" else "⭐"
            text += f"{role} [{a.user.full_name}](tg://user?id={a.user.id})\n"
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

async def chatinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    count = await context.bot.get_chat_member_count(chat.id)
    cid = chat.id
    await update.message.reply_text(
        f"💬 *Chat Info:*\n\n"
        f"📛 {chat.title}\n🆔 `{cid}`\n👥 Members: {count}\n"
        f"🔗 @{chat.username or 'N/A'}\n📁 {chat.type}\n\n"
        f"🔒 Lock: {'ON' if locked_db.get(cid) else 'OFF'}\n"
        f"🔗 Link Ban: {'ON' if linkban_db.get(cid) else 'OFF'}\n"
        f"🛡️ Spam Ban: {'ON' if spamban_db.get(cid) else 'OFF'}",
        parse_mode=ParseMode.MARKDOWN)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📊 *Bot Stats:*\n\n"
        f"📝 Notes: {sum(len(v) for v in notes_db.values())}\n"
        f"🔍 Filters: {sum(len(v) for v in filters_db.values())}\n"
        f"⚠️ Warns: {sum(sum(v.values()) for v in warns_db.values())}\n"
        f"👑 Owner: @{OWNER_USERNAME}",
        parse_mode=ParseMode.MARKDOWN)

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Jis message ko report karna ho usse reply karo!")
    reporter = update.effective_user
    ru = update.message.reply_to_message.from_user
    reason = " ".join(context.args) if context.args else "Koi reason nahi"
    try:
        admins = await context.bot.get_chat_administrators(update.effective_chat.id)
        mentions = " ".join([f"[{a.user.first_name}](tg://user?id={a.user.id})" for a in admins if not a.user.is_bot])
        await update.message.reply_text(
            f"🚨 *Report!*\n\n"
            f"📢 [{reporter.first_name}](tg://user?id={reporter.id})\n"
            f"⚠️ Reported: [{ru.first_name}](tg://user?id={ru.id})\n"
            f"📝 {reason}\n\n👮 {mentions}",
            parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")

# ════════════════════════════════════════════════════════
#  🔧 UTILITY
# ════════════════════════════════════════════════════════

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = time.time()
    msg = await update.message.reply_text("🏓 Pinging...")
    ms = round((time.time() - s) * 1000, 2)
    await msg.edit_text(f"🏓 Pong!\n⚡ *{ms}ms*", parse_mode=ParseMode.MARKDOWN)

async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ /calc 5+3*2")
    expr = " ".join(context.args)
    try:
        if not all(c in "0123456789+-*/.() " for c in expr):
            return await update.message.reply_text("❌ Sirf numbers aur + - * / ( ) use karo!")
        result = eval(expr)
        await update.message.reply_text(f"🧮 `{expr}` = *{result}*", parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text("❌ Invalid expression!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context, update.effective_user.id):
        return await update.message.reply_text("❌ Sirf admins echo kar sakte hain!")
    if not context.args: return await update.message.reply_text("⚠️ /echo [text]")
    try: await update.message.delete()
    except: pass
    await context.bot.send_message(update.effective_chat.id, " ".join(context.args))

async def time_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🕐 *Time:*\n`{datetime.now().strftime('%d %B %Y, %I:%M %p')}`", parse_mode=ParseMode.MARKDOWN)

# ════════════════════════════════════════════════════════
#  🚀 MAIN
# ════════════════════════════════════════════════════════

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("owner", owner_cmd))
    app.add_handler(CallbackQueryHandler(btn))

    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("kick", kick))
    app.add_handler(CommandHandler("tban", tban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("tmute", tmute))

    app.add_handler(CommandHandler("warn", warn))
    app.add_handler(CommandHandler("unwarn", unwarn))
    app.add_handler(CommandHandler("warns", warns_cmd))
    app.add_handler(CommandHandler("resetwarns", resetwarns))

    app.add_handler(CommandHandler("pin", pin))
    app.add_handler(CommandHandler("unpin", unpin))
    app.add_handler(CommandHandler("unpinall", unpinall))
    app.add_handler(CommandHandler("purge", purge))
    app.add_handler(CommandHandler("del", del_msg))

    app.add_handler(CommandHandler("promote", promote))
    app.add_handler(CommandHandler("demote", demote))

    app.add_handler(CommandHandler("save", save_note))
    app.add_handler(CommandHandler("get", get_note))
    app.add_handler(CommandHandler("notes", list_notes))
    app.add_handler(CommandHandler("clear", clear_note))
    app.add_handler(CommandHandler("clearall", clearall_notes))

    app.add_handler(CommandHandler("filter", add_filter))
    app.add_handler(CommandHandler("filters", list_filters))
    app.add_handler(CommandHandler("stop", stop_filter))
    app.add_handler(CommandHandler("stopall", stopall_filters))

    app.add_handler(CommandHandler("setrules", setrules))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("clearrules", clearrules))

    app.add_handler(CommandHandler("setwelcome", setwelcome))
    app.add_handler(CommandHandler("welcome", show_welcome))
    app.add_handler(CommandHandler("clearwelcome", clearwelcome))
    app.add_handler(CommandHandler("setgoodbye", setgoodbye))
    app.add_handler(CommandHandler("goodbye", show_goodbye))
    app.add_handler(CommandHandler("cleargoodbye", cleargoodbye))

    # 🔒 Lock System
    app.add_handler(CommandHandler("lock", lock))
    app.add_handler(CommandHandler("unlock", unlock))
    app.add_handler(CommandHandler("lockall", lockall))
    app.add_handler(CommandHandler("unlockall", unlockall))
    app.add_handler(CommandHandler("locks", locks_status))

    # 🔗 Link Ban
    app.add_handler(CommandHandler("linkban", linkban_cmd))

    # 🛡️ Spam Ban
    app.add_handler(CommandHandler("spamban", spamban_cmd))

    app.add_handler(CommandHandler("setflood", setflood))
    app.add_handler(CommandHandler("flood", flood_info))
    app.add_handler(CommandHandler("noflood", noflood))

    app.add_handler(CommandHandler("afk", afk))
    app.add_handler(CommandHandler("brb", afk))

    app.add_handler(CommandHandler("id", user_id))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("adminlist", adminlist))
    app.add_handler(CommandHandler("chatinfo", chatinfo))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("report", report))

    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("calc", calc))
    app.add_handler(CommandHandler("echo", echo))
    app.add_handler(CommandHandler("time", time_cmd))

    # Auto handlers
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, left_member))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_links),   group=1)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_spam),    group=2)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_flood),   group=3)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_filters), group=4)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hashtag_note),  group=5)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_afk),     group=6)

    print("=" * 55)
    print("🌹  MISS ROSE STYLE BOT — START HO GAYA!")
    print(f"👑  Owner: @{OWNER_USERNAME}")
    print("🔗  Link Ban: READY")
    print("🛡️  Spam Ban: READY")
    print("🔒  LockAll / UnlockAll: READY")
    print("✅  Sari commands ready hain!")
    print("⛔  Band karne ke liye Ctrl+C dabaao")
    print("=" * 55)
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
