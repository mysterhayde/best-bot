import	os
import	requests
from	dotenv		import load_dotenv


def	init_user_dict(ft_user_list, ft_token_access):
	user_dict = {}
	for login in ft_user_list:
		auth_info = {"Authorization": f"Bearer {ft_token_access}"}
		request = requests.get(f"https://api.intra.42.fr/v2/users/{login}", headers=auth_info, timeout=15)
		request.raise_for_status()
		user_dict[login] = request.json()["location"]


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
	return (discord_token, ft_uid, ft_secret)