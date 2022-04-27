import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import weather
from pandas.api.types import CategoricalDtype
import re 
import datetime
import icon_data
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import locale
from datetime import datetime as dt2
st.set_page_config(layout="wide",page_title="Güneş Enerjisi Üretim Tahmini",)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css("style.css")

#locale.setlocale(locale.LC_ALL, "tr_TR")
with st.sidebar:

    sehir = st.radio(
     "Şehir:",
     ('İstanbul',"Ankara","İzmir"))
    st.markdown("<br>",unsafe_allow_html=True)
    scol1, scol2 = st.columns(2)
    if sehir == "İstanbul":
        sehir_ad = "Istanbul"
        lat = 41.0122
        lon = 28.976
    elif sehir == "İzmir":
        sehir_ad = "Izmir"
        lat = 38.4333
        lon =27.15
    else:
        sehir_ad="Ankara"
        lat = 39.925533
        lon = 32.8543
    
    sonuc = weather.predict(sehir_ad,lat,lon)
    sonuc.to_csv(""+sehir_ad+"_weather.csv", index=False)
    
    df = pd.read_csv(""+sehir_ad+"_weather.csv")
    
    icono_df_dort = icon_data.cevir(sehir_ad,lat,lon)
    icono_df_dort.to_csv(""+sehir_ad+"_icon.csv", index=False)
    icono_df_dort = pd.read_csv(""+sehir_ad+"_icon.csv")
    
    sicaklik = df["AirTemperature"][161:162].round(1).to_string(index=False)
    durum = weather.main(icono_df_dort["main"][161:162].to_string(index=False))
    resim = weather.icon(icono_df_dort["icon"][161:162].to_string(index=False))
    with scol1:
        st.markdown("<p style='text-align: right; color: #ec6e4c;font-size: 23px;font-weight:bold ;margin-right:10px'>Hava</p>", unsafe_allow_html=True)
        image = Image.open('images/'+resim+'.png')
        st.image(image,use_column_width="auto")
        st.markdown("<p style='text-align: center; color: #31333f;font-size: 22px;font-weight:bold ;margin-top:-25px'>"+durum+"</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: right;color: #31333f;font-size: 13px ;'>Son Güncelleme</p>", unsafe_allow_html=True)
    with scol2:

        st.markdown("<p style='text-align: left; color: #ec6e4c;font-size: 23px;font-weight:bold ;margin-left:-20px'>Durumu</p>", unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #31333f;font-size: 22px;font-weight:bold ;margin-top:10px'>"+str(sehir)+"</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #31333f;font-size: 22px;font-weight:bold ;margin-top:5px'>"+sicaklik+" °C</p>", unsafe_allow_html=True)
        
        saat = str(dt2.now().strftime("%H"))
        st.markdown("<p style='text-align: left;color: #31333f;font-size: 13px ;margin-left:-5px'>"+saat+":00</p>", unsafe_allow_html=True)






       
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 250px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 250px;
        margin-left: -250px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown("<h1 style='text-align: center;margin-top: -100px; color: #31333f ;'>Güneş Enerji Santrali Üretim Tahmini</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
df['dt_obj'] = pd.to_datetime(df['dt_obj'], errors='coerce')
yedigun = df.groupby(df["dt_obj"][:163].dt.weekday).sum()
yedi = yedigun.reset_index()

ready = pd.read_csv("ready.csv")
ready["dt_obj"] = pd.to_datetime(ready["dt_obj"])


anlik = str(int(df[162:163]["Generation"].round(0)))
anlik2 = "{:,}".format(int(anlik))

gunluk = str(int(yedi["Generation"][6].round(0)))
gunluk2 = "{:,}".format(int(gunluk))

aylik = str(int(gunluk) * 22)
aylik2 = "{:,}".format(int(aylik))

yillik = int(aylik) * 32
yillik2 = "{:,}".format(yillik)

col1, col2, col3, col4 = st.columns(4)


with col1:
    
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 17px;font-weight:bold ;'>Anlık Üretim</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #31333f;font-size: 30px;font-weight:bold ;'>"+anlik2+" MW</p>", unsafe_allow_html=True)

with col2:
   
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 17px;font-weight:bold ;'>Günlük Üretim</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #31333f;font-size: 30px;font-weight:bold ;'>"+gunluk2+" MWh</p>", unsafe_allow_html=True)

with col3:
    
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 17px;font-weight:bold ;'>Aylık Üretim</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #31333f;font-size: 30px;font-weight:bold ;'>"+aylik2+" MWh</p>", unsafe_allow_html=True)

with col4:
    
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 17px;font-weight:bold ;'>Tüm Zamanlar Üretim</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #31333f;font-size: 30px;font-weight:bold ;'>"+yillik2+" MWh</p>", unsafe_allow_html=True)


st.markdown("<br><br><br>", unsafe_allow_html=True)

tahmin_title_1 = (datetime.date.today() - datetime.timedelta(days=0)).strftime("%d %B")
tahmin_title_2 = (datetime.date.today() + datetime.timedelta(days=3)).strftime("%d %B")
st.markdown("<p style='text-align: center; color: #31333f;font-size: 2.25rem;font-weight:bold ;'>4 Günlük Tahmini Üretim ("+tahmin_title_1+" - "+tahmin_title_2+")</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

colon0, colon1, colon2, colon3, colon4, colon5,  = st.columns([2,1,1,1,1,2])

#df['dt_obj'] = pd.to_datetime(df['dt_obj'], errors='coerce')

cats = [ 'Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
cat_type = CategoricalDtype(categories=cats, ordered=True)

dort_gun = df.groupby(df["dt_obj"][120:].dt.day_name().sum()
dort = dort_gun.reset_index()
dort['dt_obj'] = dort['dt_obj'].astype(cat_type)
dort_g = dort.sort_values(by="dt_obj").reset_index(drop=True)





gun_tahmin1 = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%A")
uretim_tahmin1 = int(dort_g["Generation"][dort_g["dt_obj"]==gun_tahmin1])
durum_tahmin1= weather.main(icono_df_dort["main"][120:][icono_df_dort["day"]==gun_tahmin1][12:13].to_string(index=False))
resim_tahmin1 = weather.icon(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin1][12:13].to_string(index=False))
with colon1:
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun_tahmin1), unsafe_allow_html=True)
    image = Image.open('images/'+resim_tahmin1+'.png')
    st.image(image,use_column_width=True,caption="{}".format(durum_tahmin1))
    st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} MWh</p>".format(uretim_tahmin1), unsafe_allow_html=True)

gun_tahmin2 = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%A")
uretim_tahmin2 = int(dort_g["Generation"][dort_g["dt_obj"]==gun_tahmin2])
durum_tahmin2= weather.main(icono_df_dort["main"][120:][icono_df_dort["day"]==gun_tahmin2][12:13].to_string(index=False))
resim_tahmin2 = weather.icon(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin2][12:13].to_string(index=False))
with colon2:
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun_tahmin2), unsafe_allow_html=True)
    image = Image.open('images/'+resim_tahmin2+'.png')
    st.image(image,use_column_width=True,caption="{}".format(durum_tahmin2))
    st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} MWh</p>".format(uretim_tahmin2), unsafe_allow_html=True)

