import csv
import asyncio
import nest_asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ChatJoinRequestHandler
from telegram.error import TelegramError
from telegram.ext import CallbackContext

# Enable nested event loop for Jupyter notebook or other asynchronous environments
nest_asyncio.apply()

# Admin ID
ADMIN_ID = 6773787379

# Bot File ID for the photo (replace with your actual file ID)
file_id = "AgACAgQAAxkBAAMCZ2HDb6obJvEPEp9qJhZ6QsMOWuoAAlbFMRv1ORFTtVh02ftXt0sBAAMCAAN5AAM2BA"

# List to store user IDs who interacted with the bot
user_ids = set()  # Using a set to ensure unique user IDs

# Dictionary to store invite links for each chat
invite_links = {}

# Function to save user IDs to CSV
def save_user_ids_to_csv():
    with open('user_ids.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["User ID"])  # Only User ID in the CSV
        for user_id in user_ids:
            writer.writerow([user_id])

# Define the start command handler
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user

    # The new caption to be sent along with the image
    caption = (
        "• Fᴜʟʟ Cᴏʟʟᴇᴄᴛɪᴏɴ 🥳\n"
        "• Qᴜɪᴄᴋ Dᴇʟɪᴇᴠᴇʀʏ Sʏsᴛᴇᴍ 🏎️💨\n"
        "• Nᴏ Lɪɴᴋ❗, Dɪʀᴇᴄᴛ 🍃\n"
        "• Oʀɪɢɪɴᴀʟ Qᴜᴀʟɪᴛʏ ☄️\n"
        "• Pʟᴜs Bᴏɴᴜs⚜"
    )

    # Inline button to the external bot
    inline_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("𝗚𝗲𝘁 𝗡𝗼𝘄🔥", url="http://t.me/iinkprovider_bot?start=S")]
    ])

    # Send the photo with caption and inline button using file_id
    await update.message.reply_photo(
        file_id,  # Use the file ID here
        caption=caption, 
        parse_mode="HTML", 
        reply_markup=inline_button
    )

    # Add user ID to the set if not already present
    user_ids.add(user.id)

# Define the chat join request handler
async def approve(update: Update, context: CallbackContext):
    chat = update.chat_join_request.chat  # Correct way to access chat info in chat join requests
    user = update.chat_join_request.from_user  # Access the user who requested to join
    
    try:
        # Approve the join request and send message in parallel
        tasks = [
            context.bot.approve_chat_join_request(chat.id, user.id),
            send_welcome_message(context, user, chat)
        ]
        await asyncio.gather(*tasks)  # Run both tasks concurrently
        
    except TelegramError as e:
        print(f"Error while approving join request: {e}")
    except Exception as err:
        print(str(err))

# Function to send the welcome message with the image and caption
async def send_welcome_message(context: CallbackContext, user, chat):
    caption = (
        "• Fᴜʟʟ Cᴏʟʟᴇᴄᴛɪᴏɴ 🥳\n"
        "• Qᴜɪᴄᴋ Dᴇʟɪᴇᴠᴇʀʏ Sʏsᴛᴇᴍ 🏎️💨\n"
        "• Nᴏ Lɪɴᴋ❗, Dɪʀᴇᴄᴛ 🍃\n"
        "• Oʀɪɢɪɴᴀʟ Qᴜᴀʟɪᴛʏ ☄️\n"
        "• Pʟᴜs Bᴏɴᴜs⚜"
    )
    
    inline_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("𝗚𝗲𝘁 𝗡𝗼𝘄🔥", url="http://t.me/iinkprovider_bot?start=S")]
    ])
    
    # Send the photo using file_id with caption
    await context.bot.send_photo(user.id, file_id, caption=caption, parse_mode="HTML", reply_markup=inline_button)

# Define the detail command handler
async def detail(update: Update, context: CallbackContext):
    user = update.message.from_user
    if user.id == ADMIN_ID:
        if not invite_links:
            await update.message.reply_text("No groups or channels joined yet.")
        else:
            details_message = "Here are all the groups/channels the bot has joined:\n\n"
            for chat_id, invite_url in invite_links.items():
                chat = await context.bot.get_chat(chat_id)
                details_message += f"**{chat.title}**\nInvite URL: {invite_url}\n\n"
            
            await update.message.reply_text(details_message)
    else:
        await update.message.reply_text("You do not have permission to view this information.")

# Define the id command handler to send CSV
async def send_cv(update: Update, context: CallbackContext):
    user = update.message.from_user
    if user.id == ADMIN_ID:
        save_user_ids_to_csv()  # Save user IDs to CSV
        
        # Send the CSV file to the admin
        with open('user_ids.csv', 'rb') as file:
            await update.message.reply_document(file, caption="Here is the CV file with user IDs.")
    else:
        await update.message.reply_text("You do not have permission to access this data.")

# Function to set up the bot
