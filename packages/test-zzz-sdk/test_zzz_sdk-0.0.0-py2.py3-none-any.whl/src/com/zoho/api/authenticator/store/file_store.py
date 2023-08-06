try:
    import logging
    import csv
    from .token_store import TokenStore
    import os
except Exception as e:
    import logging
    import csv
    from .token_store import TokenStore
    import os


class FileStore(TokenStore):
    logger = logging.getLogger('client_lib')

    def __init__(self, filepath):
        self.file_path = filepath
        if (os.path.exists(filepath) and os.stat(filepath).st_size == 0) or not os.path.exists(filepath):
            with open(self.file_path, mode='w') as token_file:
                self.csv_writer = csv.writer(token_file, delimiter=',', quotechar='"',
                                             quoting=csv.QUOTE_MINIMAL)
                self.csv_writer.writerow(
                    ['user_mail', 'client_id', 'refresh_token', 'access_token', 'grant_token', 'expiry_time'])

    def get_token(self, user, token):
        try:
            lines = list()
            clientid = token.client_id
            email = user.email
            granttoken = token.grant_token
            refreshtoken = token.refresh_token
            with open(self.file_path, mode='r') as f:
                data = csv.reader(f, delimiter=',')
                for row in data:
                    lines.append(row)
                    tokencheck = granttoken == row[
                        4] if token.grant_token is not None else refreshtoken == \
                                                                 row[2]
                    if row[0] == email and row[1] == clientid and tokencheck:
                        token.access_token = row[3]
                        token.expires_in = row[5]
                        token.refresh_token = row[2]
                        return token
        except IOError as e:
            FileStore.logger.error("Exception in get_token - FileStore", e, exc_info=1)
        return None

    def save_token(self, user, token):
        self.delete_token(user, token)
        try:
            with open(self.file_path, mode='a+') as f:
                self.csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                self.csv_writer.writerow([user.email, token.client_id,
                                          token.refresh_token,
                                          token.access_token, token.grant_token,
                                          token.expires_in])
        except IOError as e:
            FileStore.logger.error("Exception in save_token - FileStore", e, exc_info=1)

    def delete_token(self, user, token):
        lines = list()
        clientid = token.client_id
        email = user.email
        granttoken = token.grant_token
        refreshtoken = token.refresh_token
        try:
            with open(self.file_path, mode='r') as f:
                data = csv.reader(f, delimiter=',')
                for row in data:
                    lines.append(row)
                    tokencheck = granttoken == row[
                        4] if token.grant_token is not None else refreshtoken == row[2]
                    if row[0] == email and row[1] == clientid and tokencheck:
                        lines.remove(row)
                        break
            with open(self.file_path, mode='w') as f:
                self.csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                self.csv_writer.writerows(lines)
        except IOError as e:
            FileStore.logger.error("Exception in delete_token - FileStore", e, exc_info=1)
