import	discord
import	init
import	utils
from	discord.ext		import commands, tasks

ft_uid = None
ft_secret = None
users_list = None
bot_channel_id = 0

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Game('Big Brother is watching you'))
	get_users_state.start()

@tasks.loop(minutes=5)
async def get_users_state():
	global users_list
	old_location_list = utils.get_current_location(users_list)
	new_location_list = utils.get_new_location(users_list, ft_uid, ft_secret)
	if (old_location_list != new_location_list):
		users_list = await utils.compare_location(bot, users_list, new_location_list, bot_channel_id)

def main():
	global users_list, ft_uid, ft_secret, bot_channel_id
	discord_token, ft_uid, ft_secret, user_ids , bot_channel_id = init.load_env()
	users_list = init.init_program(user_ids, ft_uid, ft_secret)
	bot.run(discord_token)

if (__name__ == "__main__"):
	main()