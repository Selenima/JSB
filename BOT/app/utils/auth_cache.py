from cachetools import TTLCache

auth_cache = TTLCache(maxsize=100, ttl=60)

def add_to_cache(user_id: int):
    auth_cache[user_id] = True

def check_cache(user_id: int) -> bool:
    return user_id in auth_cache

starter_cache = TTLCache(maxsize=100, ttl=600)

def starter(user_id: int):
    starter_cache[user_id] = True

def check_starter(user_id: int):
    return user_id in starter_cache

def del_starter(user_id: int):
    del starter_cache[user_id]


