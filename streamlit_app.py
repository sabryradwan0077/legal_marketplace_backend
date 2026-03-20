import streamlit as st

st.set_page_config(page_title="سوق المحاماة الرقمي", page_icon="⚖️", layout="wide")

# حالة تسجيل الدخول
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def do_login():
    st.session_state["logged_in"] = True

def do_logout():
    st.session_state["logged_in"] = False

# تنسيق بسيط وآمن
st.markdown("""
<style>
html, body, [class*="css"] {
    direction: rtl;
}
.main-title {
    color: #f4d35e;
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-top: 20px;
}
.sub-title {
    color: #d9d9d9;
    font-size: 22px;
    text-align: center;
    margin-bottom: 30px;
}
.stat-box {
    background: #0b2a4a;
    border: 2px solid #d4af37;
    border-radius: 18px;
    padding: 20px;
    color: white;
    text-align: center;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# شاشة الدخول
if not st.session_state["logged_in"]:
    st.markdown('<div class="main-title">⚖️ سوق المحاماة الرقمي</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">تسجيل الدخول إلى البوابة</div>', unsafe_allow_html=True)

    with st.container():
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")

        if st.button("دخول", use_container_width=True):
            if username == "admin" and password == "1234":
                do_login()
                st.success("تم تسجيل الدخول بنجاح")
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة")

    st.stop()

# بعد الدخول
st.markdown('<div class="main-title">⚖️ سوق المحاماة الرقمي</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">بوابة المستشار صبري رضوان الذكية</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="stat-box"><h3>📊 إجمالي القضايا</h3><h1>0</h1></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="stat-box"><h3>🧑‍⚖️ محامين متاحين</h3><h1>0</h1></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="stat-box"><h3>📝 عروض جديدة</h3><h1>0</h1></div>', unsafe_allow_html=True)

st.button("تسجيل الخروج", on_click=do_logout)
