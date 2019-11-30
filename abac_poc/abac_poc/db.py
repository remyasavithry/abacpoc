from mongoengine import connect
from mongoengine.connection import disconnect

__all__ = ('setup_connection',)


def setup_connection():
    from django.conf import settings

    # Disconnect any previous session if any
    disconnect(alias=settings.DB_CONNECTION_STRING)

    try:
        connect(host=settings.DB_CONNECTION_STRING, **settings.DB_REPLICA_SET)
    except ConnectionError as conn_exc:
        print('DB Error: {}'.format(str(conn_exc)))
        exit(1)
