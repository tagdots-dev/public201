import requests


# import yaml


owner_repo = "org/repo_name"
access_token = ""
headers = {'Authorization': f'token {access_token}'}

try:
    response_dict = requests.get(f"https://test.com/repos/{owner_repo}/tags", headers=headers)
except Exception as e:
    print(f"Error: {e}")
