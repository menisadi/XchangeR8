import unittest
from XchangeR8 import Rates

class TestRates(unittest.TestCase):
    def setUp(self):
        self.rates = Rates('Data\currency_graph.csv')

    def test_update_graph(self):
        # Test that TypeError: is raised if updates is not a list
        with self.assertRaises(TypeError):
            self.rates.update_graph({'from': 'Dollar', 'to': 'Euro', 'bank': 'XBank', 'rate': 0.9})
        
        # Test that KeyError is raised if any dictionary in updates is missing a key
        updates = [{'from': 'Dollar', 'to': 'Euro', 'bank': 'XBank'}, {'from': 'Euro', 'to': 'Yen', 'rate': 110.0}]
        with self.assertRaises(KeyError):
            self.rates.update_graph(updates)
        
        # Test that the graph is correctly updated
        updates = [{'from': 'Dollar', 'to': 'Euro', 'bank': 'XBank', 'rate': 0.9}, {'from': 'Euro', 'to': 'Yen', 'bank': 'ZBank', 'rate': 110.0}]
        self.rates.update_graph(updates)
        self.assertEqual(self.rates.banks_table.loc[(self.rates.banks_table['source']=='Dollar') & (self.rates.banks_table['target']=='Euro'), 'XBank'].values[0], 0.9)
        self.assertEqual(self.rates.banks_table.loc[(self.rates.banks_table['source']=='Euro') & (self.rates.banks_table['target']=='Yen'), 'ZBank'].values[0], 110.0)

    def test_max_revenue(self):
        # Test that KeyError is raised if query_dict is missing a key
        with self.assertRaises(KeyError):
            self.rates.max_revenue({'from': 'Dollar', 'to': 'Euro'})
        
        # Test that the output is an empty string in the case that there is no path
        
        # Test that the output is the expected path
        # query = {'from': 'Dollar', 'to': 'Yen', 'amount': 1000}
        # expected_path = [{'from': 'Dollar', 'to': 'Euro', 'bank': 'XBank'}, {'from': 'Euro', 'to': 'Yen', 'bank': 'ZBank'}]
        # self.assertEqual(self.rates.max_revenue(query), expected_path)
        
    def test_flow(self):
        pass

if __name__ == '__main__':
    unittest.main()
