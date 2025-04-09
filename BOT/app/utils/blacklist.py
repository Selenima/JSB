import aiofiles

class Blacklist:

    @staticmethod
    async def gen():
        async with aiofiles.open('blacklist.txt', mode='a+') as file:
            yield file

    @staticmethod
    async def blacklist(user_id):
        async with Blacklist.gen() as file:
            bl = await file.read().splitlines()
            user_id = str(user_id)
            if user_id not in bl:
                await file.write(f'{user_id}\n')

    @staticmethod
    async def check_user(user_id):
        async with Blacklist.gen() as file:
            bl = await file.read().splitlines()
            return user_id in bl
