# daPdfBot

A Telegram bot that summarises PDFs. Send it a PDF and it replies with a one-page summary, as a new PDF.

## How it works

1. `/auth <username> <password>` unlocks the bot (credentials come from environment variables).
2. Send a PDF; the bot saves it.
3. `/model gemini` picks the model, `/gen` runs it.
4. The PDF is uploaded to Gemini 2.0 Flash with a prompt for a summary of at most 300 words, returned as HTML.
5. WeasyPrint renders that HTML to PDF and the bot sends it back in the chat.

## Run

```sh
docker build -t dapdfbot .
docker run -e TELEGRAM_KEY=... -e GEMINI_KEY=... -e BOT_USERNAME=... -e BOT_PASSWORD=... dapdfbot
```

GitHub Actions builds the image and publishes it to GitHub Container Registry.

## Stack

Python, pyTelegramBotAPI, Google Gemini (google-genai), WeasyPrint, Docker, GitHub Actions.
