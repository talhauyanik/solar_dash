import streamlit as st
import awesome_streamlit as ast
import home
import predict
import about
from weather import icon
st.set_page_config(layout="wide",page_title="Güneş Enerjisi Üretim Tahmini",page_icon="logov5.png")
ast.core.services.other.set_logging_format()

PAGES = {   
    "Anasayfa": home, 
    "Tahminler": predict, 
    "Hakkında":about,         
            
}      

def main():
    

    with st.sidebar:
        
        st.image("logov5.png",width=120)
        st.markdown("<h1 style='margin-top:-20px'>Solar Forecast</h1>",unsafe_allow_html=True)    
        selection = st.sidebar.radio("", list(PAGES.keys()))

        page = PAGES[selection]
 
    with st.spinner("Yükleniyor"):
        
        ast.shared.components.write_page(page)

    
if __name__ == "__main__":
    main()
    