import requests
import streamlit as st

# =========================
# إعدادات عامة
# =========================
st.set_page_config(
    page_title="سوق المحاماة الرقمي",
    page_icon="⚖️",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

SPECIALIZATIONS = [
    "أحوال شخصية",
    "جنائي",
    "تجاري",
    "عمالي",
    "إداري",
    "مدني"
]

# =========================
# Session State
# =========================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "token" not in st.session_state:
    st.session_state["token"] = None

if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

if "user_role" not in st.session_state:
    st.session_state["user_role"] = None


# =========================
# CSS
# =========================
st.markdown("""
<style>
html, body, [class*="css"]  {
    direction: rtl;
    text-align: right;
}
.main-title {
    color: #f4d35e;
    font-size: 48px;
    font-weight: 800;
    text-align: center;
    margin-top: 5px;
}
.sub-title {
    color: #d9d9d9;
    font-size: 22px;
    text-align: center;
    margin-bottom: 25px;
}
.stat-box {
    background: #0b2a4a;
    border: 2px solid #d4af37;
    border-radius: 24px;
    padding: 25px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
    min-height: 180px;
}
.small-card {
    background: #102c4c;
    border: 1px solid #d4af37;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 12px;
    color: white;
}
.section-title {
    color: white;
    font-size: 24px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 10px;
}
.role-badge {
    background: #d4af37;
    color: #08111f;
    padding: 8px 14px;
    border-radius: 999px;
    font-weight: bold;
    display: inline-block;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# API Helpers
# =========================
def get_headers():
    token = st.session_state.get("token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def register_api(full_name, email, password, role, specialization=None, phone=None):
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json={
                "full_name": full_name,
                "email": email,
                "password": password,
                "role": role,
                "specialization": specialization,
                "phone": phone
            },
            timeout=20
        )
        return response
    except requests.RequestException:
        return None


def login_api(email, password):
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "email": email,
                "password": password
            },
            timeout=20
        )
        return response
    except requests.RequestException:
        return None


def fetch_cases():
    try:
        response = requests.get(
            f"{API_URL}/cases",
            headers=get_headers(),
            timeout=20
        )
        if response.status_code == 200:
            return response.json()
        return []
    except requests.RequestException:
        return []


def create_case_api(title, description, specialization):
    try:
        response = requests.post(
            f"{API_URL}/cases/",
            json={
                "title": title,
                "description": description,
                "specialization": specialization,
                "attachment_name": None
            },
            headers=get_headers(),
            timeout=20
        )
        return response
    except requests.RequestException:
        return None


def fetch_case_proposals(case_id):
    try:
        response = requests.get(
            f"{API_URL}/proposals/case/{case_id}",
            headers=get_headers(),
            timeout=20
        )
        if response.status_code == 200:
            return response.json()
        return []
    except requests.RequestException:
        return []


def create_proposal_api(case_id, offer_text, price, estimated_days):
    try:
        response = requests.post(
            f"{API_URL}/proposals/{case_id}",
            json={
                "offer_text": offer_text,
                "price": int(price),
                "estimated_days": int(estimated_days)
            },
            headers=get_headers(),
            timeout=20
        )
        return response
    except requests.RequestException:
        return None


def decode_role_from_cases_fallback():
    """
    احتياطي فقط إذا لم نعرف الدور من الواجهة.
    """
    return st.session_state.get("user_role")


def do_logout():
    st.session_state["logged_in"] = False
    st.session_state["token"] = None
    st.session_state["user_email"] = None
    st.session_state["user_role"] = None


def check_backend():
    try:
        response = requests.get(f"{API_URL}/", timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False


# =========================
# Header
# =========================
st.markdown('<div class="main-title">سوق المحاماة الرقمي</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">بوابة المستشار صبري رضوان الذكية</div>', unsafe_allow_html=True)

backend_ok = check_backend()
if not backend_ok:
    st.error("الـ Backend غير شغال. شغّل FastAPI أولًا بالأمر: uvicorn app.main:app --reload")
    st.stop()


# =========================
# Auth Screen
# =========================
if not st.session_state["logged_in"]:
    tab_login, tab_register = st.tabs(["تسجيل الدخول", "إنشاء حساب"])

    with tab_login:
        st.markdown("### تسجيل الدخول")
        login_email = st.text_input("البريد الإلكتروني", key="login_email")
        login_password = st.text_input("كلمة المرور", type="password", key="login_password")

        if st.button("دخول", use_container_width=True):
            if not login_email or not login_password:
                st.error("أدخل البريد الإلكتروني وكلمة المرور")
            else:
                response = login_api(login_email, login_password)
                if response is None:
                    st.error("تعذر الاتصال بالسيرفر")
                elif response.status_code == 200:
                    data = response.json()
                    st.session_state["token"] = data["access_token"]
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = login_email
                    st.success("تم تسجيل الدخول بنجاح")
                    st.rerun()
                else:
                    try:
                        msg = response.json().get("detail", "فشل تسجيل الدخول")
                    except Exception:
                        msg = "فشل تسجيل الدخول"
                    st.error(msg)

    with tab_register:
        st.markdown("### إنشاء حساب جديد")
        reg_full_name = st.text_input("الاسم الكامل", key="reg_full_name")
        reg_email = st.text_input("البريد الإلكتروني", key="reg_email")
        reg_password = st.text_input("كلمة المرور", type="password", key="reg_password")
        reg_phone = st.text_input("رقم الهاتف", key="reg_phone")
        reg_role = st.selectbox("نوع الحساب", ["client", "lawyer"], key="reg_role")

        reg_specialization = None
        if reg_role == "lawyer":
            reg_specialization = st.selectbox("التخصص", SPECIALIZATIONS, key="reg_specialization")

        if st.button("إنشاء الحساب", use_container_width=True):
            if not reg_full_name or not reg_email or not reg_password:
                st.error("أكمل البيانات الأساسية")
            else:
                response = register_api(
                    full_name=reg_full_name,
                    email=reg_email,
                    password=reg_password,
                    role=reg_role,
                    specialization=reg_specialization,
                    phone=reg_phone
                )

                if response is None:
                    st.error("تعذر الاتصال بالسيرفر")
                elif response.status_code == 200:
                    st.success("تم إنشاء الحساب بنجاح. يمكنك الآن تسجيل الدخول.")
                else:
                    try:
                        msg = response.json().get("detail", "تعذر إنشاء الحساب")
                    except Exception:
                        msg = "تعذر إنشاء الحساب"
                    st.error(msg)

    st.stop()


# =========================
# Main Data
# =========================
cases = fetch_cases()

# محاولة تحديد الدور من الشاشة الحالية
# في هذا المشروع البسيط نأخذه من اختيار المستخدم عند التسجيل/التعامل
if st.session_state["user_role"] is None:
    st.session_state["user_role"] = decode_role_from_cases_fallback()

user_role = st.session_state.get("user_role")

# لو المستخدم دخل مباشرة بدون أن نعرف دوره، نتركه يحدده يدويًا
if not user_role:
    st.session_state["user_role"] = st.selectbox(
        "حدد نوع حسابك الحالي لعرض الواجهة المناسبة",
        ["client", "lawyer", "admin"],
        key="manual_role_select"
    )
    user_role = st.session_state["user_role"]

# =========================
# Stats
# =========================
all_proposals_count = 0
for c in cases:
    all_proposals_count += len(fetch_case_proposals(c["id"]))

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f'<div class="stat-box"><h2>📊 إجمالي القضايا</h2><h1>{len(cases)}</h1></div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="stat-box"><h2>🧾 إجمالي العروض</h2><h1>{all_proposals_count}</h1></div>',
        unsafe_allow_html=True
    )

with col3:
    badge = "عميل" if user_role == "client" else "محامٍ" if user_role == "lawyer" else "إدارة"
    st.markdown(
        f'<div class="stat-box"><h2>👤 نوع الحساب</h2><h1 style="font-size:32px">{badge}</h1></div>',
        unsafe_allow_html=True
    )

st.markdown(f'<div class="role-badge">البريد الحالي: {st.session_state["user_email"]}</div>', unsafe_allow_html=True)


# =========================
# Client View
# =========================
if user_role == "client":
    tab1, tab2 = st.tabs(["إضافة قضية جديدة", "قضاياي والعروض"])

    with tab1:
        st.markdown("### إضافة قضية جديدة")
        with st.form("create_case_form"):
            case_title = st.text_input("عنوان القضية")
            case_description = st.text_area("وصف القضية")
            case_specialization = st.selectbox("التخصص", SPECIALIZATIONS)
            submit_case = st.form_submit_button("حفظ القضية")

            if submit_case:
                if not case_title.strip() or not case_description.strip():
                    st.error("أدخل عنوان ووصف القضية")
                else:
                    response = create_case_api(
                        title=case_title.strip(),
                        description=case_description.strip(),
                        specialization=case_specialization
                    )
                    if response is None:
                        st.error("تعذر الاتصال بالسيرفر")
                    elif response.status_code == 200:
                        st.success("تم إنشاء القضية بنجاح")
                        st.rerun()
                    else:
                        try:
                            msg = response.json().get("detail", "تعذر إنشاء القضية")
                        except Exception:
                            msg = "تعذر إنشاء القضية"
                        st.error(msg)

    with tab2:
        st.markdown("### قضاياي")
        if not cases:
            st.info("لا توجد قضايا بعد")
        else:
            for case in cases:
                st.markdown(
                    f"""
                    <div class="small-card">
                        <b>العنوان:</b> {case['title']}<br>
                        <b>التخصص:</b> {case['specialization']}<br>
                        <b>الحالة:</b> {case['status']}<br>
                        <b>الوصف:</b> {case['description']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                proposals = fetch_case_proposals(case["id"])
                if proposals:
                    st.write("العروض المقدمة:")
                    for proposal in proposals:
                        st.info(
                            f"المحامي رقم {proposal['lawyer_id']} | السعر: {proposal['price']} | "
                            f"المدة: {proposal['estimated_days']} يوم | "
                            f"التفاصيل: {proposal['offer_text']}"
                        )
                else:
                    st.warning("لا توجد عروض بعد لهذه القضية")


# =========================
# Lawyer View
# =========================
elif user_role == "lawyer":
    tab1, tab2 = st.tabs(["القضايا المتاحة", "تقديم عرض"])

    with tab1:
        st.markdown("### القضايا المناسبة لتخصصك")
        if not cases:
            st.info("لا توجد قضايا متاحة حاليًا")
        else:
            for case in cases:
                st.markdown(
                    f"""
                    <div class="small-card">
                        <b>رقم القضية:</b> {case['id']}<br>
                        <b>العنوان:</b> {case['title']}<br>
                        <b>التخصص:</b> {case['specialization']}<br>
                        <b>الحالة:</b> {case['status']}<br>
                        <b>الوصف:</b> {case['description']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with tab2:
        st.markdown("### تقديم عرض على قضية")
        if not cases:
            st.info("لا توجد قضايا لتقديم عروض عليها")
        else:
            case_options = {f"{c['id']} - {c['title']}": c["id"] for c in cases}
            selected_case_label = st.selectbox("اختر القضية", list(case_options.keys()))
            selected_case_id = case_options[selected_case_label]

            with st.form("proposal_form"):
                offer_text = st.text_area("تفاصيل العرض")
                price = st.number_input("السعر", min_value=0, step=100)
                estimated_days = st.number_input("المدة المتوقعة بالأيام", min_value=1, step=1)
                submit_proposal = st.form_submit_button("إرسال العرض")

                if submit_proposal:
                    if not offer_text.strip():
                        st.error("أدخل تفاصيل العرض")
                    else:
                        response = create_proposal_api(
                            case_id=selected_case_id,
                            offer_text=offer_text.strip(),
                            price=price,
                            estimated_days=estimated_days
                        )
                        if response is None:
                            st.error("تعذر الاتصال بالسيرفر")
                        elif response.status_code == 200:
                            st.success("تم إرسال العرض بنجاح")
                            st.rerun()
                        else:
                            try:
                                msg = response.json().get("detail", "تعذر إرسال العرض")
                            except Exception:
                                msg = "تعذر إرسال العرض"
                            st.error(msg)


# =========================
# Admin View
# =========================
else:
    st.markdown("### لوحة الإدارة")
    if not cases:
        st.info("لا توجد بيانات بعد")
    else:
        for case in cases:
            st.markdown(
                f"""
                <div class="small-card">
                    <b>رقم القضية:</b> {case['id']}<br>
                    <b>العنوان:</b> {case['title']}<br>
                    <b>التخصص:</b> {case['specialization']}<br>
                    <b>الحالة:</b> {case['status']}<br>
                    <b>العميل رقم:</b> {case['client_id']}
                </div>
                """,
                unsafe_allow_html=True
            )

            proposals = fetch_case_proposals(case["id"])
            if proposals:
                for proposal in proposals:
                    st.info(
                        f"عرض على القضية {case['id']} | المحامي رقم {proposal['lawyer_id']} | "
                        f"السعر: {proposal['price']} | المدة: {proposal['estimated_days']} يوم"
                    )
            else:
                st.warning("لا توجد عروض على هذه القضية")


# =========================
# Footer
# =========================
st.divider()
if st.button("تسجيل الخروج", use_container_width=True):
    do_logout()
    st.rerun()
