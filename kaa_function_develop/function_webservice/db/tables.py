TABLES = [
            '''CREATE TABLE USER_PASSWORD
               (ID INTEGER PRIMARY KEY   AUTOINCREMENT  NOT NULL,
                USERNAME           TEXT    NOT NULL,
                PASSWORD           TEXT     NOT NULL);''',
            '''CREATE TABLE TENANT
               (ID TEXT PRIMARY KEY     NOT NULL,
                TENANT_NAME           TEXT    NOT NULL,
                TENANT_ADMIN_USERNAME            TEXT     NOT NULL,
                TENANT_ADMIN_PASSWORD            TEXT     NOT NULL,
                TENANT_DEVELOPER_USERNAME            TEXT     NOT NULL,
                TENANT_DEVELOPER_PASSWORD            TEXT     NOT NULL,
                TENANT_USER_USERNAME            TEXT     NOT NULL,
                TENANT_USER_PASSWORD            TEXT     NOT NULL);''',
            '''CREATE TABLE APPLICATION
               (APP_TOKEN TEXT PRIMARY KEY     NOT NULL,
                APP_NAME           TEXT    NOT NULL,
                CONFIG_VER            INT     NOT NULL,
                PROFILE_VER            INT     NOT NULL,
                NOTIFY_VER            INT     NOT NULL,
                LOG_VER            INT     NOT NULL);''',
            '''CREATE TABLE USER_TEMPPASS
               (USERNAME TEXT PRIMARY KEY     NOT NULL,
                TEMP_PASS           TEXT    NOT NULL);''',
            '''CREATE TABLE GATEWAY
               (UUID TEXT PRIMARY KEY     NOT NULL,
                NAME           TEXT    NOT NULL,
                STATUS           TEXT    NOT NULL,
                FAKE_STATUS           TEXT    NOT NULL,
                EXPIRED_TIME    INT NOT NULL);''',
            '''CREATE TABLE GATEWAY_APPLICATION
               (UUID TEXT      NOT NULL,
                APP_TOKEN           TEXT    NOT NULL,
                SDK_ID           TEXT    NOT NULL,
                PRIMARY KEY (UUID, APP_TOKEN),
                CONSTRAINT FK_UUID
                FOREIGN KEY (UUID)
                REFERENCES GATEWAY(UUID));''',
            '''CREATE TABLE GATEWAY_ENDPOINT
               (EP_KEY_HASH TEXT PRIMARY KEY     NOT NULL,
                UUID           TEXT    NOT NULL,
                CONSTRAINT FK_UUID
                FOREIGN KEY (UUID)
                REFERENCES GATEWAY(UUID));'''
         ]
