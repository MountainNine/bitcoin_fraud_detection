import pandas as pd
import json
import matplotlib.pyplot as plt


def get_address():
    sum_nTx = 0
    address = set()

    for i in range(1, 47):
        file_name = "D:\\download\coin\coin{}.json".format(i)
        with open(file_name, 'r') as file_data:
            line = file_data.readline()
            while line:
                data = json.loads(line)
                for tx in data['tx']:
                    for vout in tx['vout']:
                        if vout['scriptPubKey']['type'] not in ('nulldata', 'nonstandard'):
                            address.update(vout['scriptPubKey']['addresses'])
                line = file_data.readline()

            file_data.close()
            print("coin{} Clear.".format(i))

    text_file = open('address.txt', 'w')
    for a in address:
        text_file.write(a + "\n")
    text_file.close()


def save_transaction():
    median_list = []
    nTx = []

    for i in range(1, 47):
        file_name = "D:\\download\coin\coin{}.json".format(i)
        with open(file_name, 'r') as file_data:
            line = file_data.readline()
            while line:
                data = json.loads(line)
                median_list.append(data['mediantime'])
                nTx.append(data['nTx'])
                line = file_data.readline()

            file_data.close()
            print("coin{} Clear".format(i))

    df_transaction = pd.DataFrame({'medianTime': median_list, 'nTx': nTx})
    df_transaction.to_csv('./transaction.csv', sep=',', na_rep='NaN')


def show_transaction():
    data = pd.read_csv("transaction.csv")
    x = data.get('medianTime')
    x = pd.to_datetime(x, unit='s')
    y = data.get('nTx')
    plt.bar(x, y, width=0.01)
    plt.show()


def save_user_data():
    import json
    import pandas as pd

    list_address = []

    for i in range(1, 47):
        file_name = "D:\\download\coin\coin{}.json".format(i)
        with open(file_name, 'r') as file_data:
            line = file_data.readline()
            while line:
                data = json.loads(line)
                for tx in data['tx']:
                    for vout in tx['vout']:
                        if vout['scriptPubKey']['type'] not in ('nulldata', 'nonstandard'):
                            list_address.append([vout['scriptPubKey']['addresses'], vout['value']])
                line = file_data.readline()

            file_data.close()
            print("coin{} Clear.".format(i))

    list_address_new = list(zip(map(lambda x: x[0][0], list_address), map(lambda x: x[1], list_address)))
    addresses = list(map(lambda x: x[0], list_address_new))
    values = list(map(lambda x: x[1], list_address_new))
    df_new = pd.DataFrame({'address': addresses, 'value': values})
    df_new.to_csv('./users.csv', sep=',', na_rep='NaN')


def group_user():
    import pandas as pd

    df = pd.read_csv("users.csv")
    grouped = df.groupby("address")
    df_new = grouped.agg(['count', 'sum', 'std'])
    df_new['value'].to_csv('./users_new.csv', sep=',', na_rep='NaN')


def visualize_user():
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    data = pd.read_csv("users_new_2.csv")
    sub_data = data[data['is_fraud'] == 1]
    sub_data_2 = data[data['is_fraud'] == 0]

    x = sub_data_2.get('count')
    y = sub_data_2.get('sum')
    x2 = sub_data.get('count')
    y2 = sub_data.get('sum')
    colors = np.where(data['is_fraud'] == 1, 'r', 'b')
    plt.scatter(x, y, s=9)
    plt.scatter(x2, y2, s=9)
    plt.yscale("log")
    plt.xscale("log")
    plt.show()


def get_abuse_address():
    import pandas as pd
    from bs4 import BeautifulSoup
    import requests
    import time
    import numpy as np

    abuse_addresses = set()

    for i in range(1, 2248):
        page = requests.get("https://www.bitcoinabuse.com/reports?page={}".format(i))
        soup = BeautifulSoup(page.content, "html.parser")
        for s in soup.select("div.col-xl-4 a"):
            abuse_addresses.append(s.contents[0])
        print("{} passed.".format(i))
        time.sleep(1)

    df = pd.DataFrame(abuse_addresses)
    df_address = pd.read_csv('users_new.csv', index_col=False)
    common_address = pd.merge(df, df_address, how='inner', left_on=0, right_on='address')
    df_address['is_fraud'] = np.where(df_address['address'].isin(common_address['address']), 1, 0)
    df_address.to_csv('users_new_2.csv', index=None)


def cluster():
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import time

    df = pd.read_csv('users_new_3.csv', index_col=False)
    list_km = pd.DataFrame(map(list, zip(df['count'], df['sum'])))

    km = KMeans(n_clusters=7).fit(list_km)
    pred = km.labels_

    plt.scatter(df['count'], df['sum'], s=9, c=pred)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

    df['is_suspicious'] = pred

    df.to_csv('users_new_3.csv', index=False)

# 9222178 transactions
# 10541781 addresses
# 유저 산점도 (코인 수, 거래 수를 축으로)
# medianTime별 거래 수 막대그래프
# abusing address 표시
# 1L5KGyo42cd1ecyuQ3eLtvBVJDYDrTvJen
