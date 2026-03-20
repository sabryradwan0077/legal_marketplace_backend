import streamlit as st

st.set_page_config(page_title="سوق المحاماة الرقمي", page_icon="⚖️", layout="wide")

# =========================
# Session State Initialization
# =========================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "cases" not in st.session_state:
    st.session_state["cases"] = []

if "lawyers" not in st.session_state:
    st.session_state["lawyers"] = []

if "offers" not in st.session_state:
    st.session_state["offers"] = []


# =========================
# Helpers
# =========================
def do_login():
    st.session_state["logged_in"] = True

def do_logout():
    st.session_state["logged_in"] = False

def add_case(title, specialization, client_name):
    st.session_state["cases"].append({
        "id": len(st.session_state["cases"]) + 1,
        "title": title,
        "specialization": specialization,
        "client_name": client_name,
        "status": "مفتوحة",
        "selected_lawyer": None
    })

def add_lawyer(name, specialization):
    st.session_state["lawyers"].append({
        "id": len(st.session_state["lawyers"]) + 1,
        "name": name,
        "specialization": specialization
    })

def add_offer(case_id, case_title, lawyer_id, lawyer_name, price):
    st.session_state["offers"].append({
        "id": len(st.session_state["offers"]) + 1,
        "case_id": case_id,
        "case_title": case_title,
        "lawyer_id": lawyer_id,
        "lawyer_name": lawyer_name,
        "price": price
    })

def get_case_by_title(case_title):
    for case in st.session_state["cases"]:
        if case["title"] == case_title:
            return case
    return None

def get_matching_lawyers(case_specialization):
    return [
        lawyer for lawyer in st.session_state["lawyers"]
        if lawyer["specialization"] == case_specialization
    ]

def get_available_lawyers_count():
    needed_specs = {case["specialization"] for case in st.session_state["cases"]}
    return sum(
        1 for lawyer in st.session_state["lawyers"]
        if lawyer["specialization"] in needed_specs
    )

def get_case_offers(case_id):
    return [o for o in st.session_state["offers"] if o["case_id"] == case_id]

def select_offer_for_case(case_id, lawyer_name):
    for case in st.session_state["cases"]:
        if case["id"] == case_id:
            case["status"] = "مغلقة"
            case["selected_lawyer"] = lawyer_name
            break


# =========================
# Styling
# =========================
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

.small-card {
    background: #102c4c;
    border: 1px solid #d4af37;
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 12px;
    color: white;
}

.info-line {
    color: #d9d9d9;
    font-size: 16px;
    margin-bottom: 10px;
}

.block-title {
    color: white;
    font-size: 28px;
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# Login Screen
# =========================
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


# =========================
# Header
# =========================
st.markdown('<div class="main-title">سوق المحاماة الرقمي</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">بوابة المستشار صبري رضوان الذكية</div>', unsafe_allow_html=True)


# =========================
# Dashboard Stats
# =========================
total_cases = len(st.session_state["cases"])
available_lawyers = get_available_lawyers_count()
total_offers = len(st.session_state["offers"])

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f'<div class="stat-box"><h2>📊 إجمالي القضايا</h2><h1>{total_cases}</h1></div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="stat-box"><h2>🧑‍⚖️ محامين متاحين</h2><h1>{available_lawyers}</h1></div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<div class="stat-box"><h2>📝 عروض جديدة</h2><h1>{total_offers}</h1></div>',
        unsafe_allow_html=True
    )


# =========================
# Data Management Forms
# =========================
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
            if case_title.strip() and client_name.strip():
                add_case(case_title.strip(), case_specialization, client_name.strip())
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
            if lawyer_name.strip():
                add_lawyer(lawyer_name.strip(), lawyer_specialization)
                st.success("تمت إضافة المحامي بنجاح")
                st.rerun()
            else:
                st.error("أدخل اسم المحامي")

