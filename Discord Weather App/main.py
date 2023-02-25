import discord
from discord.ext import commands
import httpx

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')


@client.command()
async def weather(ctx, *, location):
    key = "files/API_KEY.txt"

    try:
        with open(key, "r") as api:
            api_key = api.read().strip()

        if not api_key:
            raise ValueError("API Key is empty or missing!")

        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'

        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)

        if response.status_code == 200:
            weather_data = response.json()
            temperature = round(weather_data['main']['temp'])
            description = weather_data['weather'][0]['description']
            await ctx.send(f'The weather in {location} is {temperature}°C and {description}.')
        else:
            await ctx.send('Failed to fetch weather information.')

    except Exception as e:
        await ctx.send(f'An error occurred: {str(e)}')


token_file = "files/token.txt"

try:
    with open(token_file, "r") as token:
        discord_token = token.read().strip()

    if not discord_token:
        raise ValueError("Discord token is empty in the token file.")

    client.run(discord_token)
except Exception as e:
    print(f'An error occurred while starting the client: {str(e)}')
