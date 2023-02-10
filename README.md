# volvo

## For Javascript:

- When you'd like to use the API's with Postman, you can use a Pre-request Script like the following:
postman-parameters.js

Simply define the Volvo On-call Username and Password variables and it replaces the access tokens from Andy Nash's collection:
https://www.postman.com/andynash/workspace/volvo-apis/collection/6009097-92ddc541-ef84-4d87-acec-03b1b19abd9b?action=share&creator=6009097

You can also use the default Volvo collections from here:
https://developer.volvocars.com/apis/connected-vehicle/specification/
https://developer.volvocars.com/apis/energy/specification/
https://developer.volvocars.com/apis/extended-vehicle/specification/

Import them into Postman and create the collections from the API. For this, use the following Pre-request Script:
postman-api-parameters.js

## For Python:
 
- rename or copy volvo.conf.sample

Use volvo-selenium.py to use your own api tokens
- currently only github authentication works (google does not allow selenium to logon "insecure browser")
- add all details (your username/password for developer portal, username/password for your volvo and your api-key from the developer portal)
- script only runs the vehiclelist and shows output as a proof of concept

Use the other python scripts (like volvo-vehicles.py) to use the generic oauth2 authorization

## For OpenHAB

Define the relevant items used in the DSL rules:
volvo.items

Use the rules file to define the rules that are triggered by the items:
volvo.rules

