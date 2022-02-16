from venv import create
import pandas as pd
import requests
import matplotlib.pyplot as plt

URL = 'https://raw.githubusercontent.com/wiki/anuwatavis/agricultural-commodities-price/rubber_data/rubber_price_2022.json'

def get_rubber_data():
    response = requests.get(URL)
    response_data = response.json()
    data = response_data['data']
    df = pd.DataFrame.from_dict(data)
    return df

def create_line_chart(dataframe_input, label):
  latex_price = dataframe_input.loc[0:, ["date", label]]
  latex_price["date"] =  pd.to_datetime(latex_price['date'])
  latex_price['date'] = latex_price["date"].dt.strftime("%y-%m-%d")
  plt.figure(figsize=(10,5))
  plt.xticks(rotation=90)
  plt.plot(latex_price['date'], latex_price[label], label=label, marker='o')
  plt.legend()
  plt.savefig(f"../chart/{label}_rubber.svg")
	

if __name__ == '__main__':
	rubber_df = get_rubber_data()
	create_line_chart(rubber_df, 'latex_price')
	create_line_chart(rubber_df, 'raw_robber_price')
	print('DONE')
