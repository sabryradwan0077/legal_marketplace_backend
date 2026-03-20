import streamlit as st

st.set_page_config(page_title="سوق المحاماة الرقمي", page_icon="⚖️", layout="wide")

# =========================
# Session State
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "cases" not in st.session_state:
    st.session_state.cases = []

if "lawyers" not in st.session_state:
    st.session_state.lawyers = []

if "offers" not in st.session_state:
    st.session_state.offers = []

# =========================
# Functions
# =========================
def login():
    st.session_state.logged_in = True

def logout():
    st.session_state.logged_in = False

def reset_system():
    st.session_state.cases = []
    st.session_state.lawyers = []
    st.session_state.offers = []

def add_case(title, specialization, client_name, file):
    st.session_state.cases.append({
        "id": len(st.session_state.cases)+1,
        "title": title,
        "specialization": specialization,
        "client_name": client_name,
        "status": "مفتوحة",
        "selected_lawyer": None,
        "file": file.name if file else None
    })

def add_lawyer(name, specialization):
    st.session_state.lawyers.append({
        "id": len(st.session_state.lawyers)+1,
        "name": name,
        "specialization": specialization
    })

def add_offer(case_id, case_title, lawyer_id, lawyer_name, price):
    st.session_state.offers.append({
        "id": len(st.session_state.offers)+1,
        "case_id": case_id,
        "case_title": case_title,
        "lawyer_id": lawyer_id,
        "lawyer_name": lawyer_name,
        "price": price
    })

def delete_case(case_id):
    st.session_state.cases = [c for c in st.session_state.cases if c["id"] != case_id]
    st.session_state.offers = [o for o in st.session_state.offers if o["case_id"] != case_id]

def delete_lawyer(lawyer_id):
    st.session_state.lawyers = [l for l in st.session_state.lawyers if l["id"] != lawyer_id]
    st.session_state.offers = [o for o in st.session_state.offers if o["lawyer_id"] != lawyer_id]

def delete_offer(offer_id):
    st.session_state.offers = [o for o in st.session_state.offers if o["id"] != offer_id]

def select_offer(case_id, lawyer_name):
    for c in st.session_state.cases:
        if c["id"] == case_id:
            c["status"] = "مغلقة"
            c["selected_lawyer"] = lawyer_name

# =========================
# Login
# =========================
if not st.session_state.logged_in:
    st.title("🔐 تسجيل الدخول")

    user = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
        if user == "admin" and password == "1234":
            login()
            st.rerun()
        else:
            st.error("بيانات خاطئة")

    st.stop()

# =========================
# Header
# =========================
st.title("⚖️ سوق المحاماة الرقمي")

# =========================
# Stats
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("إجمالي القضايا", len(st.session_state.cases))
col2.metric("عدد المحامين", len(st.session_state.lawyers))
col3.metric("عدد العروض", len(st.session_state.offers))

# =========================
# Admin Controls
# =========================
st.warning("لوحة تحكم الإدارة")

if st.button("🧨 تصفير النظام بالكامل"):
    reset_system()
    st.success("تم تصفير النظام")
    st.rerun()

# =========================
# Tabs
# =========================
tab1, tab2, tab3 = st.tabs(["قضية", "محامي", "عرض"])

# ---------- CASE ----------
with tab1:
    st.subheader("إضافة قضية")

    with st.form("case"):
        title = st.text_input("عنوان")
        spec = st.selectbox("التخصص", ["جنائي","مدني","تجاري","أسرة"])
        client = st.text_input("العميل")
        file = st.file_uploader("رفع ملف", type=["pdf","png","jpg"])

        if st.form_submit_button("حفظ"):
            add_case(title, spec, client, file)
            st.success("تمت الإضافة")
            st.rerun()

# ---------- LAWYER ----------
with tab2:
    st.subheader("إضافة محامي")

    with st.form("lawyer"):
        name = st.text_input("اسم")
        spec = st.selectbox("تخصص", ["جنائي","مدني","تجاري","أسرة"])

        if st.form_submit_button("حفظ"):
            add_lawyer(name, spec)
            st.success("تمت الإضافة")
            st.rerun()

# ---------- OFFER ----------
with tab3:
    st.subheader("إضافة عرض")

    if st.session_state.cases and st.session_state.lawyers:

        case_titles = [c["title"] for c in st.session_state.cases]
        selected_case = st.selectbox("القضية", case_titles)

        case_obj = next(c for c in st.session_state.cases if c["title"] == selected_case)

        matching = [l for l in st.session_state.lawyers if l["specialization"] == case_obj["specialization"]]

        if matching:
            lawyer_names = [l["name"] for l in matching]

            with st.form("offer"):
                lawyer = st.selectbox("المحامي", lawyer_names)
                price = st.number_input("السعر", 0)

                if st.form_submit_button("حفظ"):
                    lawyer_obj = next(l for l in matching if l["name"] == lawyer)
                    add_offer(case_obj["id"], case_obj["title"], lawyer_obj["id"], lawyer, price)
                    st.success("تمت الإضافة")
                    st.rerun()
        else:
            st.error("لا يوجد محامي مناسب")

# =========================
# DATA VIEW
# =========================
st.header("📂 البيانات")

# CASES
st.subheader("القضايا")
for c in st.session_state.cases:
    st.write(c)

    if st.button(f"❌ حذف {c['title']}", key=f"dc{c['id']}"):
        delete_case(c["id"])
        st.rerun()

    offers = [o for o in st.session_state.offers if o["case_id"] == c["id"]]

    for o in offers:
        col1, col2 = st.columns([3,1])

        col1.write(f"{o['lawyer_name']} - {o['price']}")

        if c["status"] == "مفتوحة":
            if col2.button("اختيار", key=f"s{o['id']}"):
                select_offer(c["id"], o["lawyer_name"])
                st.rerun()

    if c["status"] == "مغلقة":
        st.success(f"تم الإسناد إلى {c['selected_lawyer']}")

# LAWYERS
st.subheader("المحامين")
for l in st.session_state.lawyers:
    st.write(l)

    if st.button(f"❌ حذف {l['name']}", key=f"dl{l['id']}"):
        delete_lawyer(l["id"])
        st.rerun()

# OFFERS
st.subheader("العروض")
for o in st.session_state.offers:
    st.write(o)

    if st.button(f"❌ حذف عرض {o['id']}", key=f"do{o['id']}"):
        delete_offer(o["id"])
        st.rerun()

# =========================
# Logout
# =========================
st.button("🚪 تسجيل خروج", on_click=logout)
