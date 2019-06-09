import sqlite3

class ApplicationModel:
    def __init__(self, kaa_db_file_path,
                 app_token=None, sdk_id=None,
                 tar_file_path=None, tenant_id=None):
        self.app_token = app_token
        self.sdk_id = sdk_id
        self.tar_file_path = tar_file_path
        self.tenant_id = tenant_id
        self.dbconn = sqlite3.connect(kaa_db_file_path)

    def insert(self):
        # Return 0 if success
        insert_syntax = "INSERT INTO APPLICATION (APP_TOKEN,SDK_ID,TAR_FILE_PATH,TENANT_ID)" \
                        " VALUES ('%s','%s','%s','%s')" % (self.ep_key_hash,
                                                           self.app_token,
                                                           self.pid,
                                                           self.tenant_id)
        try:
            a = self.dbconn.execute(insert_syntax)
            self.dbconn.commit()
            return 0
        except Exception as e:
            return e

    def get_record_use_apptoken(self, app_token):
        # Success will return dict{"app_token": "",
        #                          "sdk_id": "",
        #                          "tar_file_path": "",
        #                          "tenant_id": ""}
        # Fail will return 1
        get_syntax = "select * from application" \
                     " where app_token='%s'" % app_token
        try:
            get = self.dbconn.execute(get_syntax).next()
            return {"app_token": get[0],
                    "sdk_id": get[1],
                    "tar_file_path": get[2],
                    "tenant_id": get[3]}
        except:
            return 1

    def close_db_connect(self):
        self.dbconn.close()