import requests
import pandas as pd

BASE = "https://api.collegefootballdata.com"

def get_transfers(year=2023):
    url = f"{BASE}/player/transfer"
    params = {"year": year}
    data = requests.get(url, params=params).json()
    df = pd.DataFrame(data)

    df = df[[
        "playerName",
        "position",
        "originConference",
        "destinationConference"
    ]]

    df.columns = ["player", "position", "from_conf", "to_conf"]

    df["prev_snaps"] = 200
    df["years_exp"] = 2
    df["starter_prev"] = 0
    df["scheme_match"] = 0.75
    df["nil_bucket"] = "Mid"
    df["year1_snaps"] = 350

    return df

if __name__ == "__main__":
    df = get_transfers()
    df.to_csv("data/transfers.csv", index=False)
    print("Transfer data updated")

