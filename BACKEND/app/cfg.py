import configparser

class Config:
    config = configparser.ConfigParser()
    config.read("D:/PyProjects/JSB/BACKEND/app/config.ini")
    smtp_address = config.get('smtp', 'address')
    smtp_port = config.getint('smtp', 'port')

    postgres_base = config.get('PostgreSQL', 'base')
    postgres_port = config.getint('PostgreSQL', 'port')
    postgres_user = config.get('PostgreSQL', 'user')
    postgres_password = config.get('PostgreSQL', 'pwd')

    redis_host = config.get('REDIS', 'base')
    redis_port = config.getint('REDIS', 'port')
    redis_user = config.get('REDIS', 'user')
    redis_password = config.get('REDIS', 'password')

    email = config.get('AD', 'email')
    user = email.split('@')[0]
    password = config.get('AD', 'pwd')

    jira_server = config.get('JIRA', 'link')
    jira_user = config.get('JIRA', 'login')
    jira_api = config.get('JIRA', 'api_key')

    def get_redis_url(self):
        return f'redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/1'

cfg = Config()
