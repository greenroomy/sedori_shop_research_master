import requests
import yaml
import urllib

class MyKeepa(object):
    def __init__(self):
        with open('./data/config.yaml', 'r') as yaml_file:
            config_data = yaml.safe_load(yaml_file)
        self.graph_endpoint = 'https://api.keepa.com/graphimage'
        self.product_endpoint = 'https://api.keepa.com/product'
        self.access_key = config_data['keepa_config']['ACCESS_KEY']

    def get_graph_image(self, asin):
        '''
        :param asin: ASIN code list or ASIN code
        :return: IMAGE tag with keepa graph url
        ex)
        {'B01292389283': "=IMAGE("https://api.keepa.com/graphimage...")}
        '''
        end_point = self.graph_endpoint
        keepa_url_dict = {}
        if isinstance(asin, list):
            for elem in asin:
                if elem is not None:
                    params = {
                        'key': self.access_key,
                        'domain': 5,
                        'asin': elem,
                        'bb': 1,
                        'width': 1000,
                        'height': 400,
                        'salesrank': 1
                    }
                    url = end_point + '?' + urllib.parse.urlencode(params)
                    tag_url = '=IMAGE("{}")'.format(url)
                    keepa_url_dict[elem] = tag_url
            return keepa_url_dict
        else:
            params = {
                'key': self.access_key,
                'domain': 5,
                'asin': asin,
                'bb': 1,
                'salesrank': 1
            }
            url = end_point + '?' + urllib.parse.urlencode(params)
            tag_url = '=IMAGE("{}")'.format(url)
            keepa_url_dict[asin] = tag_url
            return keepa_url_dict

        # if mode == 'binary':
        #     response = requests.get(end_point, params)
        #     return response
        # elif mode == 'tag':
        #     url = end_point + '?' + urllib.parse.urlencode(params)
        #     tag_url = '=IMAGE("{}")'.format(url)
        #     return tag_url
        # elif mode == 'url':
        #     url = end_point + '?' + urllib.parse.urlencode(params)
        #     return url



