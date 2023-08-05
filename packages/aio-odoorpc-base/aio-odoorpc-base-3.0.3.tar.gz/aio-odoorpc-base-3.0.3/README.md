## Base functions to pilot Odoo's jsonrpc API (aio-odoorpc-base)

### Description:
This python package implements a **complete** set of methods to access  
Odoo's external API (using jsonrpc rather than xmlrpc).

It offers an almost-exact mirror of Odoo's external API, even parameter names are the same.
It is 'almost-exact' because 'execute' is skipped in favor of 'execute_kw' only and the 
It is 'almost-exact' because 'execute' is skipped in favor of 'execute_kw' only and the 
API methods from the 'db' service: 'list', 'drop', 'dump', 'rename', 'restore' are here 
implemented with names 'list_databases', 'drop_database', 'dump_database', 'rename_database'
and 'restore_database' respectively.  

The 'documentation' offered by this package is mostly in the form of proper type 
annotations so that you have a better idea of what kind of data each API method expects. 
Other than that, developers are recommended to go study Odoo's external API by reading the
source code at (https://github.com/odoo/odoo/tree/master/odoo/service). The three API services
'object', 'common' and 'db' are implemented there in files model.py, common.py and db.py 
respectively. On each of these python files, a 'dispatch' method is implemented for the service
in question. The methods available on the external service api are usually those prefixed with 
'exp_' in the method name, with the exception of the 'object' service which only exposes 
'execute' and 'execute_kw'.

All functions offered by this package are available in both async and sync versions.

Odoo's API methods implemented:
- about
- authenticate
- change_admin_password
- create_database
- db_exist
- drop_database
- dump_database
- duplicate_database
- execute_kw
- list_countries
- list_databases
- list_lang
- login
- migrate_databases
- rename_database
- restore_database
- server_version
- version

All methods take as first 2 parameters:
- **http_client**: a callable or an instance of a compatible http_client (it must implement a 'post'
  method that accepts a 'url' and a 'json' parameter. Packages 'requests', 'httpx' and 'aiohttp' are 
  compatible).
  If http_client is a callable, it will be called with a dict as the post payload and must return a 
  response object with a '.json()' method that may be synchronous or asynchronous (when using the async
  functions). It must return a dict or dict-like object representing the reponse.

- **url**: the complete URL of your Odoo's jsonrpc endpoint. Usually something like
  'https://odoo.acme.com/jsonrpc' or 'https://odoo.acme.com:8443/jsonrpc'. 

Remaining parameters on each method are those expected by Odoo's external API, with identical names
as you will find on Odoo's source code. The method 'jsonrpc' is the low-level method in this package that
actually does all the HTTP calls for all implemented methods.

By default, when you issue 'from aio_odoorpc_base import ...' you will be importing the async methods.
If you want the sync methods you must import from 'aio_odoorpc_base.sync'. You may also use 
'aio_odoorpc_base.aio' if you prefer to be explicit on whether you are importing sync or async code.


### aio-odoorpc: a higher-level API

In practice, you may notice that 99% of the time you will be calling the 'execute_kw' method
which is what allows you to deal with Odoo's models, reading and writing actual business data 
via the model methods 'search', 'read', 'search_read', 'search_count', 'write', 'create', etc.
While this package only offers you a bare 'execute_kw' method and a helper 'execute_kwargs', 
the higher-level package 'aio-odoorpc' expands over this one adding higher-level objects and methods
(such as 'search', 'read', 'search_read', 'search_count', 'write', 'create', etc) to consume those 
model methods through calls to 'execute_kw' external API method. 


### No dependencies:
No dependency is not a promise, just a preference. It may change in the future, but only if for very
good reason. Here, are free to use whatever HTTP Client library you want.

I am willing to make modifications in the code in order to support other http client solutions, 
just get in touch (use the project's github repository for that).

While it would be easier if this package shipped with a specific http client dependency, it should be
noted that having the possibility to reuse HTTP sessions is a great opportunity to improve the 
speed of your running code. Also, it is possible that your project is already using some http client
library and here you have the opportunity to use it. 

Remember that you must use an async http client library if you are going to use the async functions,
or use a synchronous http client library if you are going to use the sync function.

### Python HTTP Client packages known to be compatible:
- sync-only: 'requests'
- async-only: 'aiohttp'
- sync and async: 'httpx'

### Motivation:
The package 'odoorpc' is the most used and better maintained package to let you easily consume Odoo's
external API. It has lots of functionality, good documentation, a large user base and was developed
by people that are very experienced with Odoo in general and big contributors to the Odoo Community.  
In other words, if you are taking your first steps and do not need an async interface now, start with
odoorpc.

However, for my needs, once I was developing Odoo integrations that needed to make hundreds of calls
to the Odoo API to complete a single job, I began to sorely miss an async interface as well as more
control over the HTTP client used (I wished for HTTP2 support and connection polling/reuse).

Also, as I understood Odoo's external API, it started to sound like 'odoorpc' was too big for a task
too simple. For instance, most of the time (like 99,99% of the time), you will be calling to a single
jsonrpc method called 'execute_kw'. It is the same call over and over just changing the payload which 
itself is a simple json. 

So I decided to develop a new package myself, made it async-first and tryed to keep it as simple as
possible. Also, I decided to split it in two, a very simple base package (this one) with only methods
that mirror those in Odoo's external API and another one 'aio-odoorpc' that adds another layer to
implement Odoo's model methods like 'search', 'search_read', 'read', etc. as well as an object model
to instantiate a class once and then make simple method invocation with few parameters to access 
what you need.  


### Useful tips about Odoo's external API:

- The 'login' call is really only a lookup of the user_id (an int) of a user given a
  database name, user/login name and password. If you are using this RPC client over and over in your 
  code, maybe even calling from a stateless cloud service, you should consider finding out the 
  user id (uid) of the user and pass the uid instead of the username to the constructor of AsyncOdooRPC.
  This way, you do not need to call the login() RPC method to retrieve the uid, saving a RPC call;

- The uid mentioned above is not a session-like id. It is really only the database id of the user
  and it never expires. There is really no 'login' or 'session initiation' step required to access 
  Odoo's external API if you know the uid from the beginning;


### Other things to know about this module:
- It ships will a good suite of tests that run against an OCA runbot instance;

- Asyncio is a python3 thing, so no python2 support;

- Type hints are used everywhere;

- This package uses jsonrpc only (no xmlrpc). There is a lack of async xmlrpc tooling and
  jsonrpc is considered the best RPC protocol in Odoo (faster, more widely used);
  
- The synchronous version of the code is generated automatically from the asynchronous code, so at
  least for now the effort to maintain both is minimal.

- I am willing to take patches and to add other contributors to this project. Feel free to get in touch,
  the github page is the best place to interact with the project and the project's author;

- I only develop and run code in Linux environments, if you find a bug under other OS I am happy
  to take patches but I will not myself spend time looking into these eventual bugs;


### Usage

Ok, so let's start with some examples. I will omit the event_loop logic, I assume that if you want
to use an async module you already have that sorted out yourself or through a framework like FastAPI.

All examples below could also be called using the synchronous OdooRPC object, but without the
'await' syntax.

I recommend that you check the tests folder for many more examples. Also, the codebase is very very short,
do refer to it as well.

```
from aio_odoorpc_base.aio import login, execute_kw 
from aio_odoorpc_base.helpers import execute_kwargs
import httpx

url = 'https://odoo.acme.com/jsonrpc'

async with httpx.AsyncClient() as client:
    uid = await login(http_client=client, url=url, db='acme', login='demo', password='demo')
    kwargs = execute_kwargs(fields=['partner_id', 'date_order', 'amount_total'],
                            limit=1000, offset=0, order='amount_total DESC')
    data = await execute_kw(http_client=client,
                            url=url,
                            db='acme',
                            uid=uid,
                            password='demo',
                            obj='sale.order',
                            method='search_read',
                            args=[],
                            kw=kwargs)
```
