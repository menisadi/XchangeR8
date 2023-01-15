from XchangeR8 import Rates

new_rates = Rates('Data\currency_graph.csv')

print(new_rates.banks_table)
print(new_rates.rates)

wish = {'from': 'Shekel', 'to': 'Dollar', 'amount': 100}
print(new_rates.max_revenue(wish))

flash_news = [{'from': 'Dollar','to': 'Euro','bank': 'YBank','rate': 0.9},
    {'from': 'Rupee','to': 'Shekel','bank': 'ZBank','rate': 0.041}]
new_rates.update_graph(flash_news)

# print(new_rates.banks_table.columns)
# print(set(new_rates.banks_table.columns))
print('\n')
print(new_rates.banks_table)
print(new_rates.rates)