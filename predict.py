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


def write():
    
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
    koordinat = pd.read_csv("iller_koordinat.csv",sep=";")
    #locale.setlocale(locale.LC_ALL, "en_US")

    with st.sidebar:
        st.subheader(" ")
        with st.form("my_form"):
            st.write("Tahmini Üretim Hesaplama")
            sehir_ad = st.selectbox(
            'Şehir Seçin',
            ('Adana','Adıyaman','Afyonkarahisar','Ağrı','Aksaray','Amasya','Ankara','Antalya','Ardahan','Artvin','Aydın','Balıkesir','Bartın','Batman','Bayburt','Bilecik','Bingöl','Bitlis','Bolu','Burdur','Bursa','Çanakkale','Çankırı','Çorum','Denizli','Diyarbakır','Düzce','Edirne',
 'Elazığ',
 'Erzincan',
 'Erzurum',
 'Eskişehir',
 'Gaziantep',
 'Giresun',
 'Gümüşhane',
 'Hakkari',
 'Hatay',
 'Iğdır',
 'Isparta',
 'İstanbul',
 'İzmir',
 'Kahramanmaraş',
 'Karabük',
 'Karaman',
 'Kars',
 'Kastamonu',
 'Kayseri',
 'Kırıkkale',
 'Kırklareli',
 'Kırşehir',
 'Kilis',
 'Kocaeli',
 'Konya',
 'Kütahya',
 'Malatya',
 'Manisa',
 'Mardin',
 'Mersin',
 'Muğla',
 'Muş',
 'Nevşehir',
 'Niğde',
 'Ordu',
 'Osmaniye',
 'Rize',
 'Sakarya',
 'Samsun',
 'Siirt',
 'Sinop',
 'Sivas',
 'Şanlıurfa',
 'Şırnak',
 'Tekirdağ',
 'Tokat',
 'Trabzon',
 'Tunceli',
 'Uşak',
 'Van',
 'Yalova',
 'Yozgat',
 'Zonguldak'))
            kapasite = st.number_input("Kapasiteyi Girin (kW cinsinden)",min_value=0)
            

            # Every form must have a submit button.
            submitted = st.form_submit_button("Hesapla",)
    if submitted:
        month_now = int(dt2.now().strftime("%m"))
        month_name_now = dt2.now().strftime("%B")
        day = int(dt2.now().strftime("%w"))
        oran = float(kapasite / 522)
        
        lat = float(koordinat["lat"][koordinat["il"]==sehir_ad])
        lon = float(koordinat["lon"][koordinat["il"]==sehir_ad])
        pot = float(koordinat["pot"][koordinat["il"]==sehir_ad])

        #st.write(sehir_ad,lat,lon,pot,month_now,oran,day)    
        
        st.markdown("<h2 style='text-align: center;margin-top: -100px; color: #31333f ;'>"+sehir_ad+" "+str(kapasite)+" kWp Kapasite İçin Tahminler</h2>", unsafe_allow_html=True)
        st.subheader(" ")
        df = weather.predict(sehir_ad,lat,lon)
        yedigun = df.groupby(df["dt_obj"][:163].dt.weekday).sum()
        yedi = yedigun.reset_index()

        ready = pd.read_csv("ready.csv")
        ready["dt_obj"] = pd.to_datetime(ready["dt_obj"])
        ready["Generation"][25560:26303] = ready["Generation"][17544:18286]
        ready["month"] = ready["dt_obj"].dt.month

        anlik = str(round(int(df[162:163]["Generation"]*oran),3))
        anlik = "{:,}".format(int(anlik))

        gunluk = str(int(yedi["Generation"][yedi["dt_obj"]==day].round(0)*oran))
        gunluk2 = "{:,}".format(int(gunluk))

        ready_yil = round(int(ready["Generation"][ready["year"]==2021].sum().round(0)*pot*oran),0)
        yillik = int(ready_yil)
        yillik2 = "{:,}".format(yillik)

        ready_ay = ready_yil/12
        aylik = str(round(int(ready_ay),0))
        aylik2 = "{:,}".format(int(aylik))

        


        cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        cat_type = CategoricalDtype(categories=cats, ordered=True)
        dort_gun = df.groupby(df["dt_obj"][120:].dt.day_name()).sum()
        dort = dort_gun.reset_index()
        dort['dt_obj'] = dort['dt_obj'].astype(cat_type)
        dort_g = dort.sort_values(by="dt_obj").reset_index(drop=True)
        icono_df_dort = icon_data.cevir(sehir_ad,lat,lon)
        


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.25rem;font-weight:bold ;'>Anlık Üretim</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #31333f;font-size: 1.8rem;font-weight:bold ;'>"+anlik+" kW</p>", unsafe_allow_html=True)


        with col2:
        
            st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.25rem;font-weight:bold ;'>Bugün Toplam Üretim</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #31333f;font-size: 1.8rem;font-weight:bold ;'>"+gunluk2+" kWh</p>", unsafe_allow_html=True)


        with col3:

            st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.25rem;font-weight:bold ;'>Aylık Ortalama Üretim</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #31333f;font-size: 1.8rem;font-weight:bold ;'>"+aylik2+" kWh</p>", unsafe_allow_html=True)

        with col4:

            st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 1.25rem;font-weight:bold ;'>Yıllık Toplam Üretim</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #31333f;font-size: 1.8rem;font-weight:bold ;'>"+yillik2+" kWh</p>", unsafe_allow_html=True)

        st.markdown("<br><br><br>", unsafe_allow_html=True)

        tahmin_title_1gun = (datetime.date.today() - datetime.timedelta(days=0)).strftime("%d")
        tahmin_title_1ay = (datetime.date.today() - datetime.timedelta(days=0)).strftime("%B")
        tahmin_title_2gun = (datetime.date.today() + datetime.timedelta(days=3)).strftime("%d")
        tahmin_title_2ay = (datetime.date.today() + datetime.timedelta(days=3)).strftime("%B")
        st.markdown("<p style='text-align: center; color: #31333f;font-size: 2.25rem;font-weight:bold ;'>4 Günlük Tahmini Üretim ("+tahmin_title_1gun+" "+str(weather.aycevir(tahmin_title_1ay))+" - "+tahmin_title_2gun+" "+str(weather.aycevir(tahmin_title_2ay))+")</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        colon0, colon1, colon2, colon3, colon4, colon5,  = st.columns([2,1,1,1,1,2])

        gun_tahmin1 = weather.cevir((datetime.date.today() + datetime.timedelta(days=0)).strftime("%A"))
        gun_tahmin1en = (datetime.date.today() + datetime.timedelta(days=0)).strftime("%A")
        uretim_tahmin1 = round(float(dort_g["Generation"][dort_g["dt_obj"]==gun_tahmin1en]*oran),2)
        uretim_tahmin1 = "{:,}".format(int(uretim_tahmin1))
        durum_tahmin1= weather.main(icono_df_dort["main"][120:][icono_df_dort["day"]==gun_tahmin1en][12:13].to_string(index=False))
        resim_tahmin1 = weather.icon(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin1en][12:13].to_string(index=False))
        with colon1:
            st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun_tahmin1), unsafe_allow_html=True)
            image = Image.open('images/'+resim_tahmin1+'.png')
            st.image(image,use_column_width=True,caption="{}".format(durum_tahmin1))
            st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} kWh</p>".format(uretim_tahmin1), unsafe_allow_html=True)

        gun_tahmin2 = weather.cevir((datetime.date.today() + datetime.timedelta(days=1)).strftime("%A"))
        gun_tahmin2en = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%A")
        uretim_tahmin2 = round(float(dort_g["Generation"][dort_g["dt_obj"]==gun_tahmin2en]*oran),2)
        uretim_tahmin2 = "{:,}".format(int(uretim_tahmin2))
        durum_tahmin2= weather.main(icono_df_dort["main"][120:][icono_df_dort["day"]==gun_tahmin2en][12:13].to_string(index=False))
        resim_tahmin2 = weather.icon(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin2en][12:13].to_string(index=False))
        with colon2:
            st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun_tahmin2), unsafe_allow_html=True)
            image = Image.open('images/'+resim_tahmin2+'.png')
            st.image(image,use_column_width=True,caption="{}".format(durum_tahmin2))
            st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} kWh</p>".format(uretim_tahmin2), unsafe_allow_html=True)

        gun_tahmin3 = weather.cevir((datetime.date.today() + datetime.timedelta(days=2)).strftime("%A"))
        gun_tahmin3en = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%A") 
        uretim_tahmin3 = round(float(dort_g["Generation"][dort_g["dt_obj"]==gun_tahmin3en]*oran),2)
        uretim_tahmin3 = "{:,}".format(int(uretim_tahmin3))
        durum_tahmin3= weather.main(icono_df_dort["main"][120:][icono_df_dort["day"]==gun_tahmin3en][12:13].to_string(index=False))
        resim_tahmin3 = weather.icon(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin3en][12:13].to_string(index=False))
        with colon3:
            st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun_tahmin3), unsafe_allow_html=True)
            image = Image.open('images/'+resim_tahmin3+'.png')
            st.image(image,use_column_width=True,caption="{}".format(durum_tahmin3))
            st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} kWh</p>".format(uretim_tahmin3), unsafe_allow_html=True)

        gun_tahmin4 = weather.cevir((datetime.date.today() + datetime.timedelta(days=3)).strftime("%A"))
        gun_tahmin4en = (datetime.date.today() + datetime.timedelta(days=3)).strftime("%A")
        uretim_tahmin4 = round(float(dort_g["Generation"][dort_g["dt_obj"]==gun_tahmin4en]*oran),2)
        uretim_tahmin4 = "{:,}".format(int(uretim_tahmin4))
        durum_tahmin4= weather.main(icono_df_dort["main"][120:][icono_df_dort["day"]==gun_tahmin4en][12:13].to_string(index=False))
        resim_tahmin4 = weather.icon(icono_df_dort["icon"][120:][icono_df_dort["day"]==gun_tahmin4en][12:13].to_string(index=False))
        with colon4:
            st.markdown("<p style='text-align: center; color: #e08a12;background-color:#f2f2f2;font-size: 20px;font-weight:bold ;'>{}</p>".format(gun_tahmin4), unsafe_allow_html=True)
            image = Image.open('images/'+resim_tahmin4+'.png')
            st.image(image,use_column_width=True,caption="{}".format(durum_tahmin4))
            st.markdown("<p style='text-align: center; color: black;font-size: 27px;font-weight:bold ;'>{} kWh</p>".format(uretim_tahmin4), unsafe_allow_html=True)


        st.markdown("<br><br><br>", unsafe_allow_html=True)

        df.to_csv("df_gunluk.csv")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df["dt_obj"][149:162].dt.strftime("%H"), y=df["Generation"][149:162]*oran, name='Geçmiş Üretim',
                                 line=dict(color='#e08a12', width=4)))

        fig2.add_trace(go.Scatter(x=df["dt_obj"][161:173].dt.strftime("%H"), y=df["Generation"][161:173]*oran, name='Tahmini Üretim',
                                 line=dict(color='#4c79ec', width=4)))

        #fig2.update_xaxes(tickformat='%H')

        fig2.update_layout(
            font=dict(
                #family="sans-serif",
                size=18,
                color="#000000"
            ), 
            xaxis_tickangle=0,
            xaxis_tickmode="linear", 
            xaxis_title='Saatler',
            yaxis_title='Üretim (kWh)',

            title=dict(
                text='<b>Günlük Üretim (kWh)</b>',
                x=0.5,
                y=0.95,
                font=dict(
                    #family="Arial",
                    size=35,
                    color='#31333f'
                ))
                ,
                legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

        st.plotly_chart(fig2,use_container_width=True)
        
        
        aylik = ready.groupby(ready["dt_obj"][ready["month"] == month_now].dt.day).sum().reset_index()
        
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=aylik["dt_obj"],
            y=round(aylik["Generation"]*oran,0),
            marker_color='#e08a12',
            name="Toplam Üretim",
            text=round(aylik["Generation"]*oran,0),
            texttemplate='%{text:.2s}',
        ))
        
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(
            font=dict(
                #family="sans-serif",
                size=18,
                color="#31333f"
            ),barmode='group', 
            xaxis_tickangle=0,
            xaxis_title='Günler',
            yaxis_title='Üretim (kWh)',
            

            title=dict(
                text='<b>'+weather.aycevir(month_name_now)+' Ayı Üretim (kWh)</b>',
                x=0.5,
                y=0.95,
                font=dict(
                    #family="Arial",
                    size=35,
                    color='#31333f'
                )),
            legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1)
                )
        st.plotly_chart(fig,use_container_width=True)


        yillik = ready.groupby(ready["dt_obj"][ready["year"] == 2021].dt.month).sum().reset_index()
        months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
                  'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=months,
            y=round(yillik["Generation"]*oran,0),
            text=round(yillik["Generation"]*oran,0),
            textposition='auto',
            texttemplate='%{text:.2s}',
            marker_color='#4c79ec'
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
            yaxis_title='Üretim (kWh)',

            title=dict(
                text='<b>Yıllık Üretim (kWh)</b>',
                x=0.5,
                y=0.95,
                font=dict(
                    #family="Arial",
                    size=35,
                    color='#31333f'
                ))
                ,uniformtext_minsize=35)
        st.plotly_chart(fig,use_container_width=True)
    else:
        st.subheader(" ")
        st.subheader(" ")
        st.subheader(" ")
        st.subheader(" ")
        st.subheader(" ")
        st.subheader(" ")
        st.subheader(" ")
        st.subheader(" ")
        st.subheader("<<< Hesaplamak için soldaki formu doldurun.")        
        
    
    
    
