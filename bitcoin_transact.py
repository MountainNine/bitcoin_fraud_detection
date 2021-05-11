import pandas as pd
import json

sum_nTx = 0
address = set()

for i in range(1,47):
    file_name = "D:\\download\coin\coin{}.json".format(i)
    with open(file_name, 'r') as file_data:
        line = file_data.readline()
        while line:
            data = json.loads(line)
            for tx in data['tx']:
                for vout in tx['vout']:
                    if vout['scriptPubKey']['type'] not in ('nulldata','nonstandard'):
                        address.update(vout['scriptPubKey']['addresses'])
            line = file_data.readline()

        file_data.close()
        print("coin{} Clear.".format(i))

text_file = open('address.txt', 'w')
for a in address:
    text_file.write(a + "\n")
text_file.close()
# 9222178 transactions
# 10541781 addresses