gun_tahmin3 = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%A")
uretim_tahmin3 = int(dort_g["Generation"][dort_g["dt_obj"]==gun_tahmin3])
durum_tahmin3= weather.main(icono_df_dort["main"][120:][icono_df_dort["day"]==gun_tahmin3][12:13].to_string(index=False))
resim_tahmin3 = weather.icon(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin3][12:13].to_string(index=False))
with colon3:
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun_tahmin3), unsafe_allow_html=True)
    image = Image.open('images/'+resim_tahmin3+'.png')
    st.image(image,use_column_width=True,caption="{}".format(durum_tahmin3))
    st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} MWh</p>".format(uretim_tahmin3), unsafe_allow_html=True)

gun_tahmin4 = (datetime.date.today() + datetime.timedelta(days=3)).strftime("%A")
uretim_tahmin4 = int(dort_g["Generation"][dort_g["dt_obj"]==gun_tahmin4])
durum_tahmin4= weather.main(icono_df_dort["main"][120:][icono_df_dort["day"]==gun_tahmin4][12:13].to_string(index=False))
resim_tahmin4 = weather.icon(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin4][12:13].to_string(index=False))
with colon4:
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun_tahmin4), unsafe_allow_html=True)
    image = Image.open('images/'+resim_tahmin4+'.png')
    st.image(image,use_column_width=True,caption="{}".format(durum_tahmin4))
    st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} MWh</p>".format(uretim_tahmin4), unsafe_allow_html=True)







