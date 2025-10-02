import	os
import	requests
import	api_token
from	dotenv		import load_dotenv
from	template	import User

def	init_program(users_ids : str, ft_uid, ft_secret):
	user_ids_list = [user.strip() for user in users_ids.split(',')]
	list_of_user_classes = [User(login=login) for login in user_ids_list]
	for index, user in enumerate(list_of_user_classes):
		if index < 2:
			user.gender = 1
	logins = [user.login for user in list_of_user_classes]
	api_params = {"filter[login]": ",".join(logins)}
	auth_header = {"Authorization": f"Bearer {api_token.get_access_token(ft_uid, ft_secret)}"}
	response = requests.get("https://api.intra.42.fr/v2/users", headers=auth_header, params=api_params, timeout=15)
	response.raise_for_status()
	api_data = response.json()
	api_data_array = {data['login']: data for data in api_data}
	for user in list_of_user_classes:
		if user.login in api_data_array:
			data = api_data_array[user.login]
			first_name = data.get('first_name')
			user.name = first_name.split(' ')[0]
			user.location = data.get('location')
	return (list_of_user_classes)

def	load_env():
	load_dotenv()
	discord_token = os.getenv("DISCORD_TOKEN")
	if not discord_token:
		raise ValueError("DISCORD_TOKEN not found")
	ft_uid = os.getenv("42_UID")
	if not ft_uid:
		raise ValueError("42_UID not found")
	ft_secret = os.getenv("42_SECRET")
	if not ft_secret:
		raise ValueError("42_SECRET not found")
	user_ids = os.getenv("USER_IDS")
	if not user_ids:
		raise ValueError("USER_IDS not found")
	bot_channel_id = os.getenv("BOT_CHANNEL_ID")
	if not bot_channel_id:
		raise ValueError("BOT_CHANNEL_ID not found")
	return (discord_token, ft_uid, ft_secret, user_ids, int(bot_channel_id))