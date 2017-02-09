import unittest

from boddle import boddle

from micro_url import api

class TestThings(unittest.TestCase):
    def testIndex(self):
        res = api.index()
        
        self.assertTrue('total' in res)
        self.assertTrue('data' in res)
    
    def testUrl(self):
        with boddle(method='post', params={'desktop' : 'blah'}):
            self.assertRaises(api.HTTPError, api.url)
        
        with boddle(method='post', json={'desktop' : 'example.com'}):
            res = api.url()
            self.assertTrue('shortened_url' in res)
            
    def testGetUrl(self):
        res_url = api.get_url('mydomain.com', '867nv')
        self.assertEqual(res_url, 'http://mydomain.com/867nv')

if __name__ == '__main__':
    unittest.main()