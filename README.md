# Telegram Shop Bot (Python)

This project is a Telegram bot for selling digital goods, built using Python and the `pyTelegramBotAPI` library. It features a catalog system, user profiles, balance management (via QIWI), purchase history, and an admin panel for managing products and users.

## Features

*   **User Interface:**
    *   Interactive menu for browsing products.
    *   User profile with ID, username, registration date, and balance.
    *   Purchase history tracking.
    *   Balance replenishment via QIWI payment system.
    *   Referral system allowing users to earn a percentage of deposits made by referred users.
*   **Admin Panel:**
    *   Manage catalog sections (add, delete).
    *   Manage products within sections (add, delete).
    *   Upload products in bulk via text files.
    *   View basic user statistics.
    *   Manually adjust user balances.
    *   Send broadcast messages to all users.
    *   View top referrers and their earnings.
*   **Technical:**
    *   Callback queries for menu navigation.
    *   State management for multi-step processes (e.g., adding products, making purchases).

## Prerequisites

*   Python 3.x
*   `pyTelegramBotAPI` library (`pip install pyTelegramBotAPI`)
*   `requests` library (`pip install requests`)
*   A Telegram Bot Token (obtained from [@BotFather](https://t.me/BotFather))
*   A QIWI Wallet number and API token (for balance replenishment)

## Installation

1.  **Clone or Download:** Get the project files.
2.  **Install Dependencies:** Install the required Python libraries:
    ```bash
    pip install pyTelegramBotAPI requests
    ```
3.  **Configure `settings.py`:**
    *   `bot_token`: Paste your Telegram Bot Token.
    *   `admin_id`: Set your Telegram User ID to access the admin panel.
    *   `bot_login`: Set your bot's username (without @).
    *   `CHANNEL_ID`: (Optional) Set the numeric ID of a Telegram channel (without -100) to post payment/purchase notifications. Set to `0` if not used.
    *   `QIWI_NUMBER`: Enter your QIWI wallet number (e.g., `+77777777777`).
    *   `QIWI_TOKEN`: Enter your QIWI API token.
    *   Adjust `ref_percent` and text templates (`text_purchase`, `info`, `replenish_balance`, `profile`) as needed.
4.  **Initialize Database:** Run the bot once. It should create the `base_ts.sqlite` database file. Ensure the bot has write permissions in the directory.
5.  **Start the Bot:** Execute the main script:
    ```bash
    python main.py # or the name of your main file
    ```

## Usage

1.  **Start the Bot:** Message `/start` to your bot in Telegram.
2.  **User Navigation:**
    *   Use the inline buttons provided in the chat to navigate the shop (Catalog, Profile, Info, Purchases, Replenish Balance, Referral Web).
3.  **Admin Panel:**
    *   Message `/admin` to your bot (must be from the `admin_id` specified in `settings.py`).
    *   Use the admin menu to manage the catalog, products, view info, adjust balances, send messages, and view referral stats.

## Project Structure (Based on provided files)

*   `main.py`: The main script that initializes the bot, handles commands (`/start`, `/admin`), processes callback queries, and manages user interactions and admin functions.
*   `menu.py`: Defines the `InlineKeyboardMarkup` objects for various menus (main, admin, catalog, product selection, etc.).
*   `settings.py`: Contains configuration variables like bot token, admin ID, QIWI details, and text templates.
*   `functions.py` (likely the content of `menu.txt`): Contains core logic functions for database interaction (SQLite), menu generation (`menu_catalog`, `menu_section`, `menu_product`), admin actions (add/delete sections/products, upload), user actions (profile, basket, buy, check payment, replenish balance), and utility functions (referral system).
*   `base_ts.sqlite`: The SQLite database file created and used by the bot.

## Notes

*   Ensure your server/machine running the bot has internet access.
*   The bot uses long polling (`bot.polling`) which is suitable for development and simple deployments.
*   Be cautious with the admin panel access; protect your `admin_id`.
*   Test the QIWI payment integration thoroughly.
*   The referral link uses `https://teleg.run/` which redirects to Telegram.
