import sqlite3

class UserTemppassModel:
    def __init__(self, kaa_db_file_path, username=None,
                 temp_pass=None):
        self.username = username
        self.temp_pass = temp_pass
        self.dbconn = sqlite3.connect(kaa_db_file_path)

    def insert(self):
        # Return 0 if success
        insert_syntax = "INSERT INTO USER_TEMPPASS (USERNAME,TEMP_PASS)" \
                        " VALUES ('%s','%s')" % (self.username, self.temp_pass)
        try:
            a = self.dbconn.execute(insert_syntax)
            self.dbconn.commit()
            return 0
        except Exception as e:
            return e

    def get_record_use_username(self, username):
        # Success will return dict{"username": "exuser",
        #                          "temp_pass": "secret"}
        # Fail will return 1
        get_syntax = "select * from user_temppass" \
                     " where username='%s'" % username
        try:
            get = self.dbconn.execute(get_syntax).next()
            return {"username": get[0],
                    "temp_pass": get[1]}
        except:
            return 1

    def delete_record(self, username):
        # Return 0 if success
        del_syntax = "delete from user_temppass where username='%s'" % username
        try:
            self.dbconn.execute(del_syntax)
            self.dbconn.commit()
            return 0
        except Exception as e:
            return e

    def close_db_connect(self):
        self.dbconn.close()
