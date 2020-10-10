from mysql.connector import Error, MySQLConnection
from configparser import ConfigParser


def change_db_config(host: str, database: str, user: str, password: str, filename='config.ini'):
    config = ConfigParser()
    config.read(filename)

    # Change the mysql section in the .ini file
    config.set('mysql', 'host', host)
    config.set('mysql', 'database', database)
    config.set('mysql', 'user', user)
    config.set('mysql', 'password', password)

    with open(filename, 'w') as configfile:
        config.write(configfile)


def read_db_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    global config
    config = ConfigParser()
    config.read(filename)

    # get section, default to mysql
    db_config = {}
    if config.has_section(section):
        items = config.items(section)
        for item in items:
            db_config[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
    return db_config


class IsConnected:
    """This class is a helper class for check if connection_to_db method is called """
    db_connected = None

    def __init__(self):
        if IsConnected.db_connected is None:
            IsConnected.db_connected = self


def connection_to_db():
    global conn, cursor
    conn = None
    cursor = None

    db_config = read_db_config()
    try:
        print('Connecting to MySQL database...')
        if conn is not None:
            pass
        else:
            conn = MySQLConnection(**db_config)
            if conn.is_connected():
                print('Successfully connected to MySQL database!')
            else:
                print('Connection failed.')
    except Error as e:
        print(e.msg)
        return False

    if conn is not None and cursor is None:
        cursor = conn.cursor()
        # Call for IsConnected class for the purpose of change db_connected field value.
        IsConnected()
        return True


def close_connection():
    try:
        # Just if IsConnected class already cal then this if will be true.
        if IsConnected.db_connected is not None:
            cursor.close()
            conn.close()
            print("The connection to MySQL database is closed!")
    except Error as e:
        print(e.msg)
        return False


def run_db_query(query):
    """
    The method run this MySQL query to get the relevant data.\n
    :param query: is MySQL query for running.
    :return: list of list with required data.
    """
    if type(query) == str:
        cursor.execute(query)
        row = cursor.fetchall()
        data = list()
        for x in row:
            temp_list = []
            for i in x:
                if i is None:
                    temp_list.append("Null")
                else:
                    temp_list.append(i)
            data.append(temp_list)
        return data
    else:
        raise Exception("Error, method can only get str instance!")


def get_table_column_info(table_name):
    """The method return for evert given table:\n
    1.All the column names\n
    2.All the column types\n
    :param table_name: is the name of the table in the schema.
    :return: list of list with required data.
     """
    if type(table_name) == str:
        temp_db_name = config.get('mysql', 'database')
        query = "SELECT COLUMN_NAME, COLUMN_TYPE " \
                "FROM INFORMATION_SCHEMA.COLUMNS " \
                "WHERE TABLE_SCHEMA = '" + temp_db_name + "' AND TABLE_NAME = '" + table_name + "'"
        cursor.execute(query)
        row = cursor.fetchall()

        data = []
        for x in row:
            temp_list = list()
            temp_list.append(x[0])
            temp = str(x[1])
            if temp.startswith("b\'"):
                val = temp[len("b\'"):len(temp)-1]
            elif temp.startswith('b\"'):
                val = temp[len('b"'):len(temp)-1]
                val.strip('"\"')
            temp_list.append(val)
            data.append(temp_list)
        return data
    else:
        raise Exception("Error, table name can only get str instance!")


def create_query(table_name):
    if type(table_name) is str:
        table_info = get_table_column_info(table_name)
        query = "SELECT "
        i = 0
        for x in table_info:
            if i == len(table_info)-1:
                query += str(x[0]) + " "
            else:
                query += str(x[0]) + ", "
            i += 1
        query += "FROM " + table_name + ";"
        return query
    else:
        raise Exception("Error, table name can only get str instance!")
