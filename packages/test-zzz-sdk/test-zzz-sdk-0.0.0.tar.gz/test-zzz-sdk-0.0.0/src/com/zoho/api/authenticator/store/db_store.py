try:
    import logging
    import mysql.connector
    from mysql.connector import Error
    from src.authenticator.store.token_store import TokenStore
except Exception as e:
    import logging
    import mysql.connector
    from mysql.connector import Error
    from .token_store import TokenStore

class DBStore(TokenStore):
    logger = logging.getLogger('client_lib')

    def __init__(self, host=None, databasename=None, username=None, password=None, portnumber=None):
        self.host = host if host is not None else "localhost"
        self.database_name = databasename if databasename is not None else "zohooauth"
        self.user_name = username if username is not None else "root"
        self.password = password if password is not None else ""
        self.port_number = portnumber if portnumber is not None else "3306"

    def get_token(self, user, token):
        self.email = user.email
        try:
            connection = mysql.connector.connect(host=self.host, database=self.database_name, user=self.user_name,
                                                 password=self.password)
            cursor = connection.cursor()
            query = self.construct_dbquery(user, token, False)
            cursor.execute(query)
            result = cursor.fetchone()
            if result is not None:
                token.access_token = result[4]
                token.expires_in = result[6]
                token.refresh_token = result[3]
                return token
        except Error as e:
            DBStore.logger.error("Exception in get_token - DBStore", e, exc_info=1)
        finally:
            # cursor.close()
            connection.close()

        return None

    def save_token(self, user, token):
        self.delete_token(user, token)
        try:
            connection = mysql.connector.connect(host=self.host, database=self.database_name, user=self.user_name,
                                                 password=self.password)
            cursor = connection.cursor()
            query = "insert into oauthtoken (user_mail,client_id,refresh_token,access_token,grant_token,expiry_time) values (%s,%s,%s,%s,%s,%s);"
            val = (user.email, token.client_id, token.refresh_token,
                   token.access_token, token.grant_token, token.expires_in)
            cursor.execute(query, val)
            connection.commit()
        except Error as e:
            DBStore.logger.error("Exception in save_token - DBStore", e, exc_info=1)
        finally:
            cursor.close()
            connection.close()

    def delete_token(self, user, token):
        try:
            connection = mysql.connector.connect(host=self.host, database=self.database_name, user=self.user_name,
                                                 password=self.password)
            cursor = connection.cursor()
            query = self.construct_dbquery(user, token, True)
            cursor.execute(query)
            connection.commit()
        except Error as e:
            DBStore.logger.error("Exception in delete_token - DBStore", e, exc_info=1)
        finally:
            cursor.close()
            connection.close()

    def construct_dbquery(self, user, token, isdelete):
        query = "delete from " if isdelete is True else "select * from "
        query += "oauthtoken " + "where user_mail ='" + user.email + "' and client_id='" + token.client_id + "' and "
        if token.grant_token is not None:
            query += "grant_token='" + token.grant_token + "'"
        else:
            query += "refresh_token='" + token.refresh_token + "'"
        return query
