import logging
import time

from broker.client import BrokerContractClient
from broker.exceptions import BrokerRequestException, BrokerApiException

if __name__ == '__main__':
    from broker import broker_log

    broker_log.setLevel(logging.DEBUG)
    broker_log.addHandler(logging.StreamHandler())

    proxies = {
        "http": '',
        "https": '',
    }

    entry_point = 'https://api.bhex.us/openapi'  # enter your open api entry point

    b = BrokerContractClient(entry_point,
                             api_key='J3UcHs0mbnMVlBCZLbyGHJsAUI4nfAdspmFaUcz19U42R4AnffXrfX9Jl2fbIgpd',
                             secret='cB0fec8tUk18K3gvpU7387ZJZ4od9NYZbLU4lTJ8HROjku3VSlQgG5bix5BvA6F8',
                             proxies=proxies)
    b1 = BrokerContractClient(entry_point,
                              api_key='',
                              secret='',
                              proxies=proxies)

    try:
        cid = int(time.time()*1000)
        r = b.order_new(symbol='BTC0808', clientOrderId=cid, side='BUY_OPEN', orderType='LIMIT_FREE',
                        quantity='10', price='5381', leverage='5', timeInForce='GTC', triggerPrice=None)
        print(r)

        time.sleep(1)

        cid1 = int(time.time()*1000)
        r1 = b1.order_new(symbol='BTC0808', clientOrderId=cid1, side='SELL_OPEN', orderType='LIMIT_FREE',
                          quantity='10', price='5381', leverage='5', timeInForce='GTC', triggerPrice=None)
        print(r1)
    except BrokerRequestException as bre:
        logging.error(bre)
    except BrokerApiException as bae:
        logging.error(bae)
