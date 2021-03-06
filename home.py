from enum import auto
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
import awesome_streamlit as ast
from plotly.subplots import make_subplots
import streamlit.components.v1 as components


    
st.cache()

def write(): 
    
    components.html(
    f"""
        
        <script>
            window.parent.document.querySelector('section.main').scrollTo(0, 0);
        </script>
    """,
    height=0
)
    st.markdown("""
                <style>

                footer {visibility: hidden;}
                .e19lei0e1 {visibility: hidden;}
                
                </style>
                """, unsafe_allow_html=True) 
    #MainMenu {visibility: hidden;}

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

    local_css("style.css")

    #locale.setlocale(locale.LC_ALL, "en_US")

    with st.sidebar:

        day = int((datetime.date.today() - datetime.timedelta(days=1)).strftime("%w"))
        month_now = int(dt2.now().strftime("%m"))
        sehir_ad="Ankara"
        sehir=sehir_ad
        lat = 39.925533
        lon = 32.8543

        
        
        scol1, scol2 = st.columns(2)
        df = weather.predict(sehir_ad,lat,lon)
        icono_df_dort = icon_data.cevir(sehir_ad,lat,lon)
        

        sicaklik = df["AirTemperature"][161:162].round(1).to_string(index=False)
        durum = weather.iconmain(icono_df_dort["icon"][161:162].to_string(index=False)) 
        resim = weather.icon(icono_df_dort["icon"][161:162].to_string(index=False))
        
 
        with scol1:
            #st.markdown("<p style='text-align: right; color: #31333f;font-size: 23px;font-weight:bold ;margin-right:10px;'>Hava</p>", unsafe_allow_html=True)
            image = Image.open('images/'+resim+'.png')
            st.image(image,use_column_width="auto")
            st.markdown("<p style='text-align: center; color: #31333f;font-size: 1rem;font-weight:bold ;margin-top:-1rem'>"+durum+"</p>", unsafe_allow_html=True)
            
        with scol2:

            #st.markdown("<p style='text-align: left; color: #31333f;font-size: 23px;font-weight:bold ;margin-left:-20px;'>Durumu</p>", unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #31333f;font-size: 22px;font-weight:bold ;'>"+str(sehir)+"</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #31333f;font-size: 22px;font-weight:bold ;margin-top:1.5rem'>"+sicaklik+" ??C</p>", unsafe_allow_html=True)

            
            
        sscol1, sscol2 = st.columns(2)
        with sscol1:
            st.markdown("<p style='text-align: center; color: #7f8396; font-size: 13px; margin-right: -5px; margin-top: -10px; background:#f0f2f6'>Son G??ncelleme</p>", unsafe_allow_html=True)
        with sscol2:
            saat = str(dt2.now().strftime("%d/%m/%Y %H"))
            st.markdown("<p style='text-align: center; color: #7f8396; font-size: 13px; margin-left: -15px; margin-top: -10px; background-color:#f0f2f6'>"+saat+":00</p>", unsafe_allow_html=True)

        df['dt_obj'] = pd.to_datetime(df['dt_obj'], errors='coerce')
        
        cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        cat_type = CategoricalDtype(categories=cats, ordered=True)

        dort_gun = df.groupby(df["dt_obj"][120:].dt.day_name()).sum()
        dort = dort_gun.reset_index()
        dort['dt_obj'] = dort['dt_obj'].astype(cat_type)
        dort_g = dort.sort_values(by="dt_obj").reset_index(drop=True)

        yedigun = df.groupby(df["dt_obj"][:163].dt.weekday).sum()
        yedi = yedigun.reset_index()
        
        ready = pd.read_csv("ready.csv")
        ready["dt_obj"] = pd.to_datetime(ready["dt_obj"])
        ready["Generation"][25560:26303] = ready["Generation"][17544:18286]
        ready["month"] = ready["dt_obj"].dt.month

        anlik = str(int(df[162:163]["Generation"].round(0)))
        anlik2 = "{:,}".format(int(anlik))
 
        gunluk = str(int(yedi["Generation"][yedi["dt_obj"]==day].round(0)))
        gunluk2 = "{:,}".format(int(gunluk))

        ready_ay = round(int(float(ready["Generation"][ready["year"]==2021][ready["month"]==month_now].sum().round(0))),2)   
        aylik = str(int(gunluk) +ready_ay)  
        aylik2 = "{:,}".format(int(aylik))

        ready_yil = round(int(ready["Generation"][ready["year"]==2021].sum().round(0)),0)
        yillik = int(aylik)  + int(ready_yil)
        yillik2 = "{:,}".format(yillik)

        kapasite = (int(anlik) / 522) *100
        kapasite = round(kapasite,0)

        #st.markdown("<h1 style='background:white;text-align: center;font-size:19px ;margin-top: 0px;border-radius: 5% 5% 0% 0%;'><span style=' color: #31333f ;'>Mevcut Kapasite<br>522 MWp<br><br>Kapasite Kullan??m??<br>%"+str(kapasite)+"<span></h1>", unsafe_allow_html=True)
        #st.progress(kapasite/100)
        kapasiteright = kapasite/100
        
        kapasiteleft = 1-kapasiteright
        
        labels = ['Kullan??lan',"Bo??"]
        values = [kapasiteright, kapasiteleft]
 

        fig4 = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = kapasite,
        number= { 'suffix': "%" },
        
        mode = "gauge+number",
        
        
        gauge = {'axis': {'range': [0, 100]},
                 'bar': {'color': "#e08a12"},
                 }))
        
        fig4.update_layout(
            margin=dict(l=15, r=15, t=50, b=0),
            title_text = "<b>Anl??k Kapasite Kullan??m??</b>",
            title_x=0.5,
            showlegend=False,
            width=225,
            height=200,
             font=dict(
            family="Source Sans Pro",
            size=13,
            color="#31333f")
            
            ),
        st.plotly_chart(fig4)
