import networkx as nx
import numpy as np
import pandas as pd

class Rates:
    def __init__(self, csv_file):
        self.banks_table = pd.read_csv(csv_file)

        self.banks_table['best_rate'] = self.banks_table.select_dtypes(np.number).max(axis=1)
        self.banks_table['best_bank'] = self.banks_table.select_dtypes(np.number).idxmax(axis=1)

        self.rates = pd.pivot_table(self.banks_table, index='source', 
            columns='target', values='best_rate')

        log_of_rates = -np.log(self.rates)
        self.rates_graph = nx.from_pandas_adjacency(log_of_rates, create_using=nx.DiGraph())

    def update_graph(self, updates):
        for update in updates:
            source, target, bank, new_rate = update['from'], update['to'], update['bank'], update['rate']
            self.banks_table.loc[(self.banks_table['source']==source) 
                & (self.banks_table['target']==target) , bank] = new_rate
    
    def _path_to_list_of_dicts(self, path):
        list_of_dicts = [{"from": currency, "to": next_currency, 
            "bank": self.banks_table.loc[(self.banks_table['source']==currency) 
                & (self.banks_table['target']==next_currency)]['best_bank'].to_list()[0]}
            for currency, next_currency in zip(path, path[1:])]
        return list_of_dicts

    def max_revenue(self, query_dict):
        source, target, amount = query_dict['from'], query_dict['to'], query_dict['amount']
        value, path = nx.single_source_bellman_ford(self.rates_graph, source, target)
        return self._path_to_list_of_dicts(path)

