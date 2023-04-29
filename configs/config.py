VERSION = '5.131'


import json


f = open("configs/config.json")
data =json.load(f)

USER_TOKEN = data['user_token']
GROUP_TOKEN = data['group_token']
CONSTR = data['constr']
CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')

del data

