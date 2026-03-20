import streamlit as st

st.set_page_config(page_title="سوق المحاماة الرقمي", page_icon="⚖️", layout="wide")

# -------------------------
# Session State Initialization
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "cases" not in st.session_state:
    st.session_state["cases"] = []

if "lawyers" not in st.session_state:
    st.session_state["lawyers"] = []

if "offers" not in st.session_state:
    st.session_state["offers"] = []


# -------------------------
# Helpers
# -------------------------
def do_login():
    st.session_state["logged_in"] = True

def do_logout():
    st.session_state["logged_in"] = False

def add_case(title, specialization, client_name):
    st.session_state["cases"].append({
        "title": title,
        "specialization": specialization,
        "client_name": client_name
    })

def add_lawyer(name, specialization):
    st.session_state["lawyers"].append({
        "name": name,
        "specialization": specialization
    })

def add_offer(case_title, lawyer_name, price):
    st.session_state["offers"].append({
        "case_title": case_title,
        "lawyer_name": lawyer_name,
        "price": price
    })


# -------------------------
# Style
# -------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    direction: rtl;
}
.main-title {
    color: #f4d35e;
    font-size: 52px;
    font-weight: bold;
    text-align: center;
    margin-top: 10px;
}
.sub-title {
    color: #d9d9d9;
    font-size: 24px;
    text-align: center;
    margin-bottom: 30px;
}
.stat-box {
    background: #0b2a4a;
    border: 2px solid #d4af37;
    border-radius: 24px;
    padding: 25px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
    min-height: 220px;
}
.section-box {
    background: #081f38;
    border: 1px solid #d4af37;
    border-radius: 20px;
    padding: 20px;
    margin-top: 20px;
    margin-bottom: 20px;
}
.small-card {
    background: #102c4c;
    border: 1px solid #d4af37;
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 12px;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# -------------------------
# Login Screen
# -------------------------
if not st.session_state["logged_in"]:
    st.markdown('<div class="main-title">سوق المحاماة الرقمي</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">بوابة المستشار صبري رضوان الذكية</div>', unsafe_allow_html=True)

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


# -------------------------
# Dashboard Header
# -------------------------
st.markdown('<div class="main-title">الرقمي</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">بوابة المستشار صبري رضوان الذكية</div>', unsafe_allow_html=True)

# -------------------------
# Stats
# -------------------------
total_cases = len(st.session_state["cases"])
total_lawyers = len(st.session_state["lawyers"])
total_offers = len(st.session_state["offers"])

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f'<div class="stat-box"><h2>📊 إجمالي القضايا</h2><h1>{total_cases}</h1></div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="stat-box"><h2>🧑‍⚖️ محامين متاحين</h2><h1>{total_lawyers}</h1></div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<div class="stat-box"><h2>📝 عروض جديدة</h2><h1>{total_offers}</h1></div>',
        unsafe_allow_html=True
    )


# -------------------------
# Forms
# -------------------------
st.markdown("## إدارة البيانات")

tab1, tab2, tab3 = st.tabs(["إضافة قضية", "إضافة محامٍ", "إضافة عرض"])

with tab1:
    with st.form("case_form"):
        case_title = st.text_input("عنوان القضية")
        case_specialization = st.selectbox(
            "التخصص",
            ["أحوال شخصية", "جنائي", "تجاري", "عمالي", "إداري", "مدني"]
        )
        client_name = st.text_input("اسم العميل")
        submitted_case = st.form_submit_button("حفظ القضية")
        if submitted_case:
            if case_title and client_name:
                add_case(case_title, case_specialization, client_name)
                st.success("تمت إضافة القضية بنجاح")
                st.rerun()
            else:
                st.error("أدخل عنوان القضية واسم العميل")

with tab2:
    with st.form("lawyer_form"):
        lawyer_name = st.text_input("اسم المحامي")
        lawyer_specialization = st.selectbox(
            "تخصص المحامي",
            ["أحوال شخصية", "جنائي", "تجاري", "عمالي", "إداري", "مدني"]
        )
        submitted_lawyer = st.form_submit_button("حفظ المحامي")
        if submitted_lawyer:
            if lawyer_name:
                add_lawyer(lawyer_name, lawyer_specialization)
                st.success("تمت إضافة المحامي بنجاح")
                st.rerun()
            else:
                st.error("أدخل اسم المحامي")

with tab3:
    with st.form("offer_form"):
        if st.session_state["cases"]:
            case_titles = [c["title"] for c in st.session_state["cases"]]
        else:
            case_titles = []

        if st.session_state["lawyers"]:
            lawyer_names = [l["name"] for l in st.session_state["lawyers"]]
        else:
            lawyer_names = []

        selected_case = st.selectbox("اختر القضية", case_titles if case_titles else ["لا توجد قضايا"])
        selected_lawyer = st.selectbox("اختر المحامي", lawyer_names if lawyer_names else ["لا يوجد محامون"])
        offer_price = st.number_input("قيمة العرض", min_value=0, step=100)

        submitted_offer = st.form_submit_button("حفظ العرض")

        if submitted_offer:
            if case_titles and lawyer_names:
                add_offer(selected_case, selected_lawyer, offer_price)
                st.success("تمت إضافة العرض بنجاح")
                st.rerun()
            else:
                st.error("يجب إضافة قضية ومحامٍ أولًا")


# -------------------------
# Listings
# -------------------------
st.markdown("## البيانات الحالية")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("### القضايا")
    if st.session_state["cases"]:
        for c in st.session_state["cases"]:
            st.markdown(
                f"""
                <div class="small-card">
                    <b>العنوان:</b> {c['title']}<br>
                    <b>التخصص:</b> {c['specialization']}<br>
                    <b>العميل:</b> {c['client_name']}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("لا توجد قضايا بعد")

with col_b:
    st.markdown("### المحامون")
    if st.session_state["lawyers"]:
        for l in st.session_state["lawyers"]:
            st.markdown(
                f"""
                <div class="small-card">
                    <b>الاسم:</b> {l['name']}<br>
                    <b>التخصص:</b> {l['specialization']}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("لا يوجد محامون بعد")

with col_c:
    st.markdown("### العروض")
    if st.session_state["offers"]:
        for o in st.session_state["offers"]:
            st.markdown(
                f"""
                <div class="small-card">
                    <b>القضية:</b> {o['case_title']}<br>
                    <b>المحامي:</b> {o['lawyer_name']}<br>
                    <b>السعر:</b> {o['price']}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("لا توجد عروض بعد")

st.divider()
st.button("تسجيل الخروج", on_click=do_logout, use_container_width=True)
