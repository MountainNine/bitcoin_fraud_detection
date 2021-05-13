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
    import pandas as pd
    import json

    df = pd.read_csv("address.csv")

    for i in range(1, 47):
        file_name = "D:\\download\coin\coin{}.json".format(i)
        with open(file_name, 'r') as file_data:
            line = file_data.readline()
            while line:
                data = json.loads(line)
                for tx in data['tx']:
                    for vout in tx['vout']:
                        if vout['scriptPubKey']['type'] not in ('nulldata', 'nonstandard'):
                            address_row = df.loc[df['address'].values == vout['scriptPubKey']['addresses']]
                            address_row['transaction'] += 1
                            address_row['value'] += vout['value']
                            df.loc[df['address'].values == vout['scriptPubKey']['addresses']] = address_row
                print("line clear")
                line = file_data.readline()

            file_data.close()
            print("coin{} Clear.".format(i))

# 9222178 transactions
# 10541781 addresses
# 유저 산점도 (코인 수, 거래 수를 축으로)
# medianTime별 거래 수 막대그래프
# abusing address 표시
# 1L5KGyo42cd1ecyuQ3eLtvBVJDYDrTvJen
