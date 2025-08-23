# 1.TelegramBotForBuyingNewNftGifts
# 1. Data to be filled in:
File: impo.b_st_me.py Line: 9 – Telegram bot token.

File: impo.b_s.py Line: 25 – Redis port, database name.

File: impo.u_db.py Line: 4 – PostgreSQL password, localhost, database name.

File: impo.u_db.py Line: 48 – PostgreSQL password, localhost, database name.

File: impo.api_info.py - Write in terminal: uvicorn api_info:ai --host 0.0.0.0 --port 8000 (Not necessary, only if you need fast work with database)

# 2. How each file works:
File: impo.u_db.py – Creates two PostgreSQL engines: synchronous and asynchronous. The synchronous one creates all tables once on the first code run. The asynchronous one is used for all async queries.

File: impo.b_st_me.py – The router reacts to the /start command, creates a new user in the Users table with default settings if they don’t exist, and stores the user’s Telegram language setting in a Redis key.

File: impo.b_s.py – Script for launching the bot.

File: impo.b_g.py – Background task that checks for new NFT gifts. If new NFT gifts appear, it retrieves from the database all users who have topped up their balance, sorts them in descending order by balance, then iterates through each user profile and buys NFT gifts if they match the profile’s settings.

File: impo.b_dict.py – All messages and buttons in three languages: English, Russian, and Ukrainian.

File: impo.api_info.py - Getting information from database via FastiAPI.

File: cho.b_list_prof.py – Creates buttons with a brief description of each user profile.

File: cho.b_hist_py.py – Creates buttons with a brief description of each user purchase.

File: cho.b_call.py – All callbacks: profile creation, user profile list, changing profile status, changing the minimum quantity for NFT gift purchases, changing the maximum quantity for NFT gift purchases, changing the minimum price for NFT gift purchases, changing the maximum price for NFT gift purchases, topping up profile balance, deleting a profile, exiting a profile, topping up the user balance, detailed purchase information, user referral link and referral system message, changing language, and the logic for the “back” button.

# 3. How to launch:

1. Run impo.b_s.py

2. Write in terminal: uvicorn api_info:ai --host 0.0.0.0 --port 8000 (Not necessary, only if you need fast work with database)
