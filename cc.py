from database.redis_mangager import RedisDB
REDIS_GZ = RedisDB()
REDIS_GZ.hset('specify_account_yctAppNo_page', {'getpage': 0, 'total': ''})

