import pandas as pd
import json

with open('D:\\download\coin\coin1.json', 'r') as file_data:
    line = file_data.readline()
    data = json.loads(line)

print(data['nTx'])