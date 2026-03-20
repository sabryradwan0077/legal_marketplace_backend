@echo off
echo Starting Backend...
start cmd /k uvicorn app.main:app --reload

timeout /t 3

echo Starting Streamlit...
start cmd /k streamlit run streamlit_app.py
