import os
import requests
import asyncio
from bs4 import BeautifulSoup
from telegram.ext import ApplicationBuilder

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')

# Create the Application and pass it your bot's token.
async def send_daily_message(app):
    url = "https://sputnik.kz/news/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    soup = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')
    links = soup.find_all('a', href=True)

    filtered_hrefs = [link['href'] for link in links if "bugin-alemde-zhane-qazaqstanda-qanday-mereke-" in link['href']]

    soup = BeautifulSoup(requests.get(filtered_hrefs[0], headers=headers).text, 'html.parser')
    divs = soup.find_all('div', class_='article__block')

    output = ""
    for div in divs[2:]:
        text = div.get_text(separator=' ', strip=True)
        output += text + "\n\n"

    output = output.rpartition(";")[0]
    print(len(output))

    await app.bot.send_message(chat_id=CHANNEL_ID, text=output)

async def run_app():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Start the application (polling won't be strictly necessary if only scheduling)
    await app.initialize()
    await app.start()
    
    await send_daily_message(app)  # Await the async function

    await app.stop()

if __name__ == '__main__':
    asyncio.run(run_app())  # Use asyncio.run() to run the async function