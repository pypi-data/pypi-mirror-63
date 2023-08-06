import sys
from pydomo import Domo
from sqlalchemy import create_engine

class Database:
    def connect(**kwargs):
        try:
            if ("client_id" in kwargs and "client_secret" in kwargs):
                return Domo(kwargs["client_id"], kwargs["client_secret"])
            return create_engine(
                kwargs["connection_string"],
                connect_args = { "encoding":"UTF-8","nencoding": "UTF-8" }
            ).connect()
        except Exception as err:
            print("Unable to connect to database:")
            sys.exit(err)
