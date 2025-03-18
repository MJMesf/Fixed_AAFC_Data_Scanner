"""This code tests the DataCatalogue class implemented in __main__.py and is 
intended to be run from project's top folder using:
  py -m unittest tests.test_data_catalogue
Use -v for more verbose.
"""

from aafc_data_scanner.constants import *
from aafc_data_scanner.tools import *

import unittest


class TestDataCatalogue(unittest.TestCase):

    def test_init(self):

        base_url1 = 'https:/example.com/'
        dc1 = RequestsDataCatalogue(base_url1)
        self.assertEqual(dc1.base_url, base_url1)

        base_url2 = ''
        dc2 = DriverDataCatalogue(base_url2)
        self.assertEqual(dc2.base_url, base_url2)

    def test_request_ckan(self):

        registry = RequestsDataCatalogue(REGISTRY_BASE_URL)

        url1 = REGISTRY_BASE_URL + 'package_list'
        result1 = registry.request_ckan(url1)
        self.assertIsInstance(result1, list)

        url2 = REGISTRY_BASE_URL + 'package_lists'
        with self.assertRaises(AssertionError) as ae2:
            result2 = registry.request_ckan(url2)
        self.assertEqual(str(ae2.exception), 
                        'Request Error:\nUnexpected status code: 400')

        url3 = 'https://open.canada.ca/data/thisisatest'
        with self.assertRaises(AssertionError) as ae3:
            result3 = registry.request_ckan(url3)
        self.assertEqual(str(ae3.exception), 
                        'Request Error:\nUnexpected status code: 404')

        url4 = REGISTRY_BASE_URL + 'dashboard_activity_list'
        with self.assertRaises(AssertionError) as ae4:
            result4 = registry.request_ckan(url4)
        self.assertEqual(str(ae4.exception), 
                        'Request Error:\nUnexpected status code: 403')

    def test_list_datasets(self):
        registry = RequestsDataCatalogue(REGISTRY_BASE_URL)
        datasets = registry.list_datasets()
        self.assertIsInstance(datasets, list)
        self.assertGreaterEqual(len(datasets), 41000)

    def test_get_dataset(self):

        registry = RequestsDataCatalogue(REGISTRY_BASE_URL)

        id1 = '000bb94e-d929-4214-8893-bb42b114b0c3'
        title1 = 'COVID-19: How to care at home for someone who has or may have been exposed'
        result1 = registry.get_dataset(id1)
        self.assertEqual(result1['id'], id1)
        self.assertEqual(result1['title'], title1)

        id2 = '3656b2ad-8cf1-4241-8b58-e20154ac2037'
        title2 = 'Notices Softwood Lumber Exports to the United States: Export Allocation Methodologies'
        result2 = registry.get_dataset(id2)
        self.assertEqual(result2['id'], id2)
        self.assertEqual(result2['title'], title2)

    def test_search_datasets(self):

        registry = RequestsDataCatalogue(REGISTRY_BASE_URL)
        
        datasets1 = registry.search_datasets(date_published='"2013-03-21%2000:00:00"')
        self.assertEqual(len(datasets1), 4)
        for ds in datasets1:
            record = registry.get_dataset(ds)
            self.assertEqual(record['date_published'], "2013-03-21 00:00:00")


        datasets2 = registry.search_datasets(metadata_created='"2023-03-08T19:28:22.318687Z"')
        self.assertEqual(len(datasets2), 1)
        for ds in datasets2:
            record = registry.get_dataset(ds)
            self.assertEqual(record['metadata_created'], "2023-03-08T19:28:22.318687")
    
    def test_get_resource(self):

        registry = RequestsDataCatalogue(REGISTRY_BASE_URL)

        id1 = 'b3146b7c-5809-4cf9-b8dc-ced9ea3167ff'
        name1 = 'Data Product Specification (French)'
        result1 = registry.get_resource(id1)
        self.assertEqual(result1['id'], id1)
        self.assertEqual(result1['name'], name1)

        id2 = '5e09b65b-04ae-4008-80f6-b21be4143703'
        name2 = 'Notices: Item 5203: Sugar-Containing Products Serial No. 166 - 2009-08-20'
        result2 = registry.get_resource(id2)
        self.assertEqual(result2['id'], id2)
        self.assertEqual(result2['name'], name2)
            
if __name__ == '__main__':
    unittest.main()