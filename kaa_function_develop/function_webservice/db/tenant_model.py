import sqlite3

class TenantModel:
    def __init__(self, kaa_db_file_path, id=None, tenant_name=None,
                 tenant_admin_username=None,
                 tenant_admin_password=None,
                 tenant_developer_username=None,
                 tenant_developer_password=None,
                 tenant_user_username=None,
                 tennat_user_password=None):
        self.id = id
        self.tenant_name = tenant_name
        self.tenant_admin_username = tenant_admin_username
        self.tenant_admin_password = tenant_admin_password
        self.tenant_developer_username = tenant_developer_username
        self.tenant_developer_password = tenant_developer_password
        self.tenant_user_username = tenant_user_username
        self.tennat_user_password = tennat_user_password
        self.dbconn = sqlite3.connect(kaa_db_file_path)

    def get_tenant_admin_account(self, id=None, tenant_name=None):
        # Return {"username": "admin",
        #         "password": "admin123"} for tenant admin account
        select = None
        if tenant_name:
            select = "select * from tenant" \
                     " where tenant_name='%s'" % tenant_name
        if id:
            select = "select * from tenant" \
                     " where id='%s'" % id
        get = self.dbconn.execute(select).next()
        return {"username": get[2],
                "password": get[3]}

    def get_tenant_developer_account(self, id=None, tenant_name=None):
        # Return {"username": "admin",
        #         "password": "admin123"} for tenant developer account
        select = None
        if tenant_name:
            select = "select * from tenant" \
                     " where tenant_name='%s'" % tenant_name
        if id:
            select = "select * from tenant" \
                     " where id='%s'" % id
        get = self.dbconn.execute(select).next()
        return {"username": get[4],
                "password": get[5]}

    def close_db_connect(self):
        self.dbconn.close()
