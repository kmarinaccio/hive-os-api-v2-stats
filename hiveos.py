from optparse import Values
import time
import json
import gmail
import requests
import traceback
import sched, time
from flask import Flask
from flask_caching import Cache
import datetime
import csv

app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

HIVE_EMAIL= "YOUR EMAIL"
HIVE_USERNAME= "YOUR USERNAME"
HIVE_PASSWORD= "YOUR PASSWORD"

HIVE_API_KEY = "YOUR HIVE OS API KEY"
CSV_PATH = "C:\\Users\\Public\\Documents\\rpt.csv"

s = sched.scheduler(time.time, time.sleep)

api_endpoint = "https://api2.hiveos.farm/api/v2/"

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': HIVE_API_KEY
}

@app.route("/")
def index():
    return ""


def get_otp_hive(retry = 0):
    print("Getting otp from HiveOS")
    current_otp = 0
    try:
        get_otp_ep = "auth/login/confirmation"
        response = requests.post(api_endpoint+get_otp_ep,
            headers=headers,
            data=json.dumps({
                "login": HIVE_USERNAME
            })
        )
        print("Sent otp request, waiting for 30 seconds before reading email")
        time.sleep(30)
        if response.status_code == 200:
            otps = gmail.get_otp()
            print("Got these otps from gmail %s" % otps)
            if len(otps) >= 1:
                current_otp = otps[0]
                return current_otp
        if current_otp == 0 and retry <= 1:
            print("OTP not found, retrying again")
            return get_otp_hive(retry=retry+1)
    except Exception as ex:
        if retry <= 1:
            return get_otp_hive(retry = retry+1)
    print("Even after retrying unable to get OTP.")
    return current_otp

def auth_hive():
    print("Checking for hive auth token cache")
    if cache.get("hive_auth_token"):
        print("Found Hive auth token cache, returning")
        return cache.get("hive_auth_token")
    print("Hive auth token cache not found")
    otp = get_otp_hive()
    auth_api_url = "auth/login"
    if otp > 0:

        # we have otp, send login request
        response = requests.post(api_endpoint + auth_api_url,
            headers=headers,
            data=json.dumps({
                "login": HIVE_USERNAME,
                "password": HIVE_PASSWORD,
                "twofa_code": str(otp),
                "remember": True
            })
        )
        print("auth login status code", response.status_code)
        if response.status_code == 200:
            data = response.json()
            if data.get("access_token", None):
                cache.set("hive_auth_token",data.get("access_token"), timeout=data.get("expires_in"))
                print("Got access_token from Hive caching it for future use")
                return data.get("access_token")
    print("Unable to get bearer token from hive api")
    return ""

def get_farm_data():
    bearer_token = auth_hive()
    print("Bearer Token: ", bearer_token)
    auth_header = {
        'Accept': 'application/json',
        "Authorization": "Bearer %s" % bearer_token
    }

    response = requests.get(api_endpoint+"farms", headers=auth_header)
    if response.status_code == 200:

        f = open(CSV_PATH, 'w')
        writer = csv.writer(f)

        farms_data = response.json()
        # from print import print; print(farms_data)
        farms_data = farms_data.get("data")
        for farm in farms_data:

            # so you are going to get the farm Name and Id and loop through each farm for the workers, if no workers skip it.
            if (farm.get("stats").get("workers_total") > 0):
                print("Farm ID - for future API calls",farm.get("id"))
                print("Farm Name: ", farm.get("name"), "--------------------")

                response = requests.get(api_endpoint+"farms/" + str(farm.get("id")) + "/workers", headers=auth_header) 
                workers_data = response.json()

                workers_data = workers_data.get("data")

                for worker in workers_data:
                    # Get the worker ids in the farm, for the stat call that's next
                    # print("     ", worker.get("name"), "   ID: ", worker.get("id"))

                    response = requests.get(api_endpoint + "farms/" + str(farm.get("id")) + "/workers/" + str(worker.get("id")) + "/metrics?date=2022-06-01&period=1m&fill_gaps=1", headers=auth_header) 
                    stats_data = response.json()

                    stats_data = stats_data.get("data")

                    for time in stats_data:

                        if time.get("hashrates") != []:
                            ethash = time.get("hashrates")
                        else:
                            ethash = 0
                        
                        # write a row to the csv file
                        writer.writerow({str(datetime.datetime.fromtimestamp(time.get("time"))) + "," + worker.get("name") + "," + str(ethash)})

            else:
                print(farm.get("name"), " skipped, no workers found.")

        # close the file
        f.close()
        print("Farm Data completed.")
        return ""

    print(response.status_code," Unable to fetch farm data")
    return ""

def start_metrics(s):
    if not (HIVE_EMAIL and HIVE_PASSWORD):
        print("Please set all environment variables before starting.")
        exit(1)
    try: 
        print("Calling, get_farm_data()")
        get_farm_data()
    except Exception as ex:
        print(traceback.format_exc())
        print("Unable to fetch data!!!")
    s.enter(int(99), 1, start_metrics, (s,))
    s.run()


start_metrics(s)
