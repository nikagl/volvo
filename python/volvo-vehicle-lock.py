import requests
import json
from os.path import join, dirname, expanduser
from itertools import product

def read_config():
    """Read config from file."""

    # iterate folders and files
    for directory, filename in product(
        [
            ".",
            expanduser("~"),
        ],
        ["volvo.conf", ".volvo.conf"],
    ):
        try:
            # open folder / file
            config = join(directory, filename)
            with open(config) as config:
                # return the dictionary with parameters from config file
                return dict(
                    x.split(": ")
                    for x in config.read().strip().splitlines()
                    if not x.startswith("#")
                )
        except (IOError, OSError):
            # try next folder / file
            continue
    return {}

config = read_config()

username = config["volvoid_username"]
password = config["volvoid_password"]
vccapikey = config["vcc_apikey"]
vehicle = config["volvo_vin"]

try:
    authentication = requests.post(
        "https://volvoid.eu.volvocars.com/as/token.oauth2",
        headers = {
            'authorization': 'Basic aDRZZjBiOlU4WWtTYlZsNnh3c2c1WVFxWmZyZ1ZtSWFEcGhPc3kxUENhVXNpY1F0bzNUUjVrd2FKc2U0QVpkZ2ZJZmNMeXc=',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'okhttp/4.10.0'
        },
        data = {  
            'username': config["volvoid_username"],
            'password': config["volvoid_password"],
            'grant_type': 'password',
            'scope': 'openid email profile care_by_volvo:financial_information:invoice:read care_by_volvo:financial_information:payment_method care_by_volvo:subscription:read customer:attributes customer:attributes:write order:attributes vehicle:attributes tsp_customer_api:all conve:brake_status conve:climatization_start_stop conve:command_accessibility conve:commands conve:diagnostics_engine_status conve:diagnostics_workshop conve:doors_status conve:engine_status conve:environment conve:fuel_status conve:honk_flash conve:lock conve:lock_status conve:navigation conve:odometer_status conve:trip_statistics conve:tyre_status conve:unlock conve:vehicle_relation conve:warnings conve:windows_status energy:battery_charge_level energy:charging_connection_status energy:charging_system_status energy:electric_range energy:estimated_charging_time energy:recharge_status vehicle:attributes'
        }
    )
    print("Authentication successful!")
    access_token = authentication.json()['access_token']
except requests.exceptions.RequestException as error:
    print("Authentication failed: {}".format(error))

try:
    url = "https://api.volvocars.com/connected-vehicle/v2/vehicles/" + config["volvo_vin"] + '/commands/lock'
    print("URL: {}".format(url))
    vehicles = requests.post(
        url,
        headers= {
            "Content-Type": "application/json",
            "vcc-api-key": config["vcc_apikey"],
            "Authorization": "Bearer " + access_token
        }
    )
    print("Result: {}".format(vehicles))
    vehiclesjson = json.dumps(vehicles.json(), indent=4)
    print("\nResult JSON: {}".format(vehiclesjson))
except requests.exceptions.RequestException as error:
    print("Get vehicles failed:")
    print(error)
