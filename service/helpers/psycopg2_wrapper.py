'''
A wrapper on the psycopg2 driver that connects to the PostgreSQL database.

To be able to use this wrapper, four environment variables must be set:
-DB_NAME : the database name
-DB_USER: user credential for the database
-DB_PASSWORD: password credential of the database
-DB_HOST: host of the database

The wrapper can be used with python keyword `with` context manager,
as it reimplements exactly psycopg2 __enter__ and __exit__ methods with connection check
before hand.
The wrapper automatically checks that connection with the database is alive.
If not, it tries to connect to it.
WARNING: If transaction is not proceeded correctly, it does not attempt to reproceed
'''

import psycopg2


class ResilientConnection(object):

    def __init__(self, db_name, db_user, db_password, db_host):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host

        self.connection = None
        self.logger = None

        self._attempt_to_connect_to_db()

    def _check_connection_status_and_attempts_to_reconnect(self):
        '''
        Check connection status. If it is not connected to the database,
        it tries to establish a connection.
        '''
        if not self.connection or self.connection.closed != 0:
            self._attempt_to_connect_to_db()

        if not self.connection:
            raise psycopg2.OperationalError

    def _check_connection_status(self):
        '''
        Check connection status.
        Raises psycopg2.OperationalError if connection is not set.
        '''
        if not self.connection or self.connection.closed != 0:
            self.connection = None
            raise psycopg2.OperationalError

    def _attempt_to_connect_to_db(self):
        '''
        Attempts to connect to the database.
        If it fails it puts `self.connection` attribute to None.
        '''
        try:
            self.connection = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
            )
        except psycopg2.OperationalError:
            self.connection = None
            if self.logger:
                self.logger.warning(
                    {
                        'database_error': 'OperationalError',
                        'action': 'connect_to_db',
                    }
                )

    def __getattr__(
            self,
            attr
    ):
        '''
        This method returns all attribute from psycopg2 connection class
        '''
        self._check_connection_status_and_attempts_to_reconnect()

        return getattr(
            self.connection,
            attr,
        )

    def __enter__(self):
        self._check_connection_status_and_attempts_to_reconnect()

        return self.connection.__enter__()

    def __exit__(
            self,
            exception_type,
            exception_value,
            exception_traceback,
    ):
        self._check_connection_status()

        return self.connection.__exit__(
            exception_type,
            exception_value,
            exception_traceback,
        )

    def configure(self, **kwargs):
        '''
        Give a logger to be called when we encounter issues
        '''
        self.logger = kwargs.get('logger', None)
