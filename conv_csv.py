import pandas as pd
import glob
import json

full_data = []

for filename in glob.glob('payscaleSpiderResult/*.json'):
    with open(filename, 'r') as f:
        content = json.load(f)
    
    # format salary
    content["salary"] = content["salary"].replace("S$", '').replace("k", "000")
    content["salary"] = int(content["salary"]) / 12
    full_data.append(content)

df = pd.DataFrame(full_data)
df.to_csv("CategoryIndustrySalary.csv", index=False)