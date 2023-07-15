# zoho-client-django

A modest Zoho CRM API client which will do the oAuth2 for you.

```python
 from zoho_client.zoho import ZohoClient
 client = ZohoClient()
 # GET all Sales_Orders
 res = client.make_request(api_endpoint="Sales_Orders")
 for sales_order in res['data']:
    print(f"sales order #{sales_order['id']}")

 # find the first record
 sales_order_id = res['data'][0]['id']

 # update the sales order's subject
 payload = {'data': [ {'Subject': 'CHNAGED'}]}
 res = client.make_request(method='PUT', api_endpoint=f"Sales_Orders/{sales_order_id}", data=payload)
 print(res['data'][0]['status'])
 # => success

```

# setup

generate the refresh token

fetch the auth code:

scope:
ZohoCRM.modules.ALL,ZohoCRM.settings.ALL,ZohoCRM.users.ALL,ZohoCRM.bulk.ALL,ZohoCRM.notifications.ALL

choose either production or sandbox
press generate and copy the code and run this from the django console:

```python
from zoho_client.zoho import ZohoClient
# the code you have just copied
code = "1000.12c557408797e20c8432216dca0bbb5f.f1896d4f9e2329136806637798859a99"
ZohoClient().fetch_tokens(code)
# -> '1000.03b32b6490d8573e242664710bbc4f2c.e009198b6ab4b89013485657409e4913'
```
