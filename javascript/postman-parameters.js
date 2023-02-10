const username = pm.variables.get('Volvo On-call Username')
const password = pm.variables.get('Volvo On-call Password')
console.log('Using username:' + username)
const postRequest = {
  url: 'https://volvoid.eu.volvocars.com/as/token.oauth2',
  method: 'POST',
  timeout: 0,
  header: {
    'authorization': 'Basic aDRZZjBiOlU4WWtTYlZsNnh3c2c1WVFxWmZyZ1ZtSWFEcGhPc3kxUENhVXNpY1F0bzNUUjVrd2FKc2U0QVpkZ2ZJZmNMeXc=',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'okhttp/4.10.0'
  },
  body: {
    mode: 'urlencoded',
    urlencoded: [
        { key: 'username', value: username},
        { key: 'password', value: password},
        { key: 'grant_type', value: 'password'},
        { key: 'scope', value: 'openid email profile care_by_volvo:financial_information:invoice:read care_by_volvo:financial_information:payment_method care_by_volvo:subscription:read customer:attributes customer:attributes:write order:attributes vehicle:attributes tsp_customer_api:all conve:brake_status conve:climatization_start_stop conve:command_accessibility conve:commands conve:diagnostics_engine_status conve:diagnostics_workshop conve:doors_status conve:engine_status conve:environment conve:fuel_status conve:honk_flash conve:lock conve:lock_status conve:navigation conve:odometer_status conve:trip_statistics conve:tyre_status conve:unlock conve:vehicle_relation conve:warnings conve:windows_status energy:battery_charge_level energy:charging_connection_status energy:charging_system_status energy:electric_range energy:estimated_charging_time energy:recharge_status vehicle:attributes'}
        ]
  }
};

pm.sendRequest(postRequest, function (err, res) {
    console.log('Granting access...');
    var responseJson = res.json();
    console.log(responseJson);
    pm.environment.set('Energy Access Token', responseJson['access_token']);
    pm.environment.set('Connected Vehicle Access Token', responseJson['access_token']);
    pm.environment.set('Extended Vehicle Access Token', responseJson['access_token']);
});