import time
import requests

ft_token_exp = 0
ft_token_access = None

def	get_access_token(ft_uid, ft_secret):
	global ft_token_exp, ft_token_access

	if (ft_token_access == None or time.time() > ft_token_exp - 60):
		request = requests.post(
			"https://api.intra.42.fr/oauth/token",
			data={"grant_type": "client_credentials", "client_id": ft_uid,"client_secret": ft_secret},
			timeout=15
		)
		request.raise_for_status()
		data = request.json()
		ft_token_access = data["access_token"]
		ft_token_exp = time.time() + data["expires_in"]
	return(ft_token_access)