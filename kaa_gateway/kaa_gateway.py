import configparser
import requests
import json
import pymongo
from db.tables import TABLES
from db.application_model import ApplicationModel
from db.app_devices_model import AppDevicesModel
import sqlite3
import os
import subprocess
from requests.auth import HTTPBasicAuth
from flask import Flask
from flask import request
from flask_cors import CORS
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

CURRENT_WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
APP_TAR_DIR = '/var/lib/kaa_gateway/applications'
DEVICES_DIR = '/var/lib/kaa_gateway/devices'
KAA_DASHBOARD_DB_DIR = "%s/sqlite_database" % CURRENT_WORKING_DIR
CONFIG_FILE_PATH = '/etc/kaa/kaa_gateway.conf'
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

KAA_INFO = {"kaa_gateway_addr": "localhost",
            "kaa_gateway_port": "3004",
            "kaa_server_addr": "52.15.81.21",
            "kaa_server_port": "8080",
            "mongodb_addr": "localhost",
            "mongodb_port": "27017",
            "kaa_database_name": "kaa",
            "kaa_gateway_db_name": "kaa_dashboard",
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
                                        KAA_INFO['kaa_gateway_db_name'])

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

UNKNOWN_ERROR_RESP = app.response_class(response='Unnknown error',
                                        status=401,
                                        mimetype='application/json')

def get_app_tar_file_path_use_apptoken(app_token):
    am = ApplicationModel(KAA_DASHBOARD_DB_FILE_PATH)
    record = am.get_record_use_apptoken(app_token)
    am.close_db_connect()
    file_path = record['tar_file_path']
    return file_path

@app.route("/")
def hello():
    return "Hello World"

@app.route("/api/initiate_kaa_endpoint", methods=['POST'])
# API: /api/initiate_kaa_endpoint
# Body of request: {"application_token": "",
#                   "device_name": "",
#                   "broker_address": "",
#                   "topic": "",
#                   "client_id": "",
#                   "access_token": ""}
def initiate_kaa_endpoint():
    body = json.loads(request.get_data())
    application_token = body.get('application_token')
    device_name = body.get('device_name')
    broker_address = body.get('broker_address')
    topic = body.get('application_token')
    client_id = body.get('client_id')
    access_token = body.get('access_token')
    if not client_id:
        client_id = device_name
    app_tar_file_path = get_app_tar_file_path_use_apptoken(application_token)
    build_command = 'bash %s/initiate_kaa_endpoint.sh %s %s %s' % (CURRENT_WORKING_DIR,
                                                                   app_tar_file_path,
                                                                   DEVICES_DIR,
                                                                   device_name)
    build_process = subprocess.Popen(build_command.split(), stdout=subprocess.PIPE)
    build_process.wait()
    initiate_command = "%s/%s/%s/kaa-demo endpoint_key_hash.txt %s %s %s %s" % (DEVICES_DIR,
                                                                                device_name,
                                                                                device_name,
                                                                                device_name,
                                                                                broker_address,
                                                                                topic,
                                                                                client_id)
    binary_dir = "%s/%s/%s" % (DEVICES_DIR, device_name, device_name)
    init_process = subprocess.Popen(initiate_command.split(), stdout=subprocess.PIPE,
                                    cwd=binary_dir)
    pid = init_process.pid
    while not os.path.exists('%s/endpoint_key_hash.txt' % binary_dir):
        pass
    ep_key_hash = ''
    with open('%s/endpoint_key_hash.txt' % binary_dir, 'r') as f:
        ep_key_hash = f.read()
    adm = AppDevicesModel(KAA_DASHBOARD_DB_FILE_PATH,
                          ep_key_hash,
                          application_token,
                          pid)
    adm.insert()
    adm.close_db_connect()
    response = app.response_class(
        response='OK',
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    # Create table in database of kaa dashboard
    conn = sqlite3.connect(KAA_DASHBOARD_DB_FILE_PATH)
    print("Initiate tables in database of kaa dashboard")
    for create_table_command in TABLES:
        try:
            conn.execute(create_table_command)
        except Exception as e:
            print(e.message)

    app.run(host=KAA_INFO['kaa_gateway_addr'],
            debug=True,
            port=KAA_INFO['kaa_gateway_port'])