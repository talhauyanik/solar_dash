def cevir(sehir_ad,lat,lon):
    import requests
    import calendar
    from datetime import datetime
    import pandas as pd
    date = datetime.now()
    end_unix_time = calendar.timegm(date.utctimetuple())
    start_unix_time = end_unix_time - 600000

    start_unix_time,end_unix_time

    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_now

    end_unix_time = str(end_unix_time)
    start_unix_time = str(start_unix_time)

    URL = "https://pro.openweathermap.org/data/2.5/forecast/hourly?q="+sehir_ad+"&appid=96510cf05767bf32f4b4163803254243&lang=tr&units=metric"
    URL2 = "http://history.openweathermap.org/data/2.5/history/city?lat="+str(lat)+"&lon="+str(lon)+"&type=hour&start="+start_unix_time+"&end="+end_unix_time+"&units=metric&appid=96510cf05767bf32f4b4163803254243"


    r = requests.get(url = URL)
    r2 = requests.get(url = URL2)

    data_now = r.json()
    data_hist = r2.json()

    data_date = pd.json_normalize(data_now)
    data_now["list"][0]["weather"]
    w_main = []
    w_icon = []
    w_date = []

    for i in range(len(data_now["list"])):
       w_main.append(data_now["list"][i]["weather"][0]["main"])
       w_icon.append(data_now["list"][i]["weather"][0]["icon"])
       w_date.append(data_now["list"][i]["dt_txt"])

    icon_df = pd.DataFrame(w_icon)
    icon_df = icon_df.rename(columns={0:"icon"})
    icon_df["main"] = w_main
    icon_df["date"] = w_date

    icon_df

    data_hist["list"][0]["weather"]
    wh_main = []
    wh_icon = []
    wh_date = []

    for i in range(len(data_hist["list"])):
      wh_main.append(data_hist["list"][i]["weather"][0]["main"])
      wh_icon.append(data_hist["list"][i]["weather"][0]["icon"])
      wh_date.append(data_hist["list"][i]["dt"])

    iconh_df = pd.DataFrame(wh_icon)
    iconh_df = iconh_df.rename(columns={0:"icon"})
    iconh_df["main"] = wh_main
    iconh_df["date"] = wh_date


    for i in range(len(iconh_df)):
      iconh_df["date"][i] = datetime.utcfromtimestamp(iconh_df["date"][i])

    iconh_df["date"] = pd.to_datetime(iconh_df["date"])
    iconh_df.date = iconh_df["date"].dt.tz_localize("utc").dt.tz_convert('Asia/Istanbul')
    iconh_df['date'] = iconh_df['date'].dt.strftime('%d-%m-%Y %H:%M:%S')
    iconh_df

    icono_df = pd.concat([iconh_df, icon_df]).reset_index()
    icono_df["date"] = pd.to_datetime(icono_df["date"])
    icono_df["day"] = pd.to_datetime(icono_df.date).dt.day_name()


    return icono_df
    


  

  