# EduComicsAI

**EduComicsAI** — is a project for automatic generation of comics from text using artificial intelligence. The project combines the capabilities of the Stable Diffusion model for image generation and GigaChat for creating comic scripts.

---

## Main functions

- **Comic book script generation**: Using GigaChat to create a script based on entered text.
- **Image generation**: Using the Stable Diffusion model to create scripted images.
- **Adding Text to Images**: Overlay text on images using the Pillow library.
- **Assembling a comic**: Automatic assembly of comics from individual images.
- **Telegram bot**: Integration with Telegram for convenient generation of comics via a bot.
- **Web interface**: A simple web interface for generating comics via a browser.

---

## Technologies

- **Python**: The main programming language.
- **Flask**: Web framework for creating web interface.
- **Stable Diffusion**: Model for image generation.
- **GigaChat API**: API for generating text scripts.
- **Pillow (PIL)**: Library for working with images.
- **Telegram Bot API**: Integration with Telegram to create a bot.
- **NLTK**: Text processing library.
- **Bootstrap**: Styling the web interface.

---

## Installation and launch

### 1. Cloning a repository

```bash
git clone https://github.com/ваш-username/EduComixAI.git
cd EduComixAI
```

### 2. Installing dependencies
Make sure you have Python 3.8 or higher installed:

```bash
pip install -r requirements.txt
```

### 3. Setting up the environment
Create a .env file in the root of the project and add the following variables:

```bash
GIGACHAT_CREDENTIALS=your_gigachat_accounts
BOT_TOKEN=your_telegram_bot_token
```

### 4. Launching a web application
To run the web application, run:

```bash
python main.py
```
The application will be available at: http://127.0.0.1:5000.

### 5. Launching а Telegram bot
To launch the Telegram bot, run:

```bash
python EduComixAI_bot.py
```
Make sure you have specified your bot token in the file EduComixAI_bot.py.

## Usage

### Web interface
```
1. Go to the address http://127.0.0.1:5000.
2. Enter text in the input field.
3. Click "Generate Comic".
4. Download the finished comic in PNG format.
```

### Telegram bot
```
1. Find your bot in Telegram.
2. Send the text to the bot.
3. The bot will generate a comic and send it to you.
```

## Project structure

``` 
EduComicsAI/
├── .gitignore                # File to ignore unnecessary files in Git
├── README.md                 # Project documentation
├── requirements.txt          # List of dependencies
├── main.py                   # Main file of Flask application
├── EduComixAI_bot.py         # Telegram bot
├── temp_images/              # Temporary images (can be added to .gitignore)
├── static/                   # Static files (CSS, images, icons)
│   ├── ECAI.ico              # Site icon
│   └── styles.css            # Styles for web interface
├── templates/                # HTML templates
│   ├── index.html            # Home page
│   └── error.html            # Error page
├── utils/                    # Utilities and auxiliary modules
│   ├── comic_utils.py        # Text processing utilities
│   ├── gigachat_utils.py     # Utilities for working with GigaChat API
│   └── image_utils.py        # Image Utilities
└── venv/                     # Virtual environment (add to .gitignore)
