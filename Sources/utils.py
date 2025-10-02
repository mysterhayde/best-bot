import discord
import template
import requests
import api_token

def get_current_location(users_list: list[template.User]):
	location_list = {}
	for user in users_list:
		location_list[user.login] = user.location
	return (location_list)

def get_new_location(users_list: list[template.User], ft_uid, ft_secret):
	location_list = {}
	logins = [user.login for user in users_list]
	api_params = {"filter[login]": ",".join(logins)}
	auth_header = {"Authorization": f"Bearer {api_token.get_access_token(ft_uid, ft_secret)}"}
	response = requests.get("https://api.intra.42.fr/v2/users", headers=auth_header, params=api_params, timeout=15)
	response.raise_for_status()
	api_data = response.json()
	for user in api_data:
		login = user.get('login')
		location = user.get('location')
		location_list[login] = location
	return (location_list)

async def compare_location(bot: discord.Client, user_ids:list[template.User], new_location_list, bot_channel_id):
	for user in user_ids:
		new_loc = new_location_list.get(user.login)
		if (user.location != new_loc):
			if (not(user.location is not None and new_loc is not None)):
				user.location = new_loc
				await send_discord_msg(bot, bot_channel_id, user)
			else:
				user.location = new_loc
	return (user_ids)

async def send_discord_msg(bot, bot_channel_id, user):
	channel = bot.get_channel(bot_channel_id)
	if not channel:
		raise ValueError("CHANNEL ID NOT VALID")
	if (user.location is None):
		if (user.gender):
			await channel.send(f"{user.name} s'est déconnectée")
		else:
			await channel.send(f"{user.name} s'est déconnecté")
	else:
		if (user.gender):
			await channel.send(f"{user.name} s'est connectée")
		else:
			await channel.send(f"{user.name} s'est connecté")