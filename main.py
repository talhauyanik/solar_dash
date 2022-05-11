import streamlit as st
import awesome_streamlit as ast
import home
import predict
import about

ast.core.services.other.set_logging_format()
 
PAGES = {   
    "Anasayfa": home, 
    "Tahminler": predict, 
    "Hakkında":about,         
            
}      
       
def main():
    #st.sidebar.markdown("<img src='logov3.png' style='max-width: 100%;'>",unsafe_allow_html=True)
    with st.sidebar:
        
        st.image("logov5.png",width=120)
            
        selection = st.sidebar.radio("", list(PAGES.keys()))

        page = PAGES[selection]
 
    with st.spinner("Yükleniyor"):
        ast.shared.components.write_page(page)
     
    
if __name__ == "__main__":
    main()
    