import pandas as pd
import json

sum_nTx = 0
for i in range(1,47):
    file_name = "D:\\download\coin\coin{}.json".format(i)
    with open(file_name, 'r') as file_data:
        line = file_data.readline()
        while line:
            data = json.loads(line)
            sum_nTx += int(data['nTx'])
            line = file_data.readline()

        file_data.close()
        print(sum_nTx)

# 9222178 transactions