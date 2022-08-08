from matplotlib import pyplot as plt
from datetime import datetime
from requests import get

'The API KEY FROM ETHERSCAN'
API_KEY = "94DZF54GQTNRCT6CVDCXMHI67V7GZHFHYT"
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18

'''https://api.etherscan.io/api
   ?module=account
   &action=balance
   &address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
   &tag=latest
   &apikey=YourApiKeyToken
'''

'This is our URL'


def make_api_url(module, action, address, **kwargs):
    url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    return url


'FUNCTION that gets eth balance from adress'


def get_account_balance(address):
    balance_url = make_api_url("account", "balance", address, tag="latest")
    response = get(balance_url)
    data = response.json()

    value = int(data["result"]) / ETHER_VALUE
    return value


''' Get Transactions function'''


def get_transactions_graph(address):
    transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=10000,
                                    sort="asc")
    response = get(transactions_url)
    data = response.json()["result"]

    internal_tx_url = make_api_url("account", "txlistinternal", address, startblock=0, endblock=99999999, page=1,
                                   offset=10000, sort="asc")
    response2 = get(internal_tx_url)
    data2 = response2.json()["result"]

    data.extend(data2)
    data.sort(key=lambda x: int(x['timeStamp']))

    current_balance = 0
    balances = []
    times = []

    for tx in data:
        to = tx["to"]
        from_addr = tx["from"]
        value = int(tx["value"]) / ETHER_VALUE

        if "gasPrice" in tx:
            gas = int(tx["gasUsed"]) * int(tx["gasPrice"]) / ETHER_VALUE
        else:
            gas = int(tx["gasUsed"]) / ETHER_VALUE

        time = datetime.fromtimestamp(int(tx['timeStamp']))
        money_in = to.lower() == address.lower()

        if money_in:
            current_balance += value
        else:
            current_balance -= value + gas

        balances.append(current_balance)
        times.append(time)

    plt.plot(times, balances)
    plt.show()


''' GET TRANSACTIONS OVERTIME IN GRAPH'''


def get_transactions(address):
    get_transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1,
                                        offset=10000,
                                        sort="asc")
    response = get(get_transactions_url)
    data = response.json()["result"]

    for tx in data:
        to = tx['to']
        from_addr = tx['from']
        value = int(tx['value']) / ETHER_VALUE
        gas = int(tx["gasUsed"]) * int(tx["gasPrice"]) / ETHER_VALUE
        time = datetime.fromtimestamp(int(tx["timeStamp"]))
        print("***************")
        print("To:", to)
        print("From:", from_addr)
        print("Value:", value)
        print("Gas Cost:", gas)
        print("Time:", time)




def get_transactions_block(address,blockstart,blockend):
    get_transactions_url = make_api_url("account", "txlist", address, startblock=blockstart, endblock=blockend, page=1,
                                        offset=10000,
                                        sort="asc")
    response = get(get_transactions_url)
    data = response.json()["result"]

    for tx in data:
        to = tx['to']
        from_addr = tx['from']
        value = int(tx['value']) / ETHER_VALUE
        gas = int(tx["gasUsed"]) * int(tx["gasPrice"]) / ETHER_VALUE
        time = datetime.fromtimestamp(int(tx["timeStamp"]))
        print("***************")
        print("To:", to)
        print("From:", from_addr)
        print("Value:", value)
        print("Gas Cost:", gas)
        print("Time:", time)





'''  ***EXAMPLE***
address = "0x73bceb1cd57c711feac4224d062b0f6ff338501e"
print(get_account_balance('0xb794f5ea0ba39494ce839613fffba74279579268'))  '''

x = input(
    "***WELCOME TO MY APPLICATION*** Type a number 1)Check amount of ETH 2)Check all transactions 3)Wiew all transactions on the time chart 4)Check all transactions from startblock to end-block:")

if x == '1':
    adresa = input("Please write the wallet adress you want to check:")
    print("On your wallet you have...")
    print(get_account_balance(adresa))
    print("ETH")

elif x == '2':
    adresa = input("Please write the wallet adress that you want to check transactions:")
    print(get_transactions(adresa))
elif x == '3':
    adresa = input("Please write the wallet adress that you want to check transactions:")
    print(get_transactions_graph(adresa))

elif x == '4':
    adresa = input("Please write the wallet adress,start-block and the end-block:")
    startblock = input("Startblock:")
    endblock = input("Endblock:")
    print(get_transactions_block(adresa,startblock,endblock))
else:
    print("You can choose only between 1,2,3 or 4 ", x, "is not an option")
