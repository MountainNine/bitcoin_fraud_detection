import pandas as pd
import json

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

# ========================================================================================

import json
import pandas as pd

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

# 9222178 transactions
# 10541781 addresses
# 유저 산점도 (코인 수, 거래 수를 축으로)
# medianTime별 거래 수 막대그래프
# abusing address 표시
