import pandas as pd
import glob

files = glob.glob("data/*.csv")

df_list = []

for file in files:
    df = pd.read_csv(file)
    df_list.append(df)

combined_df = pd.concat(df_list)

pink_df = combined_df[combined_df["product"] == "Pink Morsel"]

pink_df["Sales"] = pink_df["quantity"] * pink_df["price"]

final_df = pink_df[["Sales", "date", "region"]]

final_df.to_csv("formatted_output.csv", index=False)

print("Data processing complete!")