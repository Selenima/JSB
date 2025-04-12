from cachetools import TTLCache

blacklist = TTLCache(maxsize=7000, ttl=600)

def add_blacklist(user_id: int):
    blacklist[user_id] = True

def check_blacklist(user_id: int):
    return user_id in blacklist

def remove_blacklist(user_id: int):
    try:
        blacklist.pop(user_id)
    except KeyError:
        pass

