import sqlite3

class GatewayModel:
    def __init__(self, kaa_db_file_path, uuid=None,
                 name=None, status=None,
                 fake_status=None, app_token=None,
                 sdk_id=None, ep_key_hash=None):
        self.uuid = uuid
        self.name = name
        self.status = status
        self.fake_status = fake_status
        self.app_token = app_token
        self.sdk_id = sdk_id
        self.ep_key_hash = ep_key_hash
        self.dbconn = sqlite3.connect(kaa_db_file_path)

    def insert_gateway(self):
        # Return 0 if success
        insert_syntax = "INSERT INTO GATEWAY (UUID,NAME,STATUS,FAKE_STATUS)" \
                        " VALUES ('%s','%s', '%s','%s')" % (self.uuid, self.name,
                                                            self.status, self.fake_status)
        try:
            a = self.dbconn.execute(insert_syntax)
            self.dbconn.commit()
            return 0
        except Exception as e:
            return e

    def insert_gateway_application(self):
        # Return 0 if success
        insert_syntax = "INSERT INTO GATEWAY_APPLICATION (UUID,APP_TOKEN,SDK_ID)" \
                        " VALUES ('%s','%s','%s')" % (self.uuid, self.app_token,
                                                      self.sdk_id)
        try:
            a = self.dbconn.execute(insert_syntax)
            self.dbconn.commit()
            return 0
        except Exception as e:
            return e

    def insert_gateway_endpoint(self):
        # Return 0 if success
        insert_syntax = "INSERT INTO GATEWAY_ENDPOINT (EP_KEY_HASH,UUID)" \
                        " VALUES ('%s','%s')" % (self.ep_key_hash, self.app_token)
        try:
            a = self.dbconn.execute(insert_syntax)
            self.dbconn.commit()
            return 0
        except Exception as e:
            return e

    def delete_gateway_endpoint_record_use_epkeyhash(self, ep_key_hash):
        # Return 0 if success
        del_syntax = "delete from gateway_endpoint where ep_key_hash='%s'" % ep_key_hash
        try:
            self.dbconn.execute(del_syntax)
            self.dbconn.commit()
            return 0
        except Exception as e:
            return e

    def delete_gateway_endpoint_record_use_uuid(self, uuid):
        # Return 0 if success
        del_syntax = "delete from gateway_endpoint where uuid='%s'" % uuid
        try:
            self.dbconn.execute(del_syntax)
            self.dbconn.commit()
            return 0
        except Exception as e:
            return e

    def delete_gateway_application_record_use_uuid_apptoken(self, uuid, app_token):
        # Return 0 if success
        del_syntax = "delete from gateway_application where uuid='%s'" \
                     " and app_token='%s'" % (uuid, app_token)
        try:
            self.dbconn.execute(del_syntax)
            self.dbconn.commit()
            return 0
        except Exception as e:
            return e

    def delete_gateway_application_record_use_uuid(self, uuid):
        # Return 0 if success
        del_syntax = "delete from gateway_application where uuid='%s'" % uuid
        try:
            self.dbconn.execute(del_syntax)
            self.dbconn.commit()
            return 0
        except Exception as e:
            return e

    def delete_gateway_record_use_uuid(self, uuid):
        # Return 0 if success
        delete_gateway_endpoint_record_use_uuid(uuid)
        delete_gateway_application_record_use_uuid(uuid)
        del_syntax = "delete from gateway where uuid='%s'" % uuid
        try:
            self.dbconn.execute(del_syntax)
            self.dbconn.commit()
            return 0
        except Exception as e:
            return e

    def get_record_gateway_use_uuid(self, uuid):
        # Success will return dict{"uuid": "",
        #                          "name": "",
        #                          "status": "",
        #                          "fake_status": ""}
        # Fail will return 1
        get_syntax = "select * from gateway" \
                     " where uuid='%s'" % uuid
        try:
            get = self.dbconn.execute(get_syntax).next()
            return {"uuid": get[0],
                    "name": get[1],
                    "status": get[2],
                    "fake_status": get[3]}
        except:
            return 1

    def update_record_gateway_use_uuid(self, uuid, fake_status=None,
                                       name=None, status=None):
        try:
            if fake_status:
                update_syntax = "update gateway set fake_status='%s'" \
                                " where uuid='%s'" % (fake_status, uuid)
                self.dbconn.execute(update_syntax)
            if name:
                update_syntax = "update gateway set name='%s'" \
                                " where uuid='%s'" % (name, uuid)
                self.dbconn.execute(update_syntax)
            if status:
                update_syntax = "update gateway set status='%s'" \
                                " where uuid='%s'" % (status, uuid)
                self.dbconn.execute(update_syntax)
            return 0
        except:
            return 1

    def close_db_connect(self):
        self.dbconn.close()