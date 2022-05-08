import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
class Database:
    """
        Constructor:
            create a connect to the database
            returns None if connection fails
    """
    def __init__(self):
        try:
            self.conn = psycopg2.connect(host = os.getenv('DB_HOST'), database = os.getenv('DB_NAME'), user = os.getenv('DB_USER'), password = os.getenv('DB_PASS'))
            self.curr = self.conn.cursor()
            print("connected")
        except print(0):
            print("Could not connect to database")
            return None
    
    def findAll(self):
        query = "SELECT * FROM users;"
        self.curr.execute(query,)
        users = self.curr.fetchall()
        return users

    """
        getUserByEmail function:
            functionality: number of rows modified for bound checking
        aguments: 
            email
        return:
            the name of the user with the given email
    """

    def getUserByEmail(self, email):
        query = " SELECT username FROM users WHERE email = %s"
        self.curr.execute(query, (email,))
        name = self.curr.fetchone()
        return name

    """
        update password function:
            functionality: number of rows modified for bound checking
        aguments: 
            email
            password
        return:
            number of rows modified for bound checking
    """

    def updatePassword(self, email, password):
        update_query = "UPDATE users SET password = %s WHERE email = %s"
        try:
            self.curr.execute(update_query, (password, email))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return self.curr.rowcount    