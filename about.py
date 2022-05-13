import streamlit as st
import awesome_streamlit as ast

def write():
    st.markdown("""
                <style>

                footer {visibility: hidden;}
                .e19lei0e1 {visibility: hidden;}  
                MainMenu {visibility: hidden;}  
                </style>
                """, unsafe_allow_html=True) 
    #MainMenu {visibility: hidden;}
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
 
    local_css("style.css")
 
    st.write("Bu çalışmada Ankara ili ve çevresinde bulunan illerde 522 MW Kurulugücü olan güneş enerji santralinin üretim değerleri kullanılarak saatlik olarak tahmin edilmeye çalışılmıştır. Güneş enerjisi tahmini yapmak için Catboost modeli kullanılmıştır. Modele girdi olarak sıcaklık, nem, bulutluluk oranı, rüzgar hızı, rüzgar yönü, hava durumu kodu, güneş yükseklik açısı, güneş azimut açısı, güneş uzaklığı, güneş ışınımı verileri kullanılmıştır. Test sonuçlarına bakıldığında, 15.4 RMSE skoru ile modelin yaptığı tahminlerin tutarlı olduğu tespit edilmiştir. Buna bağlı olarak farklı konumda bulunan santrallerin üretim verileri aynı yöntemle hesaplanabilir. **Tahminleme** sayfasında bu çalışmaya yer verilmiştir.")
    st.subheader("Türkiye Güneş Enerjisi Potansiyeli Haritası")
     
    st.image("images/solar_map.png",use_column_width=True) 
    