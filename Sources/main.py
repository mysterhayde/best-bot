import	os
import	discord
from 	discord.ext	import commands
from	dotenv		import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Game('Work in progress'))

def main():
	load_dotenv()
	token = os.getenv("DISCORD_TOKEN")
	if not token:
		raise ValueError("DISCORD_TOKEN not found")
	bot.run(token)

if __name__ == "__main__":
	main()