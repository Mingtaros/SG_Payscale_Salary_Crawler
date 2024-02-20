import pandas as pd
import glob
import json

full_data = []

for filename in glob.glob('payscaleSpiderResult/*.json'):
    with open(filename, 'r') as f:
        content = json.load(f)
    
    # format salary
    for cont in content:
        print(cont)
        if type(cont["salary"]) == "str":
            print(cont["salary"])
        cont["salary"] = cont["salary"] / 12
    full_data.extend(content)

df = pd.DataFrame(full_data)
df.to_csv("CategoryIndustrySalary.csv", index=False)