import discord
import requests
import os

# 🔧 Replace with your bot token and n8n webhook URL
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')

# Set up the bot with required intents
intents = discord.Intents.default()
intents.message_content = True  # Must match your bot settings in Discord portal

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return  # ignore messages from bots

    stock_symbol = message.content.strip().upper()

    # Basic filter: only allow 1-5 letter stock-like symbols
    if not stock_symbol.isalpha() or len(stock_symbol) > 5:
        return

    # Send the stock symbol to n8n webhook
    data = {
        "stock": stock_symbol,
        "user": message.author.name,
        "channel": message.channel.name
    }

    try:
        response = requests.post(N8N_WEBHOOK_URL, json=data)
        if response.status_code == 200:
            print(f"📬 Sent '{stock_symbol}' to n8n")
        else:
            print(f"⚠️ n8n responded with {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Failed to send to n8n: {e}")

# Run the bot
client.run(DISCORD_TOKEN)



