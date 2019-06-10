import sqlite3

class AppModel:
    def __init__(self, kaa_db_file_path, app_token=None, app_name=None,
                 config_ver=None,
                 profile_ver=None,
                 notify_ver=None,
                 log_ver=None):
        self.dbconn = sqlite3.connect(kaa_db_file_path)
        self.app_token = app_token
        self.app_name = app_name
        self.config_ver = config_ver
        self.profile_ver = profile_ver
        self.notify_ver = notify_ver
        self.log_ver = log_ver

    def insert(self):
        insert_syntax = "INSERT INTO APPLICATION (APP_TOKEN,APP_NAME,CONFIG_VER," \
                        "PROFILE_VER,NOTIFY_VER,LOG_VER) VALUES ('%s','%s',%s,%s," \
                        "%s,%s)" % (self.app_token, self.app_name,
                                        self.config_ver, self.profile_ver,
                                        self.notify_ver, self.log_ver)
        a = self.dbconn.execute(insert_syntax)
        self.dbconn.commit()
        return 0

    def get_using_app_token(self, app_token):
        # return dict{"app_token": "",
        #             "app_name": "",
        #             "config_ver": "",
        #             "profile_ver": "",
        #             "notify_ver": "",
        #             "log_ver": "",}
        get_syntax = "select * from application" \
                     " where app_token='%s'" % app_token
        get = self.dbconn.execute(get_syntax).next()
        return {"app_token": get[0],
                "app_name": get[1],
                "config_ver": get[2],
                "profile_ver": get[3],
                "notify_ver": get[4],
                "log_ver": get[5]}

    def close_db_connect(self):
        self.dbconn.close()