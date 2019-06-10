import sqlite3
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class UserPasswordModel:
    def __init__(self, kaa_db_file_path, username=None, password=None):
        self.username = username
        self.password = password
        self.dbconn = sqlite3.connect(kaa_db_file_path)
        self.id = None

    def insert(self):
        # return ID of inserted record
        insert_syntax = "INSERT INTO USER_PASSWORD (USERNAME,PASSWORD)" \
                        "VALUES ('%s', '%s')" % (self.username, self.password)
        a = self.dbconn.execute(insert_syntax)
        self.dbconn.commit()
        self.id = a.lastrowid
        return a.lastrowid

    def get_username_password_using_id(self, id):
        # return dict{"username": "exuser",
        #             "password": "secret"}
        print('id: %s' % id)
        get_syntax = "select * from user_password" \
                     " where id='%s'" % id
        get = self.dbconn.execute(get_syntax).next()
        return {"username": get[1],
                "password": get[2]}

    def check_existing_of_user(self, username):
        check_syntax = "select * from user_password" \
                       " where username='%s'" % username
        check = self.dbconn.execute(check_syntax)
        try:
            check.next()
            return True
        except:
            return False

    def delete_record(self, id):
        # Return 0 if success
        del_syntax = "delete from user_password where id=%s" % id
        try:
            self.dbconn.execute(del_syntax)
            return 0
        except Exception as e:
            return e

    def generate_auth_token(self, secret_key, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    def verify_auth_token(self, secret_key, token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return 401  # valid token, but expired
        except BadSignature:
            return 402  # invalid token
        user_pass = self.get_username_password_using_id(data['id'])
        return user_pass

    def close_db_connect(self):
        self.dbconn.close()
