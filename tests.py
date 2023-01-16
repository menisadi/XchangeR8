import unittest
from XchangeR8 import Rates

class TestRates(unittest.TestCase):
    def setUp(self):
        self.rates = Rates('Data//test_rates.csv')
        self.given_rates = None

    def test_update_graph(self):
        # Test that TypeError: is raised if updates is not a list
        with self.assertRaises(TypeError):
            self.rates.update_graph({'from': 'Dollar', 'to': 'Euro', 'bank': 'XBank', 'rate': 0.9})
        
        # Test that KeyError is raised if any dictionary in updates is missing a key
        updates = [{'from': 'Dollar', 'to': 'Euro', 'bank': 'XBank'}, {'from': 'Euro', 'to': 'Yen', 'rate': 110.0}]
        with self.assertRaises(KeyError):
            self.rates.update_graph(updates)
        
        # Test that the graph is correctly updated
        updates = [{'from': 'Dollar', 'to': 'Euro', 'bank': 'WBank', 'rate': 0.78}, 
            {'from': 'Euro', 'to': 'Pound', 'bank': 'ZBank', 'rate': 0.5}]
        self.rates.update_graph(updates)
        self.assertEqual(self.rates.banks_table.loc[(self.rates.banks_table['source']=='Dollar') 
            & (self.rates.banks_table['target']=='Euro'), 'WBank'].iloc[0], 0.78)
        self.assertEqual(self.rates.banks_table.loc[(self.rates.banks_table['source']=='Euro') 
            & (self.rates.banks_table['target']=='Pound'), 'ZBank'].iloc[0], 0.5)

    def test_max_revenue(self):
        # Test that KeyError is raised if query_dict is missing a key
        with self.assertRaises(KeyError):
            self.rates.max_revenue({'from': 'Dollar', 'to': 'Euro'})
        
        # Test that the output is an empty string in the case that there is no path
        query = {'from': 'Dollar', 'to': 'Yen', 'amount': 300}
        expected_path = ""
        self.assertEqual(self.rates.max_revenue(query), expected_path)

        # Test that the output is right in the case of missing rates
        query = {'from': 'Yen', 'to': 'Shekel', 'amount': 1000}
        expected_path = [{'from': 'Yen', 'to': 'Shekel', 'bank': 'XBank'}]
        self.assertEqual(self.rates.max_revenue(query), expected_path)

        # Test that the output is the expected path
        query = {'from': 'Dollar', 'to': 'Pound', 'amount': 500}
        expected_path = [{'from': 'Dollar', 'to': 'Euro', 'bank': 'XBank'}, {'from': 'Euro', 'to': 'Pound', 'bank': 'YBank'}]
        self.assertEqual(self.rates.max_revenue(query), expected_path)
        
        # Update the rates and test if the path updates accordingly
        updates = [{'from': 'Dollar', 'to': 'Euro', 'bank': 'XBank', 'rate': 0.7}]
        self.rates.update_graph(updates)
        query = {'from': 'Dollar', 'to': 'Pound', 'amount': 500}
        expected_path = [{'from': 'Dollar', 'to': 'Pound', 'bank': 'WBank'}]
        self.assertEqual(self.rates.max_revenue(query), expected_path) 

    def test_flow(self):
        self.given_rates = Rates('Data//currency_graph.csv')
        list_of_queries = [
            {'from': 'Yen','to': 'Shekel','amount':1527},
            [{'from': 'Euro','to': 'Dollar','bank': 'WBank','rate': 0.35}],
            {'from': 'Yen','to': 'Shekel','amount':1527},
            {'from': 'Shekel','to': 'Ruble','amount':350},
            [{'from': 'Shekel','to': 'Ruble','bank': 'WBank','rate': 0.14}],
            {'from': 'Shekel','to': 'Ruble','amount':350},
            [{'from': 'Dollar','to': 'Ruble','bank': 'XBank','rate': 0.28}],
            {'from': 'Shekel','to': 'Ruble','amount':350},
            [{'from': 'Dollar','to': 'Ruble','bank': 'YBank','rate': 0.5}],
            {'from': 'Shekel','to': 'Ruble','amount':350}
        ]
        for query in list_of_queries:
                if isinstance(query, dict):
                    try:
                        self.given_rates.max_revenue(query)
                    except:
                        self.fail("max_revenue raised an exception")
                else:
                    try:
                        self.given_rates.update_graph(query)
                    except:
                        self.fail("update_graph raised an exception")


if __name__ == '__main__':
    unittest.main()
