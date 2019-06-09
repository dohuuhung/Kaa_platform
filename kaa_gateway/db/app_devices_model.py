import sqlite3

class AppDevicesModel:
    def __init__(self, kaa_db_file_path,
                 ep_key_hash=None, app_token=None, pid=None):
        self.ep_key_hash = ep_key_hash
        self.app_token = app_token
        self.pid = pid
        self.dbconn = sqlite3.connect(kaa_db_file_path)

    def insert(self):
        # Return 0 if success
        insert_syntax = "INSERT INTO APP_DEVICES (EP_KEY_HASH,APP_TOKEN,PID)" \
                        " VALUES ('%s','%s','%s')" % (self.ep_key_hash,
                                                      self.app_token,
                                                      self.pid)
        try:
            a = self.dbconn.execute(insert_syntax)
            self.dbconn.commit()
            return 0
        except Exception as e:
            return e

    def close_db_connect(self):
        self.dbconn.close()