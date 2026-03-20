import streamlit as st

# -------------------------
# نظام تسجيل دخول بسيط
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 تسجيل الدخول")

    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("تم تسجيل الدخول بنجاح")
            st.rerun()
        else:
            st.error("بيانات غير صحيحة")

# لو مش مسجل دخول
if not st.session_state.logged_in:
    login()
    st.stop()
