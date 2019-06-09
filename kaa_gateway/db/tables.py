TABLES = [
            '''CREATE TABLE APPLICATION
               (APP_TOKEN TEXT PRIMARY KEY     NOT NULL,
                SDK_ID           TEXT    NOT NULL,
                TAR_FILE_PATH            INT     NOT NULL,
                TENANT_ID      TEXT    NOT NULL);''',
            '''CREATE TABLE APP_DEVICES
               (EP_KEY_HASH TEXT PRIMARY KEY     NOT NULL,
                APP_TOKEN           TEXT    NOT NULL,
                PID    TEXT    NOT NULL);'''
         ]
