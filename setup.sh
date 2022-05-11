mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS= false\n\
headless = true\n\
[theme]\n\
base ='light'\n\
textColor = '#31333F'\n\
primaryColor = '#e08a12'\n\
backgroundColor = '#ffffff'\n\
secondaryBackgroundColor = '#F0F2F6'\n\
font = 'sans serif'\n\
\n\
" > ~/.streamlit/config.toml