with tab3:
    if st.session_state["cases"]:
        case_titles = [c["title"] for c in st.session_state["cases"]]
        selected_case_title = st.selectbox("اختر القضية", case_titles, key="offer_case_select")

        selected_case = get_case_by_title(selected_case_title)
        matching_lawyers = get_matching_lawyers(selected_case["specialization"]) if selected_case else []

        if selected_case:
            st.markdown(
                f"<div class='info-line'>تخصص القضية: <b>{selected_case['specialization']}</b></div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div class='info-line'>حالة القضية: <b>{selected_case['status']}</b></div>",
                unsafe_allow_html=True
            )

        if selected_case and selected_case["status"] == "مغلقة":
            st.warning("هذه القضية مغلقة بالفعل، ولا يمكن إضافة عروض جديدة عليها.")

        elif matching_lawyers:
            lawyer_options = [lawyer["name"] for lawyer in matching_lawyers]

            with st.form("offer_form"):
                selected_lawyer_name = st.selectbox("اختر المحامي المناسب", lawyer_options)
                offer_price = st.number_input("قيمة العرض", min_value=0, step=100)
                submitted_offer = st.form_submit_button("حفظ العرض")

                if submitted_offer:
                    selected_lawyer = next(
                        (lawyer for lawyer in matching_lawyers if lawyer["name"] == selected_lawyer_name),
                        None
                    )

                    existing_offer = next(
                        (
                            offer for offer in st.session_state["offers"]
                            if offer["case_id"] == selected_case["id"] and offer["lawyer_id"] == selected_lawyer["id"]
                        ),
                        None
                    ) if selected_case and selected_lawyer else None

                    if existing_offer:
                        st.error("هذا المحامي قدم عرضًا بالفعل على هذه القضية")
                    elif selected_case and selected_lawyer:
                        add_offer(
                            case_id=selected_case["id"],
                            case_title=selected_case["title"],
                            lawyer_id=selected_lawyer["id"],
                            lawyer_name=selected_lawyer["name"],
                            price=offer_price
                        )
                        st.success("تمت إضافة العرض بنجاح")
                        st.rerun()
                    else:
                        st.error("تعذر حفظ العرض")
        else:
            st.warning("لا يوجد محامون مطابقون لتخصص هذه القضية. أضف محاميًا بنفس التخصص أولًا.")
    else:
        st.info("لا توجد قضايا بعد. أضف قضية أولًا.")


# =========================
# Current Data
# =========================
st.markdown("## البيانات الحالية")
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("### القضايا")

    if st.session_state["cases"]:
        for c in st.session_state["cases"]:
            related_offers = get_case_offers(c["id"])

            st.markdown(
                f"""
                <div class="small-card">
                    <b>العنوان:</b> {c['title']}<br>
                    <b>التخصص:</b> {c['specialization']}<br>
                    <b>العميل:</b> {c['client_name']}<br>
                    <b>الحالة:</b> {c['status']}<br>
                    <b>عدد العروض:</b> {len(related_offers)}
                </div>
                """,
                unsafe_allow_html=True
            )

            if related_offers and c["status"] == "مفتوحة":
                st.write("العروض الخاصة بهذه القضية:")

                for offer in related_offers:
                    offer_col1, offer_col2 = st.columns([3, 1])

                    with offer_col1:
                        st.info(f"المحامي: {offer['lawyer_name']} | السعر: {offer['price']}")

                    with offer_col2:
                        if st.button("اختيار", key=f"select_offer_{offer['id']}"):
                            select_offer_for_case(c["id"], offer["lawyer_name"])
                            st.success(f"تم اختيار المحامي {offer['lawyer_name']} وإغلاق القضية")
                            st.rerun()

            if c["status"] == "مغلقة":
                st.success(f"تم الإسناد إلى: {c.get('selected_lawyer', '-')}")

    else:
        st.info("لا توجد قضايا بعد")

with col_b:
    st.markdown("### المحامون")

    if st.session_state["lawyers"]:
        for l in st.session_state["lawyers"]:
            matching_cases = [
                case for case in st.session_state["cases"]
                if case["specialization"] == l["specialization"]
            ]
            st.markdown(
                f"""
                <div class="small-card">
                    <b>الاسم:</b> {l['name']}<br>
                    <b>التخصص:</b> {l['specialization']}<br>
                    <b>قضايا مطابقة:</b> {len(matching_cases)}
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
            case_obj = next((case for case in st.session_state["cases"] if case["id"] == o["case_id"]), None)
            offer_status = "فائز" if case_obj and case_obj.get("selected_lawyer") == o["lawyer_name"] else "قيد المنافسة"

            st.markdown(
                f"""
                <div class="small-card">
                    <b>القضية:</b> {o['case_title']}<br>
                    <b>المحامي:</b> {o['lawyer_name']}<br>
                    <b>السعر:</b> {o['price']}<br>
                    <b>الحالة:</b> {offer_status}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("لا توجد عروض بعد")


# =========================
# Footer Actions
# =========================
st.divider()
st.button("تسجيل الخروج", on_click=do_logout, use_container_width=True)
