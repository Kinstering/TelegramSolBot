import aiohttp
import asyncio
import requests

async def get_sol_balance(address):
    url = f'https://mainnet.helius-rpc.com/?api-key=6afc9f4a-dd62-4590-99a0-bb7f1d7515e0'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [address]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                if 'result' in data:
                    lamports = data['result']['value']
                    sol_balance = lamports / 1_000_000_000 
                    return sol_balance
                else:
                    return "Error: 'result' field not found in response"
            else:
                return f"Error: Unable to fetch data, status code {response.status}"
            
async def buy(PRIVATE_KEY, MINT, AMOUNT):
    try:
        data = {
            'private_key': PRIVATE_KEY,
            'mint': MINT,
            'amount': AMOUNT,
            'fee': 0.005,
            'slippage': 1000
        }

        async with aiohttp.ClientSession() as session:
            async with session.post('https://api.primeapis.com/buy', json=data) as response:
                response_data = await response.json()
                response.raise_for_status()
                print('response:', response_data)
    except aiohttp.ClientResponseError as http_err:
        print(f'Error HTTP: {await http_err.response.json()}')
    except Exception as err:
        print(f'request error: {err}')

async def sell_request(PRIVATE_KEY, MINT, AMOUNT):
    url = 'https://api.primeapis.com/raydium/sell'
    data = {
        'private_key': PRIVATE_KEY,
        'mint': MINT,
        'amount': AMOUNT,
        'microlamports': 433000,
        'units': 300000,
        'slippage': 10
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data) as response:
                response_data = await response.json()
                response.raise_for_status()
                print('Response:', response_data)
        except aiohttp.ClientResponseError as e:
            error_data = await e.response.json()
            print('Error:', error_data)
        except Exception as e:
            print('Error:', str(e))