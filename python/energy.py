import requests
import json

print ("Connecting...")

username = '<USER>'
password = '<PW>'
vccapikey = '<VCCAPIKEY>'

try:
    response = requests.post(
        "https://volvoid.eu.volvocars.com/as/token.oauth2",
        headers = {
            'authorization': 'Basic aDRZZjBiOlU4WWtTYlZsNnh3c2c1WVFxWmZyZ1ZtSWFEcGhPc3kxUENhVXNpY1F0bzNUUjVrd2FKc2U0QVpkZ2ZJZmNMeXc=',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'okhttp/4.10.0'
        },
        data = {
            'username': username,
            'password': password,
            'access_token_manager_id': 'JWTh4Yf0b',
            'grant_type': 'password',
            'scope': 'openid email profile care_by_volvo:financial_information:invoice:read care_by_volvo:financial_information:payment_method care_by_volvo:subscription:read customer:attributes customer:attributes:write order:attributes vehicle:attributes tsp_customer_api:all conve:brake_status conve:climatization_start_stop conve:command_accessibility conve:commands conve:diagnostics_engine_status conve:diagnostics_workshop conve:doors_status conve:engine_status conve:environment conve:fuel_status conve:honk_flash conve:lock conve:lock_status conve:navigation conve:odometer_status conve:trip_statistics conve:tyre_status conve:unlock conve:vehicle_relation conve:warnings conve:windows_status energy:battery_charge_level energy:charging_connection_status energy:charging_system_status energy:electric_range energy:estimated_charging_time energy:recharge_status vehicle:attributes'
        }
    )
    # print(json.dumps(response.json(), indent=4))
    print("Login successful!")
    print(response.json())
except requests.exceptions.RequestException as error:
    print("Login failed:")
    print(error)

access_token = response.json()['access_token']
# print(access_token)

try:
    vehicles = requests.get(
        "https://api.volvocars.com/extended-vehicle/v1/vehicles",
        headers= {
            "accept": "application/json",
            "vcc-api-key": vccapikey,
            "Authorization": "Bearer " + access_token
        }
    )
    print("\nResult:")
    print(vehicles)
    vjson=vehicles.json()
    print("Vin = "+str(vjson["vehicles"][0]["id"]))

    vehiclesjson = json.dumps(vehicles.json(), indent=4)
    print("\nResult JSON:")
    print(vehiclesjson)

except requests.exceptions.RequestException as error:
    print("Get vehicles failed:")
    print(error)

vin = vjson["vehicles"][0]["id"]

try:
    status = requests.get(
        "https://api.volvocars.com/energy/v1/vehicles/"+vin+"/recharge-status",
        headers= {
            "accept": "application/vnd.volvocars.api.energy.vehicledata.v1+json",
            "vcc-api-key": vccapikey,
            "Authorization": "Bearer " + access_token
        }
    )

    print("\nResult:")
    print(status)
    sjson=status.json()

    sjson = json.dumps(status.json(), indent=4)
    print("\nResult JSON:")
    print(sjson)

except requests.exceptions.RequestException as error:
    print("Get rechargestatus failed:")
    print(error)