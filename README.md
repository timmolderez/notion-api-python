# Unofficial Notion SDK for Python
<img align=right src="https://raw.githubusercontent.com/timmolderez/notion-api-python/main/icon.png" />

This is an unofficial Python client for the public Notion API.

- Maps directly onto Notion's public REST API<br />(so you can keep using the [official reference documentation](https://developers.notion.com/reference))
- Abstracts away the technicalities<br />(pagination, HTTP headers, request methods)
- Enables adding Markdown-formatted text to new or existing Notion pages

## Installation

The `notion-api-python` library is installed as follows:
```
pip install -e git+https://github.com/timmolderez/notion-api-python.git#egg=notion-api-python
```

## Usage

### Getting started

If you haven't already, first [create a Notion integration](https://developers.notion.com/docs/getting-started) so you'll have the required authentication token.

Using the `notion-api-python` library is pretty straightforward: provide authentication, make a `NotionClient` instance, and every method of that instance corresponds directly to a Notion API endpoint. That's the gist of it.

To provide authentication, **set the `NOTION_TOKEN` environment variable** to your [internal integration token](https://www.notion.so/my-integrations), or [OAuth access token](https://www.notion.so/my-integrations). Alternatively, you can also pass your token directly to the `NotionClient` constructor.

Here's an example to get started:
```python
from notion import NotionClient
from pprint import pprint
 
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

This example creates a client, and retrieves the properties of the database with ID `0ae112de34684accb62cff2748402c5c`. (The simplest way to get the ID of a database or a page is to [look at its URL](https://stackoverflow.com/questions/67728038/where-to-find-database-id-for-my-database-in-notion).)

It's not a particularly interesting example, but the point is to demonstrate that the `get_database` method call corresponds directly to the REST API's [endpoint for retrieving databases](https://developers.notion.com/reference/get-database). It takes the same parameters; it produces the same JSON response. (except that the response is converted to a `Dict` for convenience)

It's the same story for all the other endpoints in the Notion API, so everything you need can be found in the API's [reference documentation](https://developers.notion.com/reference). (Feel free to browse through the rest of this Readme to find a few more complex examples.)

### Lists of objects

Some endpoints return a list of results. If that's the case, you can simply iterate over each result. (The library does all the pagination stuff under the hood, fetching pages as needed.)

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

### Markdown support

You can also easily add Markdown-formatted text to your Notion pages. An example:

```python
from notion import NotionClient
from io import StringIO

md_body = ('Hello **world**!\n\n'
           '- This is\n'
           '  - a `Markdown` list\n'
           '- with a [link](https://github.com/).')

client = NotionClient()
client.append_block_markdown(
    block_id='5f4ba0a7-e966-4ec3-b215-d0cae0cabbfa',
    md_body=StringIO(md_body))
```

- Use `append_block_markdown` to append Markdown-formatted text to an existing page (or to a block within an existing page).
- Use `create_page_markdown` to create a new page with Markdown-formatted text.

⚠ Not all of Markdown's features (currently) have an equivalent in Notion's public API. If you try to use an unsupported Markdown feature, a warning is produced with Python's built-in `logging` module.

## Related projects

You're spoiled for choice :) Here are a few other Notion clients in Python that I've bumped into:

- [jamalex/notion-py](https://github.com/jamalex/notion-py) - way more powerful than this project, as it's built on top of Notion's internal API (Security would be the main reason to stick to the public API.)
- [ramnes/notion-sdk-py](https://github.com/ramnes/notion-sdk-py) - similar to this project, but it's more faithful to the official Javascript Notion client
