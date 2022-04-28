def predict(sehir_ad,lat,lon):
    import requests
    import pandas as pd
    from datetime import datetime
    import calendar
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from astral import LocationInfo
    from astral.location import Location
    from astropy import coordinates as coord
    from astropy import units as u
    from astropy.time import Time

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

    w_df = data_now["list"]

    ww_code = []

    for i in range(len(data_now["list"])):
       ww_code.append(data_now["list"][i]["weather"][0]["id"])

    w_df = pd.json_normalize(w_df)

    n = w_df.columns[1]
    w_df.drop(["weather", "dt","visibility","pop","main.temp_min","main.temp_max","main.pressure","main.sea_level","main.grnd_level","main.temp_kf","wind.gust","sys.pod"], axis = 1, inplace = True)
    w_df[n] = ww_code

    w_df["clouds.all"][(w_df["clouds.all"]< 11.11) & (w_df["clouds.all"] >= 0)] = 0
    w_df["clouds.all"][(w_df["clouds.all"]< 22.22) & (w_df["clouds.all"] >= 11.11)] = 1
    w_df["clouds.all"][(w_df["clouds.all"]< 33.33) & (w_df["clouds.all"] >= 22.22)] = 2
    w_df["clouds.all"][(w_df["clouds.all"]< 44.44) & (w_df["clouds.all"] >= 33.33)] = 3
    w_df["clouds.all"][(w_df["clouds.all"]< 55.55) & (w_df["clouds.all"] >= 44.44)] = 4
    w_df["clouds.all"][(w_df["clouds.all"]< 66.66) & (w_df["clouds.all"] >= 55.55)] = 5
    w_df["clouds.all"][(w_df["clouds.all"]< 77.77) & (w_df["clouds.all"] >= 66.66)] = 6
    w_df["clouds.all"][(w_df["clouds.all"]<= 88.88) & (w_df["clouds.all"] >= 77.77)] = 7
    w_df["clouds.all"][(w_df["clouds.all"]<= 100) & (w_df["clouds.all"] >=88.88)] = 8

    w_df["weather"][w_df["weather"] == 500] = 58
    w_df["weather"][w_df["weather"] == 200] = 91
    w_df["weather"][w_df["weather"] == 201] = 92
    w_df["weather"][w_df["weather"] == 202] = 94
    w_df["weather"][w_df["weather"] == 210] = 95
    w_df["weather"][w_df["weather"] == 211] = 17
    w_df["weather"][w_df["weather"] == 212] = 97
    w_df["weather"][w_df["weather"] == 221] = 98
    w_df["weather"][w_df["weather"] == 230] = 91
    w_df["weather"][w_df["weather"] == 231] = 92
    w_df["weather"][w_df["weather"] == 232] = 94

    w_df["weather"][w_df["weather"] == 300] = 50
    w_df["weather"][w_df["weather"] == 301] = 56
    w_df["weather"][w_df["weather"] == 302] = 54
    w_df["weather"][w_df["weather"] == 310] = 51
    w_df["weather"][w_df["weather"] == 311] = 58
    w_df["weather"][w_df["weather"] == 312] = 59
    w_df["weather"][w_df["weather"] == 313] = 54
    w_df["weather"][w_df["weather"] == 314] = 55
    w_df["weather"][w_df["weather"] == 321] = 57

    w_df["weather"][w_df["weather"] == 500] = 60
    w_df["weather"][w_df["weather"] == 501] = 62
    w_df["weather"][w_df["weather"] == 502] = 64
    w_df["weather"][w_df["weather"] == 503] = 63
    w_df["weather"][w_df["weather"] == 504] = 65
    w_df["weather"][w_df["weather"] == 511] = 66
    w_df["weather"][w_df["weather"] == 520] = 61
    w_df["weather"][w_df["weather"] == 521] = 63
    w_df["weather"][w_df["weather"] == 522] = 65
    w_df["weather"][w_df["weather"] == 531] = 64

    w_df["weather"][w_df["weather"] == 600] = 70
    w_df["weather"][w_df["weather"] == 601] = 72
    w_df["weather"][w_df["weather"] == 602] = 74
    w_df["weather"][w_df["weather"] == 611] = 83
    w_df["weather"][w_df["weather"] == 612] = 71
    w_df["weather"][w_df["weather"] == 613] = 73
    w_df["weather"][w_df["weather"] == 615] = 83
    w_df["weather"][w_df["weather"] == 616] = 84
    w_df["weather"][w_df["weather"] == 620] = 85
    w_df["weather"][w_df["weather"] == 621] = 86
    w_df["weather"][w_df["weather"] == 622] = 86

    w_df["weather"][w_df["weather"] == 701] = 10
    w_df["weather"][w_df["weather"] == 711] = 4
    w_df["weather"][w_df["weather"] == 721] = 5
    w_df["weather"][w_df["weather"] == 731] = 8
    w_df["weather"][w_df["weather"] == 741] = 28
    w_df["weather"][w_df["weather"] == 751] = 7
    w_df["weather"][w_df["weather"] == 761] = 7
    w_df["weather"][w_df["weather"] == 762] = 4
    w_df["weather"][w_df["weather"] == 771] = 18
    w_df["weather"][w_df["weather"] == 781] = 19

    w_df["weather"][w_df["weather"] == 800] = 0

    w_df["weather"][w_df["weather"] == 801] = 0
    w_df["weather"][w_df["weather"] == 802] = 1
    w_df["weather"][w_df["weather"] == 803] = 1
    w_df["weather"][w_df["weather"] == 804] = 2
    ##########################################


    w_df = w_df.rename(columns={"dt_txt":"DateTime",
                                "main.temp":"AirTemperature",
                                "main.feels_like":"ComfortTemperature",
                                "main.humidity":"RelativeHumidity",
                                "wind.speed":"WindSpeed",
                                "wind.deg":"WindDirection",
                                "weather":"WWCode",
                                "clouds.all":"EffectiveCloudCover"})


    w_df = w_df[["DateTime", "AirTemperature", "ComfortTemperature", "RelativeHumidity", "WindSpeed", "WindDirection", "WWCode", "EffectiveCloudCover"]]

    w_df["DateTime"] = pd.to_datetime(w_df["DateTime"])

    w_df.DateTime = w_df["DateTime"].dt.tz_localize("utc").dt.tz_convert('Asia/Istanbul')

    w_df['DateTime'] = w_df['DateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    sub_dates = w_df["DateTime"]
    sub_generation = np.zeros(len(w_df))

    list_of_tuples = list(zip(sub_dates, sub_generation))

    submission_df = pd.DataFrame(list_of_tuples,
                      columns = ['DateTime', 'Generation'])

    wh_df = data_hist["list"]

    wh_df = pd.json_normalize(wh_df)

    ww_code2 = []

    for i in range(len(data_hist["list"])):
       ww_code2.append(data_hist["list"][i]["weather"][0]["id"])

#rain.1h droplanacak olan kolon ismi
    col_index = wh_df.columns[1]
    wh_df.drop(["weather","main.temp_min","main.temp_max","main.pressure","wind.gust"], axis = 1, inplace = True)
    wh_df[col_index] = ww_code2

    wh_df["clouds.all"][(wh_df["clouds.all"]< 11.11) & (wh_df["clouds.all"] >= 0)] = 0
    wh_df["clouds.all"][(wh_df["clouds.all"]< 22.22) & (wh_df["clouds.all"] >= 11.11)] = 1
    wh_df["clouds.all"][(wh_df["clouds.all"]< 33.33) & (wh_df["clouds.all"] >= 22.22)] = 2
    wh_df["clouds.all"][(wh_df["clouds.all"]< 44.44) & (wh_df["clouds.all"] >= 33.33)] = 3
    wh_df["clouds.all"][(wh_df["clouds.all"]< 55.55) & (wh_df["clouds.all"] >= 44.44)] = 4
    wh_df["clouds.all"][(wh_df["clouds.all"]< 66.66) & (wh_df["clouds.all"] >= 55.55)] = 5
    wh_df["clouds.all"][(wh_df["clouds.all"]< 77.77) & (wh_df["clouds.all"] >= 66.66)] = 6
    wh_df["clouds.all"][(wh_df["clouds.all"]<= 88.88) & (wh_df["clouds.all"] >= 77.77)] = 7
    wh_df["clouds.all"][(wh_df["clouds.all"]<= 100) & (wh_df["clouds.all"] >=88.88)] = 8

    wh_df["weather"][wh_df["weather"] == 500] = 58
    wh_df["weather"][wh_df["weather"] == 200] = 91
    wh_df["weather"][wh_df["weather"] == 201] = 92
    wh_df["weather"][wh_df["weather"] == 202] = 94
    wh_df["weather"][wh_df["weather"] == 210] = 95
    wh_df["weather"][wh_df["weather"] == 211] = 17
    wh_df["weather"][wh_df["weather"] == 212] = 97
    wh_df["weather"][wh_df["weather"] == 221] = 98
    wh_df["weather"][wh_df["weather"] == 230] = 91
    wh_df["weather"][wh_df["weather"] == 231] = 92
    wh_df["weather"][wh_df["weather"] == 232] = 94

    wh_df["weather"][wh_df["weather"] == 300] = 50
    wh_df["weather"][wh_df["weather"] == 301] = 56
    wh_df["weather"][wh_df["weather"] == 302] = 54
    wh_df["weather"][wh_df["weather"] == 310] = 51
    wh_df["weather"][wh_df["weather"] == 311] = 58
    wh_df["weather"][wh_df["weather"] == 312] = 59
    wh_df["weather"][wh_df["weather"] == 313] = 54
    wh_df["weather"][wh_df["weather"] == 314] = 55
    wh_df["weather"][wh_df["weather"] == 321] = 57

    wh_df["weather"][wh_df["weather"] == 500] = 60
    wh_df["weather"][wh_df["weather"] == 501] = 62
    wh_df["weather"][wh_df["weather"] == 502] = 64
    wh_df["weather"][wh_df["weather"] == 503] = 63
    wh_df["weather"][wh_df["weather"] == 504] = 65
    wh_df["weather"][wh_df["weather"] == 511] = 66
    wh_df["weather"][wh_df["weather"] == 520] = 61
    wh_df["weather"][wh_df["weather"] == 521] = 63
    wh_df["weather"][wh_df["weather"] == 522] = 65
    wh_df["weather"][wh_df["weather"] == 531] = 64

    wh_df["weather"][wh_df["weather"] == 600] = 70
    wh_df["weather"][wh_df["weather"] == 601] = 72
    wh_df["weather"][wh_df["weather"] == 602] = 74
    wh_df["weather"][wh_df["weather"] == 611] = 83
    wh_df["weather"][wh_df["weather"] == 612] = 71
    wh_df["weather"][wh_df["weather"] == 613] = 73
    wh_df["weather"][wh_df["weather"] == 615] = 83
    wh_df["weather"][wh_df["weather"] == 616] = 84
    wh_df["weather"][wh_df["weather"] == 620] = 85
    wh_df["weather"][wh_df["weather"] == 621] = 86
    wh_df["weather"][wh_df["weather"] == 622] = 86

    wh_df["weather"][wh_df["weather"] == 701] = 10
    wh_df["weather"][wh_df["weather"] == 711] = 4
    wh_df["weather"][wh_df["weather"] == 721] = 5
    wh_df["weather"][wh_df["weather"] == 731] = 8
    wh_df["weather"][wh_df["weather"] == 741] = 28
    wh_df["weather"][wh_df["weather"] == 751] = 7
    wh_df["weather"][wh_df["weather"] == 761] = 7
    wh_df["weather"][wh_df["weather"] == 762] = 4
    wh_df["weather"][wh_df["weather"] == 771] = 18
    wh_df["weather"][wh_df["weather"] == 781] = 19

    wh_df["weather"][wh_df["weather"] == 800] = 0

    wh_df["weather"][wh_df["weather"] == 801] = 0
    wh_df["weather"][wh_df["weather"] == 802] = 1
    wh_df["weather"][wh_df["weather"] == 803] = 1
    wh_df["weather"][wh_df["weather"] == 804] = 2

    wh_df = wh_df.rename(columns={"dt":"DateTime",
                                "main.temp":"AirTemperature",
                                "main.feels_like":"ComfortTemperature",
                                "main.humidity":"RelativeHumidity",
                                "wind.speed":"WindSpeed",
                                "wind.deg":"WindDirection",
                                "weather":"WWCode",
                                "clouds.all":"EffectiveCloudCover"})


    wh_df = wh_df[["DateTime", "AirTemperature", "ComfortTemperature", "RelativeHumidity", "WindSpeed", "WindDirection", "WWCode", "EffectiveCloudCover"]]

    for i in range(len(wh_df)):
        a = wh_df["DateTime"][i] = datetime.utcfromtimestamp(wh_df["DateTime"][i]).strftime('%Y-%m-%d %H:%M:%S')

    wh_df["DateTime"] = pd.to_datetime(wh_df["DateTime"])

    wh_df.DateTime = wh_df["DateTime"].dt.tz_localize("utc").dt.tz_convert('Asia/Istanbul')

    wh_df['DateTime'] = wh_df['DateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    gen_dates = wh_df["DateTime"]
    gen_generation = np.zeros(len(wh_df))

    list_of_tupless = list(zip(gen_dates, gen_generation))

    gen_df = pd.DataFrame(list_of_tupless,
                      columns = ['DateTime', 'Generation'])

    temp_df = pd.concat([wh_df, w_df])

    temp_df["RelativeHumidity"] = temp_df["RelativeHumidity"].astype(float).interpolate(method='linear')
    temp_df["WindDirection"] = temp_df["WindDirection"].astype(float).interpolate(method='linear')
    temp_df["EffectiveCloudCover"] = temp_df["EffectiveCloudCover"].astype(float).interpolate(method='linear')
    whole_df = gen_df.merge(temp_df, how="left", on="DateTime")


    sun_df = temp_df.copy()

    sun_df["dt_obj"] = pd.to_datetime(sun_df.DateTime).dt.tz_localize('Europe/Istanbul')

    target_loc = LocationInfo(''+sehir_ad+'', 'Turkey', 'Europe/Istanbul', lat, lon)

    print("Calculating azimuth angle...")
    sun_df["sun_az_angle"] = sun_df["dt_obj"].apply(Location(target_loc).solar_azimuth)

    print("Calculating altitude angle...")
    sun_df["sun_alt_angle"] = sun_df["dt_obj"].apply(Location(target_loc).solar_elevation)

    # Resetting to UTC
    sun_df["dt_obj"] = pd.to_datetime(sun_df.DateTime)

    def get_sun_distance(sun_time):
        converted_sun_time = Time(sun_time - pd.DateOffset(hours=3))
        loc = coord.EarthLocation(lon * u.deg,
                                  lat * u.deg)

        altaz = coord.AltAz(location=loc, obstime=converted_sun_time)
        sun = coord.get_sun(converted_sun_time)
        transformed_params = sun.transform_to(altaz)

        return transformed_params.distance.AU

    print("Calculating sun distance...")
    sun_df["sun_distance"] = get_sun_distance(sun_df["dt_obj"])

    sun_df = sun_df[["DateTime", "sun_alt_angle", "sun_az_angle", "sun_distance"]].copy().reset_index(drop=True)

    print("Generated all sun features!")

    submission_whole_df = submission_df.merge(temp_df, how="left", on="DateTime")

    whole_stacked_df = pd.concat([whole_df, submission_whole_df], axis=0).reset_index(drop=True)
    whole_stacked_df = pd.concat([whole_stacked_df, sun_df.drop(labels=["DateTime"], axis=1)], axis=1)

    whole_stacked_df["dt_obj"] = pd.to_datetime(whole_stacked_df.DateTime)

    def fourier_ext(df, col, period, orders):
        for order in orders:
            df[col+'_sin'+str(order)] = np.sin(order * 2 * np.pi * df[col]/period) 
            df[col+'_cos'+str(order)] = np.cos(order * 2 * np.pi * df[col]/period) 


    whole_stacked_df["year"] = whole_stacked_df["dt_obj"].dt.year
    whole_stacked_df["yearday"] = whole_stacked_df["dt_obj"].dt.dayofyear
    whole_stacked_df["hour"] = whole_stacked_df["dt_obj"].dt.hour
    whole_stacked_df["week"] = whole_stacked_df["dt_obj"].dt.isocalendar().week

    whole_stacked_df.loc[whole_stacked_df['WWCode'] == 84, 'WWCode'] = 83 

    whole_stacked_df["WWCode"] = whole_stacked_df["WWCode"].astype(float).fillna(-100.)

    whole_stacked_df = whole_stacked_df[["dt_obj",
                       "Generation",
                       "yearday",
                       "year",
                       "hour",
                       "AirTemperature",
                       "ComfortTemperature",
                       "RelativeHumidity",
                       "WindSpeed",
                       "WindDirection",
                       "week",
                       "WWCode",
                       "sun_alt_angle",
                       "sun_az_angle",
                       "sun_distance",
                       "EffectiveCloudCover"
                      ]
                     ].copy()

    whole_stacked_df["solar_irradiance"] = (1+0.033*np.cos(2*np.pi*whole_stacked_df["yearday"]/365))
    whole_stacked_df.drop(labels=["yearday"], axis=1, inplace=True)

    whole_stacked_df["EffectiveCloudCover_r3mean"] = whole_stacked_df["EffectiveCloudCover"].rolling(3).mean()    
    whole_stacked_df["RelativeHumidity_r3mean"] = whole_stacked_df["RelativeHumidity"].rolling(3).mean()
    whole_stacked_df["AirTemperature_r3mean"] = whole_stacked_df["AirTemperature"].rolling(3).mean()

    fourier_ext(whole_stacked_df, "hour", 23, [1])

    for i in list(range(1,8)):
        for col in [
        "EffectiveCloudCover",
        "RelativeHumidity",
        "ComfortTemperature",
        "AirTemperature",
        "WWCode",
        ]:
            whole_stacked_df[col+str(i)] = whole_stacked_df[col].shift(-i)


    fourier_ext(whole_stacked_df, "WindDirection", 360, [1])   
    whole_stacked_df["WindSpeed_sin_component"] = whole_stacked_df["WindSpeed"] * whole_stacked_df["WindDirection_sin1"]
    whole_stacked_df["WindSpeed_cos_component"] = whole_stacked_df["WindSpeed"] * whole_stacked_df["WindDirection_cos1"]
    whole_stacked_df.drop(labels=["WindSpeed", "WindDirection"], axis=1, inplace=True)

    whole_stacked_df.set_index(whole_stacked_df["dt_obj"], inplace=True)
    whole_stacked_df["year"] = whole_stacked_df["year"].astype(np.int64)
    whole_stacked_df["week"] = whole_stacked_df["week"].astype(np.int64)

    training_index = (len(whole_stacked_df[:163]))
    training_df = whole_stacked_df[:163].copy().dropna().reset_index(drop=True)

    test_index = (whole_stacked_df[163:])
    test_df = whole_stacked_df[163:].copy().reset_index(drop=True)

    model_cols = list(training_df.columns)

    import joblib

    test_df["Generation"] = np.nan
    train_test_stacked_df = pd.concat([training_df, test_df], axis=0).reset_index(drop=True)


    my_model = joblib.load("my_model")

    preds = [my_model.predict(train_test_stacked_df[model_cols])]
    mean_preds = np.mean(preds, axis=0)

    train_test_stacked_df.loc[:, 'Generation'] = np.maximum(np.zeros(len(train_test_stacked_df)), mean_preds)


    nights = [20,21, 22 , 23 , 0, 1, 2, 3, 4, 5]
    for row_i, row in enumerate(train_test_stacked_df.Generation):
        if (train_test_stacked_df.hour.iloc[row_i] in nights) or (row < 0):
            train_test_stacked_df.loc[row_i, "Generation"] = 0

    train_test_stacked_df.loc[len(train_test_stacked_df)-6:len(train_test_stacked_df),"Generation"] = 0.

    submission_df["Generation"] = train_test_stacked_df["Generation"][163:].reset_index(drop=True)
    submission_df.fillna(0, inplace=True)

    
    return train_test_stacked_df

def main(main_name):
    
    if main_name == "Thunderstorm":
        return "Fırtınalı"
    elif main_name == "Drizzle":
        return "Hafif Yağmurlu"
    elif main_name == "Rain":
        return "Yağmurlu"
    elif main_name == "Snow":
        return "Karlı"
    elif main_name == "Clear":
        return "Güneşli"
    elif main_name == "Clouds":
        return "Bulutlu"

def icon(icon):
    if icon == "01d" or icon == "01n":
        return "clear"
    elif icon == "02d" or icon == "02n":
        return "few_clouds"
    elif icon == "03d" or icon == "03n":
        return "scattered_clouds"
    elif icon == "04d" or icon == "04n":
        return "broken_clouds"
    elif icon == "09d" or icon == "09n":
        return "shower_rain"
    elif icon == "10d" or icon == "10n":
        return "rain"
    elif icon == "11d" or icon == "11n":
        return "thunderstorm"
    elif icon == "13d" or icon == "13n":
        return "snow"
    elif icon == "50d" or icon == "50n":
        return "mist" 

def cevir(gun):
    
    if gun == "Monday":
        return "Pazartesi"
    elif gun == "Tuesday":
        return "Salı"
    elif gun == "Wednesday":
        return "Çarşamba"
    elif gun == "Thursday":
        return "Perşembe"
    elif gun == "Friday":
        return "Cuma"
    elif gun == "Saturday":
        return "Cumartesi"
    elif gun == "Sunday":
        return "Pazar"