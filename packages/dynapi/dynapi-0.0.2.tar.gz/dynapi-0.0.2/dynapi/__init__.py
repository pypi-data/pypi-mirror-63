import requests, json
from dynalist import Dynalist as DynaFile
from decimal import Decimal
import getpass
import os


class DynalistIO:
    """
    Examples:

    api = DynalistIO()
    api.set_api_key(DYNALIST_API_KEY)

    # api.search_files(title='Plan')
    data = api.get_file(file_id='UdCecF09MdnK-eUJ0kYL_35k')
    """

    def __init__(self):
        self.cache = {}
        self.API_KEY = os.environ.get('DYNALIST_API_KEY', None)
        self.CACHING = False

    def set_api_key(self, apikey=None):
        if apikey is None:
            self.API_KEY = getpass.getpass(prompt='Enter Dynalist API key (generate one at https://dynalist.io/developer) (hidden input): ')
        else:
            self.API_KEY = apikey

    def search_files(self, title=None):
        files = requests.post(
            'https://dynalist.io/api/v1/file/list',
            data=json.dumps({'token': self.API_KEY})
        ).json()['files']

        if title is not None:
            files = list(filter(lambda x: title in x['title'], files))

        return files

    def search_nodes(self, file_id, title=None, node_id=None):
        "Only search top nodes."
        nodes = self.get_root_children(file_id)
        if title is not None:
            return list(filter(lambda x: title in str(x.get('content')) , nodes))
        elif node_id is not None:
            return next(filter(lambda x: str(x.get('id')==node_id) , nodes))
        else:
            return nodes

    def get_root_children(self, file_id):
        return self.get_file(file_id).get_children(node_id='root')

    def get_file(self, file_id, refresh=True):
        if file_id in self.cache and not refresh:
            return self.cache[file_id]
        else:
            client = DynaFile(file_id, token=self.API_KEY)
            if self.CACHING:
                self.cache[file_id] = client
            return client