######################################################
son_7_title1 = (datetime.date.today() - datetime.timedelta(days=6)).strftime("%d %B")
son_7_title2 = (datetime.date.today() - datetime.timedelta(days=0)).strftime("%d %B")
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #31333f;font-size: 2.25rem;font-weight:bold ;'>Son 7 Gün Üretim ("+son_7_title1+" - "+son_7_title2+")</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)




colo1, colo2, colo3, colo4, colo5, colo6, colo7 = st.columns(7)

uretim1 = int(yedi["Generation"][0].round(0))
gun1= "Pazartesi"   
durum1= weather.main(icono_df_dort["main"][:163][icono_df_dort["day"]==gun1][12:13].to_string(index=False))
resim1 = weather.icon(icono_df_dort["icon"][:163][icono_df_dort["day"]==gun1][12:13].to_string(index=False))
with colo1:
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun1), unsafe_allow_html=True)
    image = Image.open('images/'+resim1+'.png')
    st.image(image,use_column_width=True,caption="{}".format(durum1))
    st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} MWh</p>".format(uretim1), unsafe_allow_html=True)

uretim2 = int(yedi["Generation"][1].round(0))
gun2= "Salı"
durum2= weather.main(icono_df_dort["main"][:163][icono_df_dort["day"]==gun2][12:13].to_string(index=False))
resim2 = weather.icon(icono_df_dort["icon"][:163][icono_df_dort["day"]==gun2][12:13].to_string(index=False))
with colo2:
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun2), unsafe_allow_html=True)
    image = Image.open('images/'+resim2+'.png')
    st.image(image,use_column_width=True,caption="{}".format(durum2))
    st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} MWh</p>".format(uretim2), unsafe_allow_html=True)

uretim3 = int(yedi["Generation"][2].round(0))
gun3= "Çarşamba"
durum3= weather.main(icono_df_dort["main"][:163][icono_df_dort["day"]==gun3][12:13].to_string(index=False))
resim3 = weather.icon(icono_df_dort["icon"][:163][icono_df_dort["day"]==gun3][12:13].to_string(index=False))
with colo3:
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun3), unsafe_allow_html=True)
    image = Image.open('images/'+resim3+'.png')
    st.image(image,use_column_width=True,caption="{}".format(durum3))
    st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} MWh</p>".format(uretim3), unsafe_allow_html=True)

uretim4 = int(yedi["Generation"][3].round(0))
gun4= "Perşembe"
durum4= weather.main(icono_df_dort["main"][:163][icono_df_dort["day"]==gun4][12:13].to_string(index=False))
resim4 = weather.icon(icono_df_dort["icon"][:163][icono_df_dort["day"]==gun4][12:13].to_string(index=False))
with colo4:
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun4), unsafe_allow_html=True)
    image = Image.open('images/'+resim4+'.png')
    st.image(image,use_column_width=True,caption="{}".format(durum4))
    st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} MWh</p>".format(uretim4), unsafe_allow_html=True)

uretim5 = int(yedi["Generation"][4].round(0))
gun5= "Cuma"
durum5= weather.main(icono_df_dort["main"][:163][icono_df_dort["day"]==gun5][12:13].to_string(index=False))
resim5 = weather.icon(icono_df_dort["icon"][:163][icono_df_dort["day"]==gun5][12:13].to_string(index=False))
with colo5:
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun5), unsafe_allow_html=True)
    image = Image.open('images/'+resim5+'.png')
    st.image(image,use_column_width=True,caption="{}".format(durum5))
    st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} MWh</p>".format(uretim5), unsafe_allow_html=True)

