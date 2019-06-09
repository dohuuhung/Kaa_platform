import configparser
import requests
import json
import pymongo
import uuid
import sqlite3
import os
from urllib import quote
from db.tables import TABLES
from db.user_password_model import UserPasswordModel
from db.tenant_model import TenantModel
from db.application_model import AppModel
from db.user_temppass_model import UserTemppassModel
from db.gateway_model import GatewayModel
from external_action.send_email import SendEmail
from requests.auth import HTTPBasicAuth
from flask import Flask
from flask import request
from flask_cors import CORS
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

CURRENT_WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
KAA_DASHBOARD_DB_DIR = "%s/sqlite_database" % CURRENT_WORKING_DIR
CONFIG_FILE_PATH = '/etc/kaa/kaa_dashboard_webservice.conf'
TOKEN_EXPIRATION = 600
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

URLS = {"account_authen": "http://%s:%s/kaaAdmin/rest/api/auth/checkAuth",
        "get_all_tenants": "http://%s:%s/kaaAdmin/rest/api/tenants",
        "create_user": "http://%s:%s/kaaAdmin/rest/api/user",
        "change_pass": "http://%s:%s/kaaAdmin/rest/api/auth/changePassword"
                       "?username=%s&oldPassword=%s&newPassword=%s",
        "get_users_of_tenant": "http://%s:%s/kaaAdmin/rest/api/users",
        "get_user_profile": "http://%s:%s/kaaAdmin/rest/api/user/%s",
        "delete_user": "http://%s:%s/kaaAdmin/rest/api/delUser?userId=%s",
        "get_current_user_profile": "http://%s:%s/kaaAdmin/rest/api/userProfile",
        "get_apps_of_tenant": "http://%s:%s/kaaAdmin/rest/api/applications",
        "get_all_using_apptoken": "http://%s:%s/kaaAdmin/rest/api/application/%s",
        "get_groups_of_app": "http://%s:%s/kaaAdmin/rest/api/endpointGroups/%s",
        "get_endpoints_of_group": "http://%s:%s/kaaAdmin/rest/api/"
                                  "endpointProfileByGroupId?endpointGroupId=%s",
        "get_endpoint_profile": "http://%s:%s/kaaAdmin/rest/api/endpointProfile/%s",
        "get_log_schema_use_apptoken_logver": "http://%s:%s/kaaAdmin/rest/api/logSchema/%s/%s",
        "delete_ep_profile": "http://%s:%s/kaaAdmin/rest/api/removeEndpointProfileByKeyHash"
                             "?endpointProfileKeyHash=%s"}

KAA_INFO = {"kaa_dashboard_webservice_addr": "localhost",
            "kaa_dashboard_webservice_port": "5000",
            "kaa_server_addr": "localhost",
            "kaa_server_port": "8080",
            "mongodb_addr": "localhost",
            "mongodb_port": "27017",
            "kaa_database_name": "kaa",
            "kaa_dashboard_db_name": "kaa_dashboard",
            "kaa_admin_username": "kaa",
            "kaa_admin_user_password": "kaa123",
            "default_tenant_admin_user": "admin",
            "default_tenant_admin_pass": "admin123",
            "gen_token_key": "xe3454g32"}

for i in KAA_INFO:
    try:
        if config['DEFAULT'][i]:
            KAA_INFO[i] = config['DEFAULT'][i]
    except:
        pass

KAA_DASHBOARD_DB_FILE_PATH = "%s/%s" % (KAA_DASHBOARD_DB_DIR,
                                        KAA_INFO['kaa_dashboard_db_name'])

headers = {'content-type': 'application/json',
           'accept': 'application/json'}

def get_all_tenants():
    get_tenants_url = URLS['get_all_tenants'] % (KAA_INFO['kaa_server_addr'],
                                                 KAA_INFO['kaa_server_port'])
    headers = {'accept': 'application/json'}
    _auth = HTTPBasicAuth(KAA_INFO['kaa_admin_username'],
                          KAA_INFO['kaa_admin_user_password'])
    tenants = requests.get(get_tenants_url,
                           headers=headers, auth=_auth).json()
    return tenants

