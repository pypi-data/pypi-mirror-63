"""
py-ms-sql.py: connects and pulls from an MS SQL server, will accommodate for
different operating systems.
"""
__author__ = "Timothy Reeder"
__version__ = "0.0.1"

import logging

import pyodbc
import pandas as pd


class ConnectSQL:
    """
    A generalised class that will connect to a MS SQL Server regardless of
    operating system. This class can be added to any project that requires a
    Netezza connection. For Windows, the DSN of a configured ODBC config can
    be used, or alternatively, using the ODBC driver. For other systems,
    all connection details need to be specified.

    Example:
    This example is just for the connect method, make sure to first create an
    object of the class (example assumes the object is called "sql_conn").
        DSN:
        $ sql_conn.connect(dsn='mysqldsn', uid='username', pwd='password')

        ODBC Driver:
        $ sql_conn.connect(driver_string="{SQL Server}; \
                                         SERVER=test;DATABASE=test;UID=user; \
                                         PWD=password")
        - OR -
        $ sql_conn.connect(driver='{SQL Server}',
                           server='server_name',
                           db='my_db',
                           uid='username',
                           pwd='password')

        MAC OSX:
        $ sql_conn.connect(host="my-server.com",
                           port=1433,
                           db="my_db",
                           uid='my_user',
                           pwd=password,
                           tds_version=7.3
                           driver='/usr/local/lib/libtdsodbc.so')
    """

    def __init__(self, logger=None):
        """
        An object is created with no open connections and an empty Pandas
        Data Frame. It requires the user to set up the connection before
        querying.

        :param logger: (optional) initialise a Pull object with a logger object
        """
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger()

        self.__conn = None
        self.__data = pd.DataFrame()
        self.logger.info("SQL Handler Initialised")

    def close_conn(self):
        """
        The connection can (RECOMMENDED) be closed manually

        :return: 0 for a success, or -1 with the error message for an error
        """
        try:
            if self.__conn:
                self.__conn.close()
                return 0, 'pass'

        except (TypeError, ValueError) as error:
            self.logger.exception("Closing MS SQL connection error")
            return -1, error

    def connect(self, *args, **kwargs):
        """
        To connect to a MS SQL Server, enter in the name of an ODBC which has
        valid connection details (Windows only), or all server details.
        Examples:

        - DSN:
          connect(dsn='MS_SQL', uid='username', pwd='password')
        - ODBC_DRIVER (A):
          connect(driver_string='Driver={SQL Server};Server=My_Server;
          Database=My_DB;UID=user;PWD=password')
        - ODBC_DRIVER (B):
          connect(driver='{SQL Server}', server='My_Server'
          db='My_DB', uid='username', pwd='password')
        - MAC OSX:
          connect(host="My_Server.com",
          db="My_DB", uid=r'my_user', tds_version='7.4', password=r'my_pass',
          port=1234, driver='/usr/local/lib/libtdsodbc.so')

        :param args: expected None
        :param kwargs: (dsn, uid, pwd) or (driver_string) or (driver, server,
        db, uid, pwd) or (host, port, db, user, pwd, tds_version, driver)
        :return: 0 for a success, or -1 with the error message for an error
        """
        self.logger.info("Connecting to MS SQL")

        # Initial result is set to 0 and error set to set-up string
        res, err = 0, "no value"

        if len(args) != 0:
            self.logger.warning("Only use keyword arguments. Any basic "
                                "arguments will not be used.")

        # Through multiple IF statements, look for which kind of connection
        # the user is calling.
        dsn_checks = ('dsn', 'uid', 'pwd')
        odbc_driver_a_checks = ('driver_string',)
        odbc_driver_b_checks = ('driver', 'server', 'db', 'uid', 'pwd')
        mac_osx_checks = ('server', 'port', 'database', 'user', 'password',
                          'tds_version', 'driver')

        # Check for the use of DSN
        if all(check in kwargs for check in dsn_checks):
            self.logger.info("Using ODBC with DSN")
            # Convert keyword arguments to string
            conn_string = 'DSN={};UID={};PWD={}'.format(kwargs['dsn'],
                                                        kwargs['uid'],
                                                        kwargs['pwd'])
            # Set up connection
            res, err = self.__pyodbc_conn(conn_string)

        # Check for use of driver string
        elif all(check in kwargs for check in odbc_driver_a_checks):
            self.logger.info("Using ODBC driver with a conn string")
            # Set up connection
            res, err = self.__pyodbc_conn(kwargs['driver_string'])

        # Check for use of driver string
        elif all(check in kwargs for check in odbc_driver_b_checks):
            self.logger.info("Using ODBC driver with a conn details")
            # Convert keyword arguments to string
            conn_string = 'DRIVER={};SERVER={};DATABASE={};' \
                          'UID={};PWD={}'.format(kwargs['driver'],
                                                 kwargs['server'],
                                                 kwargs['db'],
                                                 kwargs['uid'],
                                                 kwargs['pwd'])
            # Set up connection
            res, err = self.__pyodbc_conn(conn_string)

        # Check for use of driver string
        elif all(check in kwargs for check in mac_osx_checks):
            self.logger.info("Using Mac OSX conn method")
            # Set up connection
            res, err = self.__pyodbc_conn(**kwargs)

        # Error check
        if res == 0:
            self.logger.info("Connecting to MS SQL - Connected")
            return 0, 'pass'

        else:
            self.logger.error("Connecting to MS SQL  - Failed")
            return res, err

    def query(self, sql_statement):
        """
        Will run the query using the member's connection (__conn) and return
        a Pandas DataFrame

        :param sql_statement: (str) The query to run
        :return: Pandas DataFrame(), or -1 with the error message for an error
        """
        self.logger.info("Running query")
        try:
            # Run query
            self.__data = pd.read_sql(sql_statement, self.__conn)
            self.logger.info("Running query - Completed")
            return 0, self.__data

        # Exception Handling
        except ConnectionError as error:
            self.logger.exception("Query failed. Connection has closed from "
                                  "being idle. ",
                                  error)
            return -1, error

        except (ValueError, TypeError) as error:
            self.logger.exception("Query failed. PullNetezza.query() requires "
                                  "a query passed as a string. ",
                                  error)
            return -1, error

        except Exception as error:
            self.logger.exception("Query failed. General exception: ", error)
            return -1, error

    def __pyodbc_conn(self, *args, **kwargs):
        """
        Using PYODBC and the stored ODBC certificates, set up a connection to
        the database specified in the connection details in the ODBC

        :param odbc_string: Name of the ODBC certificate
        :return: 0 for a success, or -1 with the error message for an error
        """
        try:
            if len(kwargs) == 0 and len(args) == 1:
                self.__conn = pyodbc.connect(args[0])
            elif len(kwargs) > 0:
                self.__conn = pyodbc.connect(**kwargs)
            else:
                self.logger.warning('Only expecting 1 argument or multiple '
                                    'keyword arguments')
                return -1, 'error'
            return 0, 'pass'

        # Exception Handling
        except ConnectionError as error:
            self.logger.exception("ODBC connection failed.")
            return -1, error

        except Exception as error:
            self.logger.exception("ODBC connection failed. General exception:",
                                  error)
            return -1, error

