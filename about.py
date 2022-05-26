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
    
    st.write("Bu çalışmada Ankara ili ve çevresinde bulunan illerde 522 MW Kurulu gücü olan güneş enerji santralinin üretim değerleri kullanılarak saatlik olarak tahmin edilmeye çalışılmıştır. Güneş enerjisi tahmini yapmak için Catboost modeli kullanılmıştır. Modele girdi olarak sıcaklık, nem, bulutluluk oranı, rüzgar hızı, rüzgar yönü, hava durumu kodu, güneş yükseklik açısı, güneş azimut açısı, güneş uzaklığı, güneş ışınımı verileri kullanılmıştır. Test sonuçlarına bakıldığında, 15.4 RMSE skoru ile modelin yaptığı tahminlerin tutarlı olduğu tespit edilmiştir. Buna bağlı olarak farklı konumda bulunan santrallerin üretim verileri aynı yöntemle hesaplanabilir. **Tahminleme** sayfasında bu çalışmaya yer verilmiştir. Çalışmanın kaynak kodlarında aşağıdaki Github bağlantısından erişilebilir.")
    
    st.markdown('''
    <div id="container">
    <a href="https://www.linkedin.com/in/talha-uyan%C4%B1k-352045172/" style='text-decoration: none;'>
        <img src="https://pngimg.com/uploads/linkedIn/linkedIn_PNG4.png" width=41rem ;/>
        
    </a> 
    <a href="https://github.com/talhauyanik/solar_dash" style='margin-left:1rem'>
        <img src="https://pngimg.com/uploads/github/github_PNG40.png" width=50rem />
        
    </a>

    
    </div>
    ''',
    unsafe_allow_html=True
)
    
    st.subheader("Türkiye Güneş Enerjisi Potansiyeli Haritası")
     
    st.image("images/solar_map.png",use_column_width=True) 
    
    