def get_role_of_user(username, password):
    get_url = URLS['get_current_user_profile'] % (KAA_INFO['kaa_server_addr'],
                                                  KAA_INFO['kaa_server_port'])
    _auth = HTTPBasicAuth(username, password)
    get_result = requests.get(get_url,
                              headers=headers,
                              auth=_auth).json()
    role = get_result.get('authority')
    return role

def get_tenant_id_of_user(username, password):
    get_profile_url = URLS['get_current_user_profile'] % (KAA_INFO['kaa_server_addr'],
                                                          KAA_INFO['kaa_server_port'])
    _auth = HTTPBasicAuth(username, password)
    profile = requests.get(get_profile_url, headers=headers,
                           auth=_auth).json()
    tenant_id = profile.get('tenantId')
    return tenant_id

def get_appname_using_appid(app_id, username, password):
    get_apps_url = URLS['get_apps_of_tenant'] % (KAA_INFO['kaa_server_addr'],
                                                 KAA_INFO['kaa_server_port'])
    _auth = HTTPBasicAuth(username, password)
    apps_result = requests.get(get_apps_url, headers=headers,
                               auth=_auth).json()
    app_name = ''
    for _app in apps_result:
        if _app['id'] == app_id:
            app_name = _app['name']
            break
    return app_name

def get_apptoken_using_appid(app_id, username, password):
    get_apps_url = URLS['get_apps_of_tenant'] % (KAA_INFO['kaa_server_addr'],
                                                 KAA_INFO['kaa_server_port'])
    _auth = HTTPBasicAuth(username, password)
    apps_result = requests.get(get_apps_url, headers=headers,
                               auth=_auth).json()
    app_token = ''
    for _app in apps_result:
        if _app['id'] == app_id:
            app_token = _app['applicationToken']
            break
    return app_token

def get_parameters_of_app_use_token(app_token, username, password, tenant_id=None):
    am = AppModel(KAA_DASHBOARD_DB_FILE_PATH)
    app_record = am.get_using_app_token(app_token)
    am.close_db_connect()
    log_ver = app_record['log_ver']
    if get_role_of_user(username, password) in ['TENANT_ADMIN']:
        if not tenant_id:
            tenant_id = get_tenant_id_of_user(username, password)
        tm = TenantModel(KAA_DASHBOARD_DB_FILE_PATH)
        dvl_account = tm.get_tenant_developer_account(id=tenant_id)
        tm.close_db_connect()
        username = dvl_account['username']
        password = dvl_account['password']
    _auth = HTTPBasicAuth(username, password)
    get_log_schema_url = URLS['get_log_schema_use_apptoken_logver']\
                         % (KAA_INFO['kaa_server_addr'],
                            KAA_INFO['kaa_server_port'],
                            app_token,
                            log_ver)
    log_schema = requests.get(get_log_schema_url,
                              headers=headers,
                              auth=_auth).json()
    parameters = json.loads(log_schema.get('description'))
    return parameters



app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

UNKNOWN_ERROR_RESP = app.response_class(response='Unnknown error',
                                       status=401,
                                       mimetype='application/json')

authority = {"TENANT_USER": "Tenant user",
             "TENANT_DEVELOPER": "Tenant developer",
             "TENANT_ADMIN": "Tenant administrator",
             "KAA_ADMIN": "Kaa system administrator"}

def verify_token(token):
    if not token:
        response = app.response_class(
            response='Missing Token',
            status=405,
            mimetype='application/json'
        )
        return response
    else:
        upm = UserPasswordModel(KAA_DASHBOARD_DB_FILE_PATH)
        user_pass = upm.verify_auth_token(KAA_INFO['gen_token_key'], token)
        upm.close_db_connect()
        if user_pass == 401:
            response = app.response_class(
                response='Token expired',
                status=403,
                mimetype='application/json'
            )
            return response
        elif user_pass == 402:
            response = app.response_class(
                response='Invalid token',
                status=405,
                mimetype='application/json'
            )
            return response
        else:
            return 0, user_pass

@app.route("/")
def hello():
    return "Hello World"

