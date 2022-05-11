import streamlit as st
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