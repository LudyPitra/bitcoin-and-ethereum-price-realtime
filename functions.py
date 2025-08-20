import os
import requests
from dotenv import load_dotenv

load_dotenv()



def coin_price_consult(coin_name: str):

    url = 'https://api.coingecko.com/api/v3/simple/price'

    coin = coin_name

    params = {
        'ids': coin,
        'vs_currencies': 'usd'
    }

    headers = {
        'x-cg-demo-api-key': os.getenv('COINGECKO_API_KEY')
    }


    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
    except requests.HTTPError as error:
        print(f'{error}')
        result = None
    else:
        result = response.json()
        price = result[coin]['usd']
        return f'Current {coin.capitalize()} price is: ${price:,.2f} USD'
    