# API1
@app.route("/api/login", methods=['POST', 'GET'])
def login():
    body = json.loads(request.get_data())
    username = body.get('username')
    password = body.get('password')
    account_auth_url = URLS['account_authen'] % (KAA_INFO['kaa_server_addr'],
                                                 KAA_INFO['kaa_server_port'])
    _auth = HTTPBasicAuth(username, password)
    auth_result = requests.get(account_auth_url,
                               headers=headers, auth=_auth)
    if auth_result.status_code == 200:
        upm = UserPasswordModel(KAA_DASHBOARD_DB_FILE_PATH,
                                username=username,
                                password=password)
        upm.insert()
        token = upm.generate_auth_token(KAA_INFO['gen_token_key'],
                                        expiration=TOKEN_EXPIRATION)
        auth_result = auth_result.json()
        tenants = get_all_tenants()
        tenant_name = None
        for tenant in tenants:
            if tenant['id'] == auth_result.get('tenantId'):
                tenant_name = tenant['name']
        rep_data = {"auth_result": auth_result.get('authResult'),
                    "authority": authority[auth_result.get('authority')],
                    "display_name": auth_result.get('displayName'),
                    "tenant_name": tenant_name,
                    "username": auth_result.get('username')}
        get_profile_url = URLS['get_current_user_profile'] % (KAA_INFO['kaa_server_addr'],
                                                              KAA_INFO['kaa_server_port'])
        profile_resp = requests.get(get_profile_url, headers=headers,
                                    auth=_auth).json()
        rep_data["user_id"] = profile_resp.get('id')
        upm.close_db_connect()
        response = app.response_class(
            response=json.dumps(rep_data),
            status=200,
            mimetype='application/json',
            headers={"token": token}
        )
        return response
    else:
        # There are 2 case: invalid username/password or
        # current password is temporary password, need change.


        utp = UserTemppassModel(KAA_DASHBOARD_DB_FILE_PATH)
        user_temppass = utp.get_record_use_username(username)
        utp.close_db_connect()
        # Case: wrong username/password
        if user_temppass == 1 or user_temppass['temp_pass'] != password:
            response = app.response_class(
                response='Username or password is invalid',
                status=403,
                mimetype='application/json'
            )
            return response
        # Case: Temporary password
        elif user_temppass['temp_pass'] == password:
            response = app.response_class(
                response='Current password is temporary,'
                         ' you need change password',
                status=402,
                mimetype='application/json'
            )
            return response
        else:
            return UNKNOWN_ERROR_RESP

#API2
@app.route("/api/registry", methods=['POST', 'GET'])
def registry():
    body_of_request = json.loads(request.get_data())
    registry_url = URLS['create_user'] % (KAA_INFO['kaa_server_addr'],
                                          KAA_INFO['kaa_server_port'])
    data = {"username": body_of_request.get('username'),
            "authority": "TENANT_USER",
            "firstName": body_of_request.get('firstname'),
            "lastName": body_of_request.get('lastname'),
            "mail": body_of_request.get('email')}
    tm = TenantModel(KAA_DASHBOARD_DB_FILE_PATH)
    tenant_admin_account = tm.get_tenant_admin_account(tenant_name=body_of_request.get('tenant_name'))
    tm.close_db_connect()
    _auth = HTTPBasicAuth(tenant_admin_account['username'],
                          tenant_admin_account['password'])
    registry_result = requests.post(registry_url,
                                    headers=headers,
                                    data=json.dumps(data),
                                    auth=_auth)
    if registry_result.status_code == 200:
        registry_result = registry_result.json()
        se = SendEmail()
        se.send_temporary_pass(registry_result.get('username'),
                               registry_result.get('tempPassword'),
                               registry_result.get('mail'))
        response = app.response_class(
            response='Success registration,'
                     'we will send a temporary password to your email address.',
            status=200,
            mimetype='application/json'
        )
        utp = UserTemppassModel(KAA_DASHBOARD_DB_FILE_PATH,
                                registry_result.get('username'),
                                registry_result.get('tempPassword'))
        utp.insert()
        utp.close_db_connect()
        return response
    else:
        return UNKNOWN_ERROR_RESP

