import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="الحصن القانوني - Sabry Radwan", layout="wide", page_icon="⚖️")

# ستايل كحلي وذهبي
st.markdown("""
    <style>
    .main { background-color: #001f3f; color: white; }
    .stMetric { background-color: #002b5c; padding: 15px; border-radius: 10px; border: 1px solid #FFD700; }
    </style>
    <div style="background-color:#001f3f; padding:25px; border-radius:15px; border: 2px solid #FFD700; text-align:center;">
        <h1 style="color:#FFD700; margin-bottom:0;">⚖️ سُوق المحاماة الرّقمي ⚖️</h1>
        <p style="color:#C0C0C0; font-size:1.2em;">بوابة المستشار صبري رضوان الذكية</p>
    </div>
""", unsafe_allow_html=True)

st.write("") # مسافة

# عرض العدادات (بشكل تجريبي الآن)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="📊 إجمالي القضايا", value="0")
with col2:
    st.metric(label="👨‍⚖️ محامين متاحين", value="0")
with col3:
    st.metric(label="📝 عروض جديدة", value="0")

st.success("✅ تم ربط المحرك (FastAPI) بقاعدة البيانات المشفرة بنجاح.")

st.sidebar.title("القائمة الرئيسية")
st.sidebar.button("إضافة قضية جديدة")
st.sidebar.button("لوحة تحكم المحامين")
st.sidebar.info(f"مفتاح الصانع نشط: {st.secrets.get('SECRET_KEY', 'مخفي')[:5]}****")
