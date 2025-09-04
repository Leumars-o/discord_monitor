import requests

url = "https://discord.com/api/v9/channels/1398068613365108871/messages"

auth = {
    'authorization': 'YOUR_TOKEN_HERE'
}

msg = {
    'content': 'hello channel!'
}

requests.post(url, headers = auth, data = msg)