#API3.1
@app.route("/api/change_temporary_password", methods=['POST', 'GET'])
def change_temporary_password():
    body_of_request = json.loads(request.get_data())
    username = body_of_request.get('username')
    old_password = body_of_request.get('old_password')
    new_password = body_of_request.get('new_password')
    change_pass_url = URLS['change_pass'] % (KAA_INFO['kaa_server_addr'],
                                             KAA_INFO['kaa_server_port'],
                                             username,
                                             old_password,
                                             new_password)
    _auth = HTTPBasicAuth(KAA_INFO['kaa_admin_username'],
                          KAA_INFO['kaa_admin_user_password'])
    change_pass_result = requests.post(change_pass_url,
                                       headers=headers,
                                       auth=_auth)
    if change_pass_result.status_code == 200:
        utp = UserTemppassModel(KAA_DASHBOARD_DB_FILE_PATH)
        utp.delete_record(username)
        utp.close_db_connect()
        response = app.response_class(
            response='OK',
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        return UNKNOWN_ERROR_RESP

#API3.2
@app.route("/api/change_password", methods=['POST', 'GET'])
def change_password():
    body_of_request = json.loads(request.get_data())
    old_password = body_of_request.get('old_password')
    new_password = body_of_request.get('new_password')
    token = request.headers.get('token')
    verify_result = verify_token(token)
    try:
        if verify_result[0] == 0:
            user_pass = verify_result[1]
            if old_password != user_pass['password']:
                response = app.response_class(
                    response='Wrong current password',
                    status=402,
                    mimetype='application/json'
                )
                return response
            else:
                change_pass_url = URLS['change_pass'] % (KAA_INFO['kaa_server_addr'],
                                                         KAA_INFO['kaa_server_port'],
                                                         user_pass['username'],
                                                         old_password,
                                                         new_password)
                _auth = HTTPBasicAuth(user_pass['username'],
                                      old_password)
                change_pass_result = requests.post(change_pass_url,
                                                   headers=headers,
                                                   auth=_auth)
                if change_pass_result.status_code == 200:
                    response = app.response_class(
                        response='OK',
                        status=200,
                        mimetype='application/json'
                    )
                    return response
                else:
                    return UNKNOWN_ERROR_RESP
    except:
        return verify_result

#API4
@app.route("/api/tenant_admin/users", methods=['POST', 'GET'])
def get_all_users_of_tenant():
    token = request.headers.get('token')
    verify_result = verify_token(token)
    try:
        if verify_result[0] == 0:
            user_pass = verify_result[1]
            get_url = URLS['get_users_of_tenant'] % (KAA_INFO['kaa_server_addr'],
                                                     KAA_INFO['kaa_server_port'])
            _auth = HTTPBasicAuth(user_pass['username'],
                                  user_pass['password'])
            get_user_result = requests.get(get_url,
                                           headers=headers,
                                           auth=_auth)
            if get_user_result.status_code == 200:
                get_user_result = get_user_result.json()
                get_user_result = [{"user_id": user['id'],
                                    "username": user['username']} for user in get_user_result]
                response = app.response_class(
                    response=json.dumps(get_user_result),
                    status=200,
                    mimetype='application/json'
                )
                return response
            else:
                return UNKNOWN_ERROR_RESP
    except:
        return verify_result

#API5
@app.route("/api/tenant_admin/users/profile/<user_id>", methods=['POST', 'GET'])
def get_user_profile(user_id):
    token = request.headers.get('token')
    verify_result = verify_token(token)
    try:
        if verify_result[0] == 0:
            user_pass = verify_result[1]
            get_url = URLS['get_user_profile'] % (KAA_INFO['kaa_server_addr'],
                                                  KAA_INFO['kaa_server_port'],
                                                  user_id)
            _auth = HTTPBasicAuth(user_pass['username'],
                                  user_pass['password'])
            get_user_profile_result = requests.get(get_url,
                                                   headers=headers,
                                                   auth=_auth)
            if get_user_profile_result.status_code == 200:
                get_user_profile_result = get_user_profile_result.json()
                resp_result = {"authority": authority[get_user_profile_result.get('authority')],
                               "firstname": get_user_profile_result.get('firstName'),
                               "lastname": get_user_profile_result.get('lastName'),
                               "email": get_user_profile_result.get('mail'),
                               "username": get_user_profile_result.get('username')}
                response = app.response_class(
                    response=json.dumps(resp_result),
                    status=200,
                    mimetype='application/json'
                )
                return response
            else:
                return UNKNOWN_ERROR_RESP
    except:
        return verify_result

#API6
@app.route("/api/tenant_admin/users/delete/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    token = request.headers.get('token')
    verify_result = verify_token(token)
    try:
        if verify_result[0] == 0:
            user_pass = verify_result[1]
            del_url = URLS['delete_user'] % (KAA_INFO['kaa_server_addr'],
                                              KAA_INFO['kaa_server_port'],
                                              user_id)
            _auth = HTTPBasicAuth(user_pass['username'],
                                  user_pass['password'])
            del_result = requests.post(del_url,
                                       headers=headers,
                                       auth=_auth)
            if del_result.status_code == 200:
                response = app.response_class(
                    response='OK',
                    status=200,
                    mimetype='application/json'
                )
                return response
            else:
                return UNKNOWN_ERROR_RESP
    except:
        return verify_result

#API7
@app.route("/api/current_user_profile", methods=['POST', 'GET'])
def get_current_user_profile():
    token = request.headers.get('token')
    verify_result = verify_token(token)
    try:
        if verify_result[0] == 0:
            user_pass = verify_result[1]
            get_url = URLS['get_current_user_profile'] % (KAA_INFO['kaa_server_addr'],
                                                          KAA_INFO['kaa_server_port'])
            _auth = HTTPBasicAuth(user_pass['username'],
                                  user_pass['password'])
            get_result = requests.get(get_url,
                                      headers=headers,
                                      auth=_auth)
            if get_result.status_code == 200:
                get_result = get_result.json()
                user_id = get_result.get('id')
                get_url_2 = URLS['get_user_profile'] % (KAA_INFO['kaa_server_addr'],
                                                        KAA_INFO['kaa_server_port'],
                                                        user_id)
                if get_result.get('authority') in ['TENANT_USER', 'TENANT_DEVELOPER']:
                    tm = TenantModel(KAA_DASHBOARD_DB_FILE_PATH)
                    tenant_admin_account = tm.get_tenant_admin_account(id=get_result.get('tenantId'))
                    tm.close_db_connect()
                    _auth = HTTPBasicAuth(tenant_admin_account['username'],
                                          tenant_admin_account['password'])
                if get_result.get('authority') in ['TENANT_ADMIN']:
                    _auth = HTTPBasicAuth(KAA_INFO['kaa_admin_username'],
                                          KAA_INFO['kaa_admin_user_password'])
                get_result_2 = requests.get(get_url_2,
                                            headers=headers,
                                            auth=_auth).json()
                resp_result = {"authority": authority[get_result.get('authority')],
                               "firstname": get_result_2.get('firstName'),
                               "lastname": get_result_2.get('lastName'),
                               "email": get_result.get('mail'),
                               "username": get_result.get('username')}
                response = app.response_class(
                    response=json.dumps(resp_result),
                    status=200,
                    mimetype='application/json'
                )
                return response
            else:
                return UNKNOWN_ERROR_RESP
    except:
        return verify_result

#API8.1
@app.route("/api/devices", methods=['POST', 'GET'])
def get_devices_of_tenant():
    token = request.headers.get('token')
    verify_result = verify_token(token)
    try:
        if verify_result[0] == 0:
            user_pass = verify_result[1]
            endpoints = []

            # Get all applications of tenant
            get_apps_url = URLS['get_apps_of_tenant'] % (KAA_INFO['kaa_server_addr'],
                                                         KAA_INFO['kaa_server_port'])
            _auth = HTTPBasicAuth(user_pass['username'],
                                  user_pass['password'])
            get_apps_result = requests.get(get_apps_url,
                                           headers=headers,
                                           auth=_auth)
            if get_apps_result.status_code == 200:
                get_apps_result = get_apps_result.json()

                # Get endpoints of applications

                if get_role_of_user(user_pass['username'],
                                    user_pass['password']) in ['TENANT_ADMIN']:
                    tm = TenantModel(KAA_DASHBOARD_DB_FILE_PATH)
                    dvp_account = tm.get_tenant_developer_account(id=get_apps_result[0]['tenantId'])
                    tm.close_db_connect()
                    _auth = HTTPBasicAuth(dvp_account['username'],
                                          dvp_account['password'])
                for _app in get_apps_result:
                    # Get group_id of group All
                    get_group_url = URLS['get_groups_of_app'] % (KAA_INFO['kaa_server_addr'],
                                                                 KAA_INFO['kaa_server_port'],
                                                                 _app['applicationToken'])
                    groups_result = requests.get(get_group_url, headers=headers,
                                                 auth=_auth).json()
                    group_all_id = ''
                    for group in groups_result:
                        if group['name'] == 'All':
                            group_all_id = group['id']
                            break

                    # Get endpoints of group All
                    get_ep_url = URLS['get_endpoints_of_group'] % (KAA_INFO['kaa_server_addr'],
                                                                   KAA_INFO['kaa_server_port'],
                                                                   group_all_id)
                    get_ep_result = requests.get(get_ep_url, headers=headers,
                                                 auth=_auth).json().get('endpointProfiles')
                    if not get_ep_result:
                        continue
                    get_ep_result = [{"device_name": json.loads(ep['clientProfileBody'])['name'],
                                      "device_key_hash": ep['endpointKeyHash'],
                                      "uuid": ep['id'],
                                      "status": 1} for ep in get_ep_result]
                    endpoints.extend(get_ep_result)
                response = app.response_class(
                    response=json.dumps(endpoints),
                    status=200,
                    mimetype='application/json'
                )
                return response
            else:
                return UNKNOWN_ERROR_RESP
    except:
        return verify_result

#API8.2
@app.route("/api/devices/delete/<device_key_hash>", methods=['DELETE'])
def delete_device_in_kaa_server(device_key_hash):
    token = request.headers.get('token')
    device_key_hash = device_key_hash.replace('F2FZAC', '/')
    print("device_key_hash_1: %s" % device_key_hash)
    verify_result = verify_token(token)
    try:
        if verify_result[0] == 0:
            user_pass = verify_result[1]
            username = user_pass['username']
            password = user_pass['password']
            if get_role_of_user(username, password) in ['TENANT_ADMIN']:
                tenant_id = get_tenant_id_of_user(username, password)
                tm = TenantModel(KAA_DASHBOARD_DB_FILE_PATH)
                dvl_account = tm.get_tenant_developer_account(id=tenant_id)
                tm.close_db_connect()
                username = dvl_account['username']
                password = dvl_account['password']
            _auth = HTTPBasicAuth(username, password)
            device_key_hash = quote(device_key_hash, safe='')
            print("device_key_hash_2: %s" % device_key_hash)
            print("device_key_hash: %s" % device_key_hash)
            del_url = URLS['delete_ep_profile'] % (KAA_INFO['kaa_server_addr'],
                                                   KAA_INFO['kaa_server_port'],
                                                   device_key_hash)
            print("del_url: %s" % del_url)
            print("username: %s" % username)
            print("password: %s" % password)
            del_result = requests.post(del_url, headers=headers,
                                       auth=_auth)
            if del_result.status_code == 200:
                response = app.response_class(
                    response='OK',
                    status=200,
                    mimetype='application/json'
                )
                return response
            else:
                return UNKNOWN_ERROR_RESP
    except:
        return verify_result

#API9
@app.route("/api/devices/overviews/<device_key_hash>", methods=['POST', 'GET'])
def get_overviews_of_device(device_key_hash):
    token = request.headers.get('token')
    device_key_hash = device_key_hash.replace('F2FZAC', '/')
    verify_result = verify_token(token)
    try:
        if verify_result[0] == 0:
            user_pass = verify_result[1]
            device_key_hash = quote(device_key_hash, safe='')
            get_ep_profile_url = URLS['get_endpoint_profile'] \
                                 % (KAA_INFO['kaa_server_addr'],
                                    KAA_INFO['kaa_server_port'],
                                    device_key_hash)
            _auth = HTTPBasicAuth(user_pass['username'],
                                  user_pass['password'])
            tenant_id = ''
            if get_role_of_user(user_pass['username'],
                                user_pass['password']) in ['TENANT_ADMIN']:
                tenant_id = get_tenant_id_of_user(user_pass['username'],
                                                  user_pass['password'])
                tm = TenantModel(KAA_DASHBOARD_DB_FILE_PATH)
                dvp_account = tm.get_tenant_developer_account(id=tenant_id)
                tm.close_db_connect()
                _auth = HTTPBasicAuth(dvp_account['username'],
                                      dvp_account['password'])
            print("tenant_id: %s" % tenant_id)
            ep_profile = requests.get(get_ep_profile_url, headers=headers,
                                      auth=_auth)
            if ep_profile.status_code == 200:
                ep_profile = ep_profile.json()
                device_type_id = ep_profile.get('applicationId')
                print("device_type_id: %s" % device_type_id)
                device_type_token = get_apptoken_using_appid(device_type_id,
                                                             user_pass['username'],
                                                             user_pass['password'])
                print("device_type_token: %s" % device_type_token)
                device_type_name = get_appname_using_appid(device_type_id,
                                                           user_pass['username'],
                                                           user_pass['password'])
                print("device_type_name: %s" % device_type_name)
                parameters = get_parameters_of_app_use_token(device_type_token,
                                                             user_pass['username'],
                                                             user_pass['password'],
                                                             tenant_id=tenant_id)
                print("parameters: %s" % parameters)
                resp_result = {"device_name": json.loads(ep_profile.get
                                                         ('clientProfileBody'))['name'],
                               "credentials": ep_profile.get('endpointKeyHash'),
                               "device_type": {"device_type_id": device_type_id,
                                               "device_type_token": device_type_token,
                                               "device_type_name": device_type_name,
                                               "parameters": parameters}}
                response = app.response_class(
                    response=json.dumps(resp_result),
                    status=200,
                    mimetype='application/json'
                )
                return response
            else:
                return UNKNOWN_ERROR_RESP
    except:
        return verify_result

#API10
@app.route("/api/devices/specifications/<device_key_hash>", methods=['POST', 'GET'])
def get_specifications_of_device(device_key_hash):
    token = request.headers.get('token')
    device_key_hash = device_key_hash.replace('F2FZAC', '/')
    verify_result = verify_token(token)
    try:
        if verify_result[0] == 0:
            user_pass = verify_result[1]
            device_key_hash = quote(device_key_hash, safe='')
            get_ep_profile_url = URLS['get_endpoint_profile'] \
                                 % (KAA_INFO['kaa_server_addr'],
                                    KAA_INFO['kaa_server_port'],
                                    device_key_hash)
            _auth = HTTPBasicAuth(user_pass['username'],
                                  user_pass['password'])
            if get_role_of_user(user_pass['username'],
                                user_pass['password']) in ['TENANT_ADMIN']:
                tenant_id = get_tenant_id_of_user(user_pass['username'],
                                                  user_pass['password'])
                tm = TenantModel(KAA_DASHBOARD_DB_FILE_PATH)
                dvp_account = tm.get_tenant_developer_account(id=tenant_id)
                tm.close_db_connect()
                _auth = HTTPBasicAuth(dvp_account['username'],
                                      dvp_account['password'])
            ep_profile = requests.get(get_ep_profile_url, headers=headers,
                                      auth=_auth)
            print("ep_profile.status_code: %s" % ep_profile.status_code)
            if ep_profile.status_code == 200:
                ep_profile = ep_profile.json()
                resp_result = json.loads(ep_profile.get('serverProfileBody'))
                response = app.response_class(
                    response=json.dumps(resp_result),
                    status=200,
                    mimetype='application/json'
                )
                return response
            else:
                return UNKNOWN_ERROR_RESP
    except:
        return verify_result

#API11
@app.route("/api/devices/monitor/<device_type_token>/<device_key_hash>", methods=['POST', 'GET'])
#API /api/devices/monitor/<device_type_token>/<device_key_hash>?parameter=&limit=
def get_monitor_of_device(device_type_token, device_key_hash):
    limit = request.args.get('limit', default=20, type=int)
    parameter = request.args.get('parameter', default='', type=str)
    token = request.headers.get('token')
    device_key_hash = device_key_hash.replace('F2FZAC', '/')
    verify_result = verify_token(token)
    try:
        if verify_result[0] == 0:
            try:
                myclient = pymongo.MongoClient("mongodb://%s:%s/" % (KAA_INFO['mongodb_addr'],
                                                                     KAA_INFO['mongodb_port']))
                mydb = myclient[KAA_INFO['kaa_database_name']]
                mycol = mydb["logs_%s" % device_type_token]
                myquery = {'header.endpointKeyHash.string': device_key_hash}
                mydocs = mycol.find(myquery).sort("_id", -1).limit(limit)
                records = []
                for mydoc in mydocs:
                    event = mydoc['event']
                    header = mydoc['header']
                    value = event[parameter]
                    try:
                        timestamp = header['timestamp']
                    except:
                        timestamp = ''
                    records.append({'timestamp': timestamp,
                                    'value': value})
                records = records[::-1]

                response = app.response_class(
                    response=json.dumps(records),
                    status=200,
                    mimetype='application/json'
                )
                return response
            except:
                return UNKNOWN_ERROR_RESP
    except:
        return verify_result

#API12
@app.route("/api/device_types", methods=['POST', 'GET'])
def get_device_types():
    token = request.headers.get('token')
    verify_result = verify_token(token)
    try:
        if verify_result[0] == 0:
            user_pass = verify_result[1]
            get_url = URLS['get_apps_of_tenant'] % (KAA_INFO['kaa_server_addr'],
                                                    KAA_INFO['kaa_server_port'])
            _auth = HTTPBasicAuth(user_pass['username'],
                                  user_pass['password'])
            get_result = requests.get(get_url, headers=headers,
                                      auth=_auth)
            if get_result.status_code == 200:
                get_result = get_result.json()
                resp_result = [{"device_type_id": dt.get('id'),
                               "device_type_token": dt.get('applicationToken'),
                               "device_type_name": dt.get('name')} for dt in get_result]
                response = app.response_class(
                    response=json.dumps(resp_result),
                    status=200,
                    mimetype='application/json'
                )
                return response
            else:
                return UNKNOWN_ERROR_RESP
    except:
        return verify_result

#API13
@app.route("/api/device_types/overviews/<device_type_token>", methods=['POST', 'GET'])
def get_overviews_of_device_types(device_type_token):
    token = request.headers.get('token')
    verify_result = verify_token(token)
    try:
        if verify_result[0] == 0:
            user_pass = verify_result[1]
            get_url = URLS['get_all_using_apptoken'] % (KAA_INFO['kaa_server_addr'],
                                                        KAA_INFO['kaa_server_port'],
                                                        device_type_token)
            _auth = HTTPBasicAuth(user_pass['username'],
                                  user_pass['password'])
            get_result = requests.get(get_url, headers=headers,
                                      auth=_auth)
            if get_result.status_code == 200:
                get_result = get_result.json()
                resp_result = {"device_type_id": get_result.get('id'),
                               "device_type_token": get_result.get('applicationToken'),
                               "device_type_name": get_result.get('name'),
                               "credential_service": get_result.get('credentialsServiceName')}
                response = app.response_class(
                    response=json.dumps(resp_result),
                    status=200,
                    mimetype='application/json'
                )
                return response
            else:
                return UNKNOWN_ERROR_RESP
    except:
        return verify_result

#API14
@app.route("/api/device_types/parameters/<device_type_token>", methods=['POST', 'GET'])
def get_parameters_of_device_type(device_type_token):
    token = request.headers.get('token')
    verify_result = verify_token(token)
    try:
        if verify_result[0] == 0:
            user_pass = verify_result[1]
            parameters = get_parameters_of_app_use_token(device_type_token,
                                                         user_pass['username'],
                                                         user_pass['password'])
            response = app.response_class(
                response=json.dumps(parameters),
                status=200,
                mimetype='application/json'
            )
            return response
        else:
            return UNKNOWN_ERROR_RESP
    except:
        return verify_result

#API16
@app.route("/api/registry_gateway/<gateway_name>", methods=['POST', 'GET'])
def registry_gateway(gateway_name):
    gateway_uuid = uuid.uuid1().hex
    status = 'ACTIVE'
    fake_status = 'ACTIVE'
    try:
        gm = GatewayModel(KAA_DASHBOARD_DB_FILE_PATH, uuid=gateway_uuid,
                          name=gateway_name, status=status,
                          fake_status=fake_status)
        gm.insert_gateway()
        gm.close_db_connect()
        response = app.response_class(
            response=json.dumps({"uuid": gateway_uuid}),
            status=200,
            mimetype='application/json'
        )
        return response
    except:
        return UNKNOWN_ERROR_RESP


if __name__ == '__main__':
    # Create table in database of kaa dashboard
    conn = sqlite3.connect(KAA_DASHBOARD_DB_FILE_PATH)
    print("Initiate tables in database of kaa dashboard")
    for create_table_command in TABLES:
        try:
            conn.execute(create_table_command)
        except Exception as e:
            print(e.message)

    app.run(host=KAA_INFO['kaa_dashboard_webservice_addr'],
            debug=True,
            port=KAA_INFO['kaa_dashboard_webservice_port'])
