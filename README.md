
# TeleImageGen

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A Telegram bot that generates high-quality images from text prompts, supporting both Persian and English inputs. Published by **DIGI-X**.

## Features

- 📸 Generate images from Persian or English text prompts.
- 🌐 Automatically translates Persian prompts to English for improved results.
- 🔐 User authentication via phone number and Telegram channel membership.
- 📊 Tracks user statistics (e.g., number of images generated).
- 🚀 Asynchronous processing for handling multiple requests efficiently.
- 🛠 Robust error handling and logging for reliable performance.

## Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token (obtain from [BotFather](https://t.me/BotFather))
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/TeleImageGen.git
   cd TeleImageGen
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your bot token:
   ```env
   BOT_TOKEN=your-telegram-bot-token
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

1. Start the bot with `/start`.
2. Send a text prompt to generate an image (e.g., "A mountain landscape at sunset").
3. In group chats, use `/:` followed by the prompt (e.g., `/:A sunset over mountains`).
4. Use `/info` to view your stats, `/help` for guidance, or `/bug` to report issues.

## Authentication

- Users must join the Telegram channel: [@DIGI_X](https://t.me/DIGI_X).
- Phone number verification is required to access the bot.

## Project Structure

```
TeleImageGen/
├── bot.py                # Main bot script
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not included in repo)
├── .gitignore            # Git ignore file
├── LICENSE               # MIT License
└── README.md             # This file
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with clear documentation.
4. Ensure code follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines.

## License

This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for details.

## Publisher

**DIGI-X**  
- Telegram Channel: [@DIGI_X](https://t.me/DIGI_X)  
- Telegram Username: [@velovpn](https://t.me/velovpn)

## Acknowledgments

- Powered by [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).
- Image generation via [g4f](https://github.com/xtekky/gpt4free).
- Translation support by [deep-translator](https://github.com/nidhaloff/deep-translator).

## Contact

For bug reports or feature requests, contact DIGI-X via:  
- Telegram: [@velovpn](https://t.me/velovpn)  
- Channel: [@DIGI_X](https://t.me/DIGI_X)