#-----------------------------------------        
    """ fig4 = go.Figure(data=[go.Pie(labels=labels, values=values)])
        
        fig4.update_traces(hole=.7,textinfo='none',marker=dict(colors=['#e08a12','#FFFFFF']) )

        fig4.update_layout(
            margin=dict(l=0, r=0, t=40, b=0),
            title_text = "<b>Anl??k Kapasite Kullan??m??</b>",
            title_x=0.5,
            showlegend=False,
            width=210,
            height=200,
             font=dict(
        family="sans-serif",
        size=13, 
        color="#31333f"
    ),
            
            annotations=[dict(text="<b>%"+str(kapasite)+"</b>", x=0.5, y=0.5, font_size=25, showarrow=False)])
        st.subheader(" ")
        st.plotly_chart(fig4)
 """
#----------------------------------------

    st.markdown("<h1 style='text-align: center;margin-top: -8rem; color: #31333f ;'>Ankara 522 MW GES ??retim Tahmin ve Analizi</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.3rem;font-weight:bold ;'>Anl??k Tahmini ??retim</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #31333f;font-size: 1.8rem;font-weight:bold ;'>"+anlik2+" MW</p>", unsafe_allow_html=True)


    with col2:
    
        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.3rem;font-weight:bold ;'>D??n Toplam ??retim</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #31333f;font-size: 1.8rem;font-weight:bold ;'>"+gunluk2+" MWh</p>", unsafe_allow_html=True)


    with col3: 

        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.3rem;font-weight:bold ;'>2021 Ayl??k Ortalama ??retim</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #31333f;font-size: 1.8rem;font-weight:bold ;'>"+aylik2+" MWh</p>", unsafe_allow_html=True)

    with col4:

        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.3rem;font-weight:bold ;'>2021 Y??l?? Toplam ??retim</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #31333f;font-size: 1.8rem;font-weight:bold ;'>"+yillik2+" MWh</p>", unsafe_allow_html=True)


    st.markdown("<br><br><br>", unsafe_allow_html=True)

    tahmin_title_1gun = (datetime.date.today() - datetime.timedelta(days=0)).strftime("%d")
    tahmin_title_1ay = (datetime.date.today() - datetime.timedelta(days=0)).strftime("%B")
    tahmin_title_2gun = (datetime.date.today() + datetime.timedelta(days=3)).strftime("%d")
    tahmin_title_2ay = (datetime.date.today() + datetime.timedelta(days=3)).strftime("%B")
    st.markdown("<p style='text-align: center; color: #31333f;font-size: 2.1rem;font-weight:bold ;'>4 G??nl??k Tahmini ??retim ("+tahmin_title_1gun+" "+str(weather.aycevir(tahmin_title_1ay))+" - "+tahmin_title_2gun+" "+str(weather.aycevir(tahmin_title_2ay))+")</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    colon0, colon1, colon2, colon3, colon4, colon5,  = st.columns([2,1,1,1,1,2])

    #df['dt_obj'] = pd.to_datetime(df['dt_obj'], errors='coerce')

    #cats = [ 'Pazartesi', 'Sal??', '??ar??amba', 'Per??embe', 'Cuma', 'Cumartesi', 'Pazar']
    


    gun_tahmin1 = weather.cevir((datetime.date.today() + datetime.timedelta(days=0)).strftime("%A"))
    gun_tahmin1en = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%A")
    uretim_tahmin1 = int(dort_g["Generation"][dort_g["dt_obj"]==gun_tahmin1en])
    durum_tahmin1= weather.iconmain(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin1en][12:13].to_string(index=False))
    resim_tahmin1 = weather.icon(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin1en][12:13].to_string(index=False))
    with colon1:
        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size:  1.3rem;font-weight:bold ;'>{}</p>".format(gun_tahmin1), unsafe_allow_html=True)
        image = Image.open('images/'+resim_tahmin1+'.png')
        st.image(image,use_column_width=True,caption="{}".format(durum_tahmin1))
        st.markdown("<p style='text-align: center; color: black;font-size: 1.7rem;font-weight:bold ;'>{} MWh</p>".format(uretim_tahmin1), unsafe_allow_html=True)

    gun_tahmin2 = weather.cevir((datetime.date.today() + datetime.timedelta(days=1)).strftime("%A"))
    gun_tahmin2en = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%A")
    uretim_tahmin2 = int(dort_g["Generation"][dort_g["dt_obj"]==gun_tahmin2en])
    durum_tahmin2= weather.iconmain(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin2en][12:13].to_string(index=False))
    resim_tahmin2 = weather.icon(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin2en][12:13].to_string(index=False))
    with colon2:
        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.3rem;font-weight:bold ;'>{}</p>".format(gun_tahmin2), unsafe_allow_html=True)
        image = Image.open('images/'+resim_tahmin2+'.png')
        st.image(image,use_column_width=True,caption="{}".format(durum_tahmin2))
        st.markdown("<p style='text-align: center; color: black;font-size: 1.7rem;font-weight:bold ;'>{} MWh</p>".format(uretim_tahmin2), unsafe_allow_html=True)

    gun_tahmin3 = weather.cevir((datetime.date.today() + datetime.timedelta(days=2)).strftime("%A"))
    gun_tahmin3en = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%A") 
    uretim_tahmin3 = int(dort_g["Generation"][dort_g["dt_obj"]==gun_tahmin3en])
    durum_tahmin3= weather.iconmain(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin3en][12:13].to_string(index=False))
    resim_tahmin3 = weather.icon(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin3en][12:13].to_string(index=False))
    with colon3:
        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.3rem;font-weight:bold ;'>{}</p>".format(gun_tahmin3), unsafe_allow_html=True)
        image = Image.open('images/'+resim_tahmin3+'.png')
        st.image(image,use_column_width=True,caption="{}".format(durum_tahmin3))
        st.markdown("<p style='text-align: center; color: black;font-size: 1.7rem;font-weight:bold ;'>{} MWh</p>".format(uretim_tahmin3), unsafe_allow_html=True)

    gun_tahmin4 = weather.cevir((datetime.date.today() + datetime.timedelta(days=3)).strftime("%A"))
    gun_tahmin4en = (datetime.date.today() + datetime.timedelta(days=3)).strftime("%A")
    uretim_tahmin4 = int(dort_g["Generation"][dort_g["dt_obj"]==gun_tahmin4en])
    durum_tahmin4= weather.iconmain(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin4en][12:13].to_string(index=False))
    resim_tahmin4 = weather.icon(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin4en][12:13].to_string(index=False))
    with colon4:
        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.3rem;font-weight:bold ;'>{}</p>".format(gun_tahmin4), unsafe_allow_html=True)
        image = Image.open('images/'+resim_tahmin4+'.png')
        st.image(image,use_column_width=True,caption="{}".format(durum_tahmin4))
        st.markdown("<p style='text-align: center; color: black;font-size: 1.7rem;font-weight:bold ;'>{} MWh</p>".format(uretim_tahmin4), unsafe_allow_html=True)





    ######################################################
    son_7_title1gun = (datetime.date.today() - datetime.timedelta(days=6)).strftime("%d")
    son_7_title1ay = (datetime.date.today() - datetime.timedelta(days=6)).strftime("%B")
    son_7_title2gun = (datetime.date.today() - datetime.timedelta(days=0)).strftime("%d")
    son_7_title2ay = (datetime.date.today() - datetime.timedelta(days=0)).strftime("%B")
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #31333f;font-size: 2.1rem;font-weight:bold ;'>Son 7 G??n ??retim ("+son_7_title1gun+" "+str(weather.aycevir(son_7_title1ay))+" - "+son_7_title2gun+" "+str(weather.aycevir(son_7_title2ay))+")</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)




    colo1, colo2, colo3, colo4, colo5, colo6, colo7 = st.columns(7)

    uretim1 = int(yedi["Generation"][0].round(0))
    gun1en= "Monday" 
    gun1= "Pazartesi"   
    durum1= weather.iconmain(icono_df_dort["icon"][:175][icono_df_dort["day"]==gun1en][12:13].to_string(index=False))
    resim1 = weather.icon(icono_df_dort["icon"][:175][icono_df_dort["day"]==gun1en][12:13].to_string(index=False))
    with colo1:
        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.3rem;font-weight:bold ;'>{}</p>".format(gun1), unsafe_allow_html=True)
        image = Image.open('images/'+resim1+'.png')
        st.image(image,use_column_width=True,caption="{}".format(durum1))
        st.markdown("<p style='text-align: center; color: black;font-size: 1.7rem;font-weight:bold ;'>{} MWh</p>".format(uretim1), unsafe_allow_html=True)

    uretim2 = int(yedi["Generation"][1].round(0))
    gun2en= "Tuesday"   
    gun2= "Sal??"
    durum2= weather.iconmain(icono_df_dort["icon"][:175][icono_df_dort["day"]==gun2en][12:13].to_string(index=False))
    resim2 = weather.icon(icono_df_dort["icon"][:175][icono_df_dort["day"]==gun2en][12:13].to_string(index=False))
    with colo2:
        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.3rem;font-weight:bold ;'>{}</p>".format(gun2), unsafe_allow_html=True)
        image = Image.open('images/'+resim2+'.png')
        st.image(image,use_column_width=True,caption="{}".format(durum2))
        st.markdown("<p style='text-align: center; color: black;font-size: 1.7rem;font-weight:bold ;'>{} MWh</p>".format(uretim2), unsafe_allow_html=True)

    uretim3 = int(yedi["Generation"][2].round(0))
    gun3en= "Wednesday"
    gun3= "??ar??amba"
    durum3= weather.iconmain(icono_df_dort["icon"][:175][icono_df_dort["day"]==gun3en][12:13].to_string(index=False))
    resim3 = weather.icon(icono_df_dort["icon"][:175][icono_df_dort["day"]==gun3en][12:13].to_string(index=False))
    with colo3:
        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.3rem;font-weight:bold ;'>{}</p>".format(gun3), unsafe_allow_html=True)
        image = Image.open('images/'+resim3+'.png')
        st.image(image,use_column_width=True,caption="{}".format(durum3))
        st.markdown("<p style='text-align: center; color: black;font-size: 1.7rem;font-weight:bold ;'>{} MWh</p>".format(uretim3), unsafe_allow_html=True)

    uretim4 = int(yedi["Generation"][3].round(0))
    gun4en= "Thursday"
    gun4= "Per??embe"
    durum4= weather.iconmain(icono_df_dort["icon"][:175][icono_df_dort["day"]==gun4en][12:13].to_string(index=False))
    resim4 = weather.icon(icono_df_dort["icon"][:175][icono_df_dort["day"]==gun4en][12:13].to_string(index=False))
    with colo4:
        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.3rem;font-weight:bold ;'>{}</p>".format(gun4), unsafe_allow_html=True)
        image = Image.open('images/'+resim4+'.png')
        st.image(image,use_column_width=True,caption="{}".format(durum4))
        st.markdown("<p style='text-align: center; color: black;font-size: 1.7rem;font-weight:bold ;'>{} MWh</p>".format(uretim4), unsafe_allow_html=True)

    uretim5 = int(yedi["Generation"][4].round(0))
    gun5en= "Friday"
    gun5= "Cuma"
    durum5= weather.iconmain(icono_df_dort["icon"][:175][icono_df_dort["day"]==gun5en][12:13].to_string(index=False))
    resim5 = weather.icon(icono_df_dort["icon"][:175][icono_df_dort["day"]==gun5en][12:13].to_string(index=False))
    with colo5:
        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.3rem;font-weight:bold ;'>{}</p>".format(gun5), unsafe_allow_html=True)
        image = Image.open('images/'+resim5+'.png')
        st.image(image,use_column_width=True,caption="{}".format(durum5))
        st.markdown("<p style='text-align: center; color: black;font-size: 1.7rem;font-weight:bold ;'>{} MWh</p>".format(uretim5), unsafe_allow_html=True)

    uretim6 = int(yedi["Generation"][5].round(0))
    gun6en= "Saturday"
    gun6= "Cumartesi"
    durum6= weather.iconmain(icono_df_dort["icon"][:175][icono_df_dort["day"]==gun6en][12:13].to_string(index=False))
    resim6 = weather.icon(icono_df_dort["icon"][:175][icono_df_dort["day"]==gun6en][12:13].to_string(index=False))
    with colo6:
        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.3rem;font-weight:bold ;'>{}</p>".format(gun6), unsafe_allow_html=True)
        image = Image.open('images/'+resim6+'.png')
        st.image(image,use_column_width=True,caption="{}".format(durum6))
        st.markdown("<p style='text-align: center; color: black;font-size: 1.7rem;font-weight:bold ;'>{} MWh</p>".format(uretim6), unsafe_allow_html=True)

    uretim7 = int(yedi["Generation"][6].round(0))
    gun7en= "Sunday"
    gun7= "Pazar"
    durum7= weather.iconmain(icono_df_dort["icon"][:175][icono_df_dort["day"]==gun7en][12:13].to_string(index=False))
    resim7 = weather.icon(icono_df_dort["icon"][:175][icono_df_dort["day"]==gun7en][12:13].to_string(index=False))
    with colo7:
        st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.3rem;font-weight:bold ;'>{}</p>".format(gun7), unsafe_allow_html=True)
        image = Image.open('images/'+resim7+'.png')
        st.image(image,use_column_width=True,caption="{}".format(durum7))
        st.markdown("<p style='text-align: center; color: black;font-size: 1.7rem;font-weight:bold ;'>{} MWh</p>".format(uretim7), unsafe_allow_html=True)


    ######################################################

    st.markdown("<br><br><br>",unsafe_allow_html=True)

    #locale.setlocale(locale.LC_TIME, 'tr_TR')
    #df["dt_obj"] = pd.to_datetime(df["dt_obj"])

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df["dt_obj"][:162], y=df["Generation"][:162], name='Ge??mi?? ??retim',
                             line=dict(color='#e08a12', width=4)))

    fig2.add_trace(go.Scatter(x=df["dt_obj"][161:], y=df["Generation"][161:], name='Tahmini ??retim',
                             line=dict(color='#129be0', width=4)))
    
    fig2.update_xaxes(tickformat='%d %B')


    fig2.update_layout(
        margin=dict(l=0, r=0, t=80, b=0), 
        font=dict(
            #family="sans-serif",
            size=18,
            color="#000000"
        ), 
        #xaxis_tickangle="auto",
        xaxis_tickmode="linear", 
        xaxis_title='G??nler',
        yaxis_title='??retim (MWh)',
        height =350,
        title=dict(
            text='<b>G??nl??k ??retim (MWh)</b>',
            x=0.5,
            y=0.98,
            font=dict(
                #family="Arial",
                size=35,
                color='#31333f'
            ))
            ,
            legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
    ))
    
    st.plotly_chart(fig2,use_container_width=True)
    st.markdown("<br><br><br>",unsafe_allow_html=True)
    ready["Generation"][25560:26303] = ready["Generation"][17544:18286]
    aylik2019 = ready.groupby(ready["dt_obj"][ready["year"] == 2019].dt.month).sum()
    aylik2020 = ready.groupby(ready["dt_obj"][ready["year"] == 2020].dt.month).sum()
    aylik2021 = ready.groupby(ready["dt_obj"][ready["year"] == 2021].dt.month).sum()
    months = ['Ocak', '??ubat', 'Mart', 'Nisan', 'May??s', 'Haziran',
              'Temmuz', 'A??ustos', 'Eyl??l', 'Ekim', 'Kas??m', 'Aral??k']
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=aylik2019["Generation"],
        name='2019',
        marker_color='#e08a12'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=aylik2020["Generation"],
        name='2020',
        marker_color='#129be0'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=aylik2021["Generation"],
        name='2021',
        marker_color='#9b12e0'
    ))
    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(
        margin=dict(l=0, r=0, t=80, b=0),
        font=dict(
            #family="sans-serif",
            size=18,
            color="#000000"
        ),barmode='group', 
        #xaxis_tickangle=0,
        xaxis_title='Aylar',
        yaxis_title='??retim (MWh)',
        height =350,
        title=dict(
            text='<b>Ayl??k ??retim (MWh)</b>',
            x=0.5,
            y=0.95,
            font=dict(
                #family="Arial",
                size=35,
                color='#31333f'
            )),legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1
    )
            ,uniformtext_minsize=35)
    st.plotly_chart(fig,use_container_width=True)
    
    
                        







    
