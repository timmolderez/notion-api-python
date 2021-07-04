import json
from os import getenv
from typing import Optional, Dict, List, Generator
from urllib.request import Request, urlopen

NOTION_API_URL = 'https://api.notion.com/v1/'
NOTION_VERSION = '2021-05-13'
PAGE_SIZE = 100


class NotionClient:
    def __init__(self, access_token: Optional[str] = None):
        """
        Notion client constructor
        Args:
            access_token: your secret Internal Integration Token
                (https://www.notion.so/my-integrations)
                If this argument is not provided, the environment variable
                NOTION_ACCESS_TOKEN is used instead.
        """
        self.access_token = (access_token if access_token
                             else getenv('NOTION_ACCESS_TOKEN'))

    def get_database(self, database_id: str) -> Dict:
        """https://developers.notion.com/reference/get-database"""
        return self._request(f'databases/{database_id}')

    def query_database(self, database_id: str,
                       filter: Dict = {},
                       sorts: List[Dict] = []) -> Generator[Dict, None, None]:
        """https://developers.notion.com/reference/post-database-query"""
        return self._paginated_request(f'databases/{database_id}/query',
                                       data={'filter': filter, 'sorts': sorts})

    def get_page(self, page_id: str) -> Dict:
        """https://developers.notion.com/reference/get-page"""
        return self._request('pages/' + page_id)

    def create_page(self, parent: Dict,
                    properties: Dict, children: List[Dict] = []) -> Dict:
        """https://developers.notion.com/reference/post-page"""
        return self._request('pages', data={'parent': parent,
                                            'properties': properties,
                                            'children': children})

    def update_page_properties(self, page_id: str, properties: Dict) -> Dict:
        return self._request(f'pages/{page_id}',
                             data={'properties': properties},
                             req_method='PATCH')

    def get_block_children(self, block_id: str) -> Generator[Dict, None, None]:
        """https://developers.notion.com/reference/get-block-children"""
        return self._paginated_request(f'blocks/{block_id}/children')

    def append_block_children(self, block_id: str,
                              children: List[Dict]) -> Dict:
        """https://developers.notion.com/reference/patch-block-children"""
        return self._request(f'blocks/{block_id}/children',
                             data={'children':children}, req_method='PATCH')

    def search(self, query: str,
               sort: Dict = {}, filter: Dict = {}) -> Generator[Dict, None, None]:
        """https://developers.notion.com/reference/post-search"""
        return self._paginated_request(
            'search', data={'query': query, 'sort': sort,'filter': filter})

    def get_user(self, user_id: str) -> Dict:
        """https://developers.notion.com/reference/get-user"""
        return self._request('users/' + user_id)

    def list_all_users(self) -> Generator[Dict, None, None]:
        """https://developers.notion.com/reference/get-users"""
        return self._paginated_request('users')

    def _paginated_request(self,
                           url_path: str,
                           data: Optional[Dict] = None,
                           req_method: Optional[str] = None
                           ) -> Generator[Dict, None, None]:
        """
        Used for endpoints that return a paginated list of results.
        This function yields each result one by one, and will request the
        next page of results as needed.

        Args:
            url_path: relative URL, without any pagination parameters
            data: a Dict with any additional POST/PATCH data
            req_method: request method ('GET', 'POST' or 'PATCH')
                (if not provided: 'POST' if data else 'GET')
        """
        separator = '&' if '?' in url_path else '?'
        next_cursor = None
        has_more = True

        while has_more:
            paginated_url_path = url_path
            if data:
                # Pass pagination parameters via POST/PATCH
                data['page_size'] = PAGE_SIZE
                if next_cursor:
                    data['start_cursor'] = next_cursor
            else:
                # Pass pagination parameters via GET
                params = f'page_size={PAGE_SIZE}'
                if next_cursor:
                    params += f'&start_cursor={next_cursor}'
                paginated_url_path = url_path + separator + params

            response = self._request(paginated_url_path, data, req_method)
            has_more = response.get('has_more', False)
            next_cursor = response.get('next_cursor', None)
            for result in response['results']:
                yield result

    def _request(self, url_path: str, data: Dict = None,
                 req_method: Optional[str] = None) -> Dict:
        """
        Make an HTTP request to the given URL
        Args:
            url_path: relative URL
            data: a Dict with any additional POST/PATCH data
            req_method: request method ('GET', 'POST' or 'PATCH')
                (if not provided: 'POST' if data else 'GET')
        Returns:
            the JSON response, converted to a Dict
        """
        data_bytes = None
        if data:
            data_bytes = str(json.dumps(data)).encode('utf-8')
        req = Request(NOTION_API_URL + url_path, data=data_bytes,
                      method=req_method)
        # The default urllib user agent is blocked, so let's use something else
        req.add_header('User-Agent', "curl/7.70.0")
        req.add_header("Authorization", "Bearer " + self.access_token)
        req.add_header("Notion-Version", NOTION_VERSION)
        if data:
            req.add_header('Content-Type', 'application/json')

        response = urlopen(req)
        return json.loads(response.read().decode('utf-8'))