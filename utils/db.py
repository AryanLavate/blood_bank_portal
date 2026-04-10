import MySQLdb
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_connection():

    conn = MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME
    )

    return conn