from catalog.models import *
from .setup import *
from django.core.exceptions import ObjectDoesNotExist

def getLineUser(user:User):
    try:
        id = UserLineID.objects.get(user=user)
    except ObjectDoesNotExist:
        print(f'User {user} not found!')
        return None
    try:
        return line_bot_api.get_profile(id)['userId']
    except LineBotApiError as e:
        print('Error occured:   ')
        print(e)
        return None 