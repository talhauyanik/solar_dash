mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS= false\n\
headless = true\n\
[theme]\n\
base ='light'\n\
textColor = '#31333F'\n\
primaryColor = '#ec6e4c'\n\
backgroundColor = '#ffffff'\n\
secondaryBackgroundColor = '#F0F2F6'\n\
font = 'serif'\n\
\n\
" > ~/.streamlit/config.toml