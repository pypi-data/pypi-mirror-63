import logging

from broker.client import BrokerClient

if __name__ == '__main__':
    from broker import broker_log

    broker_log.setLevel(logging.DEBUG)
    broker_log.addHandler(logging.StreamHandler())

    proxies = {
        "http": "",
        "https": "",
    }

    entry_point = 'https://api.bhex.us/openapi/'  # input your broker api entry point
    b = BrokerClient(entry_point, api_key='J3UcHs0mbnMVlBCZLbyGHJsAUI4nfAdspmFaUcz19U42R4AnffXrfX9Jl2fbIgpd', secret='cB0fec8tUk18K3gvpU7387ZJZ4od9NYZbLU4lTJ8HROjku3VSlQgG5bix5BvA6F8', proxies=proxies)
    result = b.order_new(symbol='BTCUSDT', side='BUY', type='LIMIT', quantity='10', price='4000', timeInForce='GTC')
    print(result)