uretim6 = int(yedi["Generation"][5].round(0))
gun6= "Cumartesi"
durum6= weather.main(icono_df_dort["main"][:163][icono_df_dort["day"]==gun6][12:13].to_string(index=False))
resim6 = weather.icon(icono_df_dort["icon"][:163][icono_df_dort["day"]==gun6][12:13].to_string(index=False))
with colo6:
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun6), unsafe_allow_html=True)
    image = Image.open('images/'+resim6+'.png')
    st.image(image,use_column_width=True,caption="{}".format(durum6))
    st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} MWh</p>".format(uretim6), unsafe_allow_html=True)

uretim7 = int(yedi["Generation"][6].round(0))
gun7= "Pazar"
durum7= weather.main(icono_df_dort["main"][:163][icono_df_dort["day"]==gun7][12:13].to_string(index=False))
resim7 = weather.icon(icono_df_dort["icon"][:163][icono_df_dort["day"]==gun7][12:13].to_string(index=False))
with colo7:
    st.markdown("<p style='text-align: center; color: #ec6e4c;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun7), unsafe_allow_html=True)
    image = Image.open('images/'+resim7+'.png')
    st.image(image,use_column_width=True,caption="{}".format(durum7))
    st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} MWh</p>".format(uretim7), unsafe_allow_html=True)


######################################################

st.markdown("<br><br><br>",unsafe_allow_html=True)




ready["Generation"][25560:26303] = ready["Generation"][17544:18286]
aylik2019 = ready.groupby(ready["dt_obj"][ready["year"] == 2019].dt.month).sum()
aylik2020 = ready.groupby(ready["dt_obj"][ready["year"] == 2020].dt.month).sum()
aylik2021 = ready.groupby(ready["dt_obj"][ready["year"] == 2021].dt.month).sum()
months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
          'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
fig = go.Figure()
fig.add_trace(go.Bar(
    x=months,
    y=aylik2019["Generation"],
    name='2019',
    marker_color='#ec6e4c'
))
fig.add_trace(go.Bar(
    x=months,
    y=aylik2020["Generation"],
    name='2020',
    marker_color='#4c79ec'
))
fig.add_trace(go.Bar(
    x=months,
    y=aylik2021["Generation"],
    name='2021',
    marker_color='#4cecbf'
))
# Here we modify the tickangle of the xaxis, resulting in rotated labels.
fig.update_layout(
    font=dict(
        #family="sans-serif",
        size=18,
        color="#000000"
    ),barmode='group', 
    xaxis_tickangle=0,
    xaxis_title='Aylar',
    yaxis_title='Üretim (MWh)',
    height=500,
    width=1100, 
    title=dict(
        text='<b>Aylık Üretim (MWh)</b>',
        x=0.5,
        y=0.95,
        font=dict(
            #family="Arial",
            size=35,
            color='#31333f'
        ))
        ,uniformtext_minsize=35)
st.plotly_chart(fig)



#locale.setlocale(locale.LC_TIME, 'tr_TR')
#df["dt_obj"] = pd.to_datetime(df["dt_obj"])

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df["dt_obj"][:162], y=df["Generation"][:162], name='Geçmiş<br>Üretim',
                         line=dict(color='#ec6e4c', width=4)))

fig2.add_trace(go.Scatter(x=df["dt_obj"][161:], y=df["Generation"][161:], name='Tahmini<br>Üretim',
                         line=dict(color='#4c79ec', width=4)))
 
fig2.update_xaxes(tickformat='%d %B')


fig2.update_layout(
    font=dict(
        #family="sans-serif",
        size=18,
        color="#000000"
    ), 
    xaxis_tickangle=0,
    xaxis_tickmode="linear", 
    xaxis_title='Günler',
    yaxis_title='Üretim (MWh)',
    height=500,
    width=1100, 
    title=dict(
        text='<b>Günlük Üretim (MWh)</b>',
        x=0.5,
        y=0.95,
        font=dict(
            #family="Arial",
            size=35,
            color='#31333f'
        ))
        ,uniformtext_minsize=35,
        legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))

st.plotly_chart(fig2)


st.markdown("""
            <style>
            
            footer {visibility: hidden;}
            </style>
            """, unsafe_allow_html=True) 
#MainMenu {visibility: hidden;}


    