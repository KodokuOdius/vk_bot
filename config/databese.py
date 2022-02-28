from simplePostgrConnector import PostgrDB
import settings

DB = PostgrDB(
    database_name=settings.database,
    user=settings.user,
    user_password=settings.user_password,
    host=settings.host,
    port=settings.port
)