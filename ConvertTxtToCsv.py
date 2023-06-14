import pandas as pd

df = pd.read_csv("./datasets/tcp.csv", sep=";")

df.to_csv("./datasets/tcp.csv", sep=',', encoding="UTF-8", index=False)
