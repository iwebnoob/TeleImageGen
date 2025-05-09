# TeleImageGen
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A Telegram bot that generates high-quality images based on user-provided text prompts. Published by **DIGI-X**.

## Features
- 📸 Generate images from Persian or English text prompts.
- 🌐 Automatic translation of Persian prompts to English for better results.
- 🔐 User authentication via phone number and channel membership.
- 📊 Tracks user statistics (e.g., number of generated images).
- 🚀 Asynchronous processing for handling multiple requests.
- 🛠 Error handling and logging for robust performance.

## Prerequisites
- Python 3.8+
- Telegram Bot Token (obtain from [BotFather](https://t.me/BotFather))
- Required Python packages (see `requirements.txt`)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/TeleImageGen.git
   cd TeleImageGen
Install dependencies:
bash

Copy
pip install -r requirements.txt
Create a .env file and add your bot token:
env

Copy
BOT_TOKEN=your-telegram-bot-token
Run the bot:
bash

Copy
python bot.py
Usage
Start the bot with /start.
Send a text prompt to generate an image (e.g., "A mountain landscape at sunset").
In groups, use /: followed by the prompt (e.g., /:A sunset over mountains).
Use /info to view your stats, /help for guidance, or /bug to report issues.
Authentication
Users must join the Telegram channel @DIGI_X.
Phone number verification is required for access.
Project Structure
text

Copy
TeleImageGen/
├── bot.py                # Main bot script
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not included in repo)
├── .gitignore            # Git ignore file
├── LICENSE               # MIT License
└── README.md             # This file
Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure your code follows PEP 8 guidelines and includes appropriate documentation.

License
This project is licensed under the MIT License. See the  file for details.

Publisher
DIGI-X
Telegram Channel: @DIGI_X
Telegram Username: @velovpn
Acknowledgments
Powered by python-telegram-bot.
Image generation via g4f.
Translation support by deep-translator.
Contact
For bug reports or feature requests, contact DIGI-X via Telegram: @velovpn or join the channel @DIGI_X.
