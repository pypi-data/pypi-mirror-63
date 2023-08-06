# eiprest

Python implementation of SOLIDserver REST client.

## Usage

As standalone executable script:

  - Using simple parameter format
    `eiprest.py -s solidserver.test.com dns_server_info dns_id=3`
  - Using json format
    `eiprest.py --server 10.0.99.99 dns_server_info '{"dns_id":3}'`

As python module in another script:

```
from eiprest import EipRest
rest = EipRest(host='10.0.99.99', user='ipmadmin', password='admin', debug=True)
params = {'dns_id': 3}
rest.query('GET', 'dns_server_info',  params)
rest.show_result()
```

Run eiprest.py -h to see all command line options.