from environs import Env


env = Env()
env.read_env('.env')

BOT_TOKEN = env.str('BOT_TOKEN')
ADMINS = env.list('ADMINS')
CHANNELS = env.list('CHANNELS')

