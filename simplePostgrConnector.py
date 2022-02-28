import psycopg2
from typing_extensions import Literal


class PostgrDB:
    """
    (only keyword argument)
        - *database*: the database name 
        - *user*: user name used to authenticate
        - *password*: password used to authenticate user
        - *host*: database host address (defaults to UNIX socket if not provided)
        - *port*: connection port number (defaults to 5432 if not provided)
    """

    def __init__(
        self, *,
        database_name,
        user,
        user_password,
        host,
        port
    ) -> None:

        self.databese_name = database_name
        self.user = user
        self.user_password = user_password
        self.host = host
        self.port = port



    def request(self, request, mode=None): # Literal["fetchone", "fetchall", "fetchmany", "result"]
        connector = None
        try:
            connector = psycopg2.connect(
                database=self.databese_name,
                user=self.user,
                password=self.user_password,
                host=self.host,
                port=self.port
            )

            with connector.cursor() as cursor:
                cursor.execute(request)

                if mode is None:
                    return None

                modes = {
                    "fetchone": cursor.fetchone,
                    "fetchall": cursor.fetchall,
                    "fetchmany": cursor.fetchmany,
                }
                if mode == "result":
                    return len(cursor.fetchall())
                else:
                    return modes[mode]()

        except Exception as ex:
            print(ex)
        
        finally:
            if connector:
                connector.commit()
                connector.close()



