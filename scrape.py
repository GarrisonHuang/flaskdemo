import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = "https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=9e565f9a-84dd-4e79-9097-d403cae1ea75&limit=1000&sort=datacreationdate desc&format=JSON"
six_countys = ["臺北市", "新北市", "桃園市", "臺中市", "臺南市", "高雄市"]
df = None


def get_six_pm25_json():
    columns, values = scrape_six_pm25()
    json_data = {"site": columns, "pm25": values}

    return json_data


def get_pm25_json():
    columns, values = scrape_pm25()

    xdata = [value[0] for value in values]
    ydata = [value[2] for value in values]

    datas = list(zip(xdata, ydata))

    datas = sorted(datas, key=lambda x: x[1])

    # print(datas)

    json_data = {"site": xdata, "pm25": ydata, "highest": datas[-1], "lowest": datas[0]}

    return json_data


def convert_value(value):
    try:
        return eval(value)
    except:
        return None


def get_pm25_data():
    global df
    if df is None:
        datas = requests.get(url).json()["records"]
        df = pd.DataFrame(datas)
        # 將非正常數值轉換成None
        df["pm25"] = df["pm25"].apply(convert_value)
        # 移除有None 的數據
        df = df.dropna()

    return df


def scrape_six_pm25():

    pm25 = []
    try:
        df = get_pm25_data()
        for county in six_countys:
            avg_pm25 = df.groupby("county").get_group(county)["pm25"].mean()
            pm25.append(round(avg_pm25, 2))
            # print(county, avg_pm25)

        columns = six_countys
        values = pm25

        return columns, values
    except Exception as e:
        print(e)

    return None, 404


def scrape_pm25(sort=False, ascending=True):
    try:
        df = get_pm25_data()
        if sort:
            df = df.sort_values("pm25", ascending=ascending)

        columns = df.columns
        values = df.values

        # columns = list(datas[0].keys())
        # values = [list(data.values()) for data in datas]
        return columns, values
    except Exception as e:
        print(e)

    return None, 404


def scrape_stocks():
    url = "https://histock.tw/%E5%9C%8B%E9%9A%9B%E8%82%A1%E5%B8%82"
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        trs = soup.find(string="今年以來").find_parent("div").find_all("tr")
        datas = []
        for tr in trs:
            data = []
            for th in tr.find_all("th"):
                data.append(th.text.strip())
            for td in tr.find_all("td"):
                data.append(td.text.strip())
            datas.append(data)
        return datas
    except Exception as e:
        print(e)

    return None


if __name__ == "__main__":
    # print(scrape_stocks())
    # print(scrape_pm25(sort=True, ascending=False))
    print(get_pm25_json())
