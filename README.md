# Unofficial Notion SDK for Python

This is an unofficial Python client for the public Notion API.

Nothing fancy really; this client only is a thin layer on top of the Notion REST API. This means you can keep using the [official reference documentation](https://developers.notion.com/reference) to know which parameters to provide for each endpoint, or what responses to expect.

## Installation

- If you haven't already, first [create a Notion integration](https://developers.notion.com/docs/getting-started) so you'll have the required access token.
- Next, you can install `notion-api-python` as follows:
```
pip install -e git+https://github.com/timmolderez/notion-api-python.git#egg=notion-api-python
```
- Good to go! Have a look at the usage section below to get started.

## Usage

```python
from notion import NotionClient
from pprint import pprint
 
# ⚠ Be sure to set the NOTION_TOKEN environment variable to your
# integration token, or OAuth access token.
client = NotionClient()
response = client.get_database(database_id='0ae112de34684accb62cff2748402c5c')
pprint(response)
```

Output:
```
{'created_time': '2021-07-01T23:01:00.000Z',
 'id': '0ae112de-3468-4acc-b62c-ff2748402c5c',
 'last_edited_time': '2021-07-03T23:19:00.000Z',
 'object': 'database',
 'parent': {'type': 'workspace', 'workspace': True},
 'properties': {'Name': {'id': 'title', 'title': {}, 'type': 'title'},
                'Amount': {'id': '~?Lc',
                        'number': {'format': 'number'},
                        'type': 'number'},
...
```
This example simply demonstrates that the `get_database` method call corresponds directly to the REST API's [endpoint for retrieving databases](https://developers.notion.com/reference/get-database). It takes the same parameters; it produces the same JSON response. (except that it's converted to a `Dict` for convenience)

### Lists of objects

Some endpoints return a list of results. If that's the case, you can simply iterate over the list to get each result (i.e. no need to deal with pagination). Here's an example for the [endpoint to query a database](https://developers.notion.com/reference/post-database-query):  

Here's an example for the [endpoint to query a database](https://developers.notion.com/reference/post-database-query):

```python
from notion import NotionClient
from pprint import pprint

client = NotionClient()
results = client.query_database(
    database_id='0ae112de34684accb62cff2748402c5c',
    filter={"property": "Amount","number": {"greater_than_or_equal_to": 3}})
 for result in results:
     pprint(result)
```


## Related projects

- [jamalex/notion-py](https://github.com/jamalex/notion-py) - way more powerful than this project, as it's built on top of Notion's internal API (Security would be the main reason to stick to the public API.)
- [ramnes/notion-sdk-py](https://github.com/ramnes/notion-sdk-py) - similar to this project, but it's more faithful to the official Javascript Notion client, and easier to use asynchronously