import networkx as nx
import numpy as np
import pandas as pd

class Rates:
    """
    Class for handling exchange rates data and finding the best path for converting currency.
    """    
    def __init__(self, csv_file):
        """
        Initialize the class by reading the CSV file, creating a pivot table of the best exchange rates
        for each currency pair, and creating a directed graph of the rates using NetworkX library.
        
        Parameters
        ----------
        csv_file : str
            The filepath of the CSV file containing the exchange rates data.
        
        Attributes
        ----------
        banks_table : pandas DataFrame
            DataFrame containing the exchange rates data, with additional columns 
            for the best rate and best bank for each currency pair.
        rates : pandas DataFrame
            Pivot table of the best exchange rates for each currency pair.
        rates_graph : networkx.DiGraph
            Directed graph of the exchange rates, with the weights on the edges representing the 
            negative logarithm of the rates.
        """
        self.banks_table = pd.read_csv(csv_file)
        
        self._update_table_and_graph()

    def _update_table_and_graph(self):
        """
        Update the banks_table, rates, and rates_graph attributes based on the current data in the banks_table.
        
        Attributes
        ----------
        banks_table : pandas DataFrame
            DataFrame containing the exchange rates data, with additional columns 
            for the best rate and best bank for each currency pair. The banks_table attribute will be updated
            with the new exchange rates, updating the 'best_bank' and 'best_rate' columns
        rates : pandas DataFrame
            Pivot table of the best exchange rates for each currency pair. This attribute will be recreated 
            based on the updated banks_table attribute
        rates_graph : networkx.DiGraph
            Directed graph of the exchange rates, with the weights on the edges representing the 
            negative logarithm of the rates. This attribute will be recreated based on the updated 
            banks_table attribute
        """        
        self.banks_table['best_rate'] = self.banks_table.select_dtypes(np.number).drop(
            'best_rate', axis=1, errors='ignore').max(axis=1)
        self.banks_table['best_bank'] = self.banks_table.select_dtypes(np.number).drop(
            'best_rate', axis=1, errors='ignore').idxmax(axis=1)

        self.rates = pd.pivot_table(self.banks_table, index='source', 
            columns='target', values='best_rate')

        log_of_rates = -np.log(self.rates)
        self.rates_graph = nx.from_pandas_adjacency(log_of_rates, create_using=nx.DiGraph())
        
    def update_graph(self, updates):
        """
        Update the graph with new exchange rates from the updates list of dictionaries.
        
        Parameters
        ----------
        updates : list of dict
            A list of dictionaries containing the keys 'from', 'to', 'bank', and 'rate'.
        """        
        for update in updates:
            source, target, bank, new_rate = update['from'], update['to'], update['bank'], update['rate']
            self.banks_table.loc[(self.banks_table['source']==source) 
                & (self.banks_table['target']==target) , bank] = new_rate
            self._update_table_and_graph()
    
    def _path_to_list_of_dicts(self, path):
        """
        Helper method to convert the path returned by the bellman_ford algorithm to a list of dictionaries.
        
        Parameters
        ----------
        path : list
            A list of currencies representing a path in the graph.
        
        Returns
        -------
        list of dict
            A list of dictionaries, where each dictionary has the keys 'from', 'to', and 'bank'.
        """        
        list_of_dicts = [{"from": currency, "to": next_currency, 
            "bank": self.banks_table.loc[(self.banks_table['source']==currency) 
                & (self.banks_table['target']==next_currency),'best_bank'].iloc[0]}
            for currency, next_currency in zip(path, path[1:])]
        return list_of_dicts

    def max_revenue(self, query_dict):
        """
        Find the best path for converting a given amount of currency from one type to another according to the current rates.
        
        Parameters
        ----------
        query_dict : dict
            A dictionary containing the keys 'from', 'to', and 'amount'.
        
        Returns
        -------
        list of dict
            A list of dictionaries, where each dictionary has the keys 'from', 'to', and 'bank'.
        """        
        source, target, amount = query_dict['from'], query_dict['to'], query_dict['amount']
        try:
            value, path = nx.single_source_bellman_ford(self.rates_graph, source, target)
        except nx.NetworkXNoPath:
            return ""
        except nx.NetworkXUnbounded:
            print(f"found negative cycle: {nx.find_negative_cycle(self.rates_graph, source)}")
            return ""
        return self._path_to_list_of_dicts(path)

