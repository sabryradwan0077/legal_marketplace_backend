import base64
import json
import requests
import streamlit as st

# =========================
# إعدادات عامة
# =========================
st.set_page_config(
    page_title="LEGAL MARKETPLACE - SABRY RADWAN",
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

if "flash_success" not in st.session_state:
    st.session_state["flash_success"] = None

if "flash_error" not in st.session_state:
    st.session_state["flash_error"] = None


# =========================
# CSS
# =========================
st.markdown("""
<style>
html, body, [class*="css"] {
    direction: rtl;
    text-align: right;
}

.stApp {
    background:
        radial-gradient(circle at top right, rgba(212,175,55,0.15), transparent 25%),
        radial-gradient(circle at bottom left, rgba(212,175,55,0.08), transparent 22%),
        linear-gradient(135deg, #06111f 0%, #081827 35%, #0b2034 70%, #09121c 100%);
    color: #f5f0df;
}

.main-brand {
    text-align: center;
    margin-top: 10px;
    margin-bottom: 20px;
}

.main-brand h1 {
    color: #f4d35e;
    font-size: 56px;
    font-weight: 900;
    margin-bottom: 8px;
    letter-spacing: 1px;
}

.main-brand p {
    color: #d7dbe0;
    font-size: 22px;
    margin: 0;
}

.auth-wrapper {
    max-width: 1100px;
    margin: 20px auto 10px auto;
}

.hero-card {
    background: linear-gradient(180deg, rgba(10,25,40,0.96), rgba(6,18,31,0.96));
    border: 1px solid rgba(212,175,55,0.35);
    border-radius: 28px;
    padding: 35px 30px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
    min-height: 520px;
}

.hero-title {
    color: #f4d35e;
    font-size: 42px;
    font-weight: 800;
    line-height: 1.3;
    margin-bottom: 16px;
}

.hero-text {
    color: #d9dfe7;
    font-size: 18px;
    line-height: 1.9;
    margin-bottom: 12px;
}

.feature-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(212,175,55,0.18);
    border-radius: 18px;
    padding: 14px 16px;
    margin-bottom: 12px;
    color: #e8edf5;
    font-size: 16px;
}

.auth-card {
    background: rgba(7, 20, 33, 0.96);
    border: 1px solid rgba(212,175,55,0.42);
    border-radius: 28px;
    padding: 28px 24px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
}

.card-title {
    color: #f4d35e;
    font-size: 28px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 8px;
}

.card-subtitle {
    color: #d6dce5;
    font-size: 15px;
    text-align: center;
    margin-bottom: 18px;
}

.metric-card {
    background: linear-gradient(180deg, #0d2742, #0a1f34);
    border: 1px solid rgba(212,175,55,0.35);
    border-radius: 24px;
    padding: 24px;
    text-align: center;
    color: white;
    min-height: 170px;
    box-shadow: 0 14px 30px rgba(0,0,0,0.22);
}

.metric-card h3 {
    font-size: 22px;
    margin-bottom: 16px;
    color: #f7f7f7;
}

.metric-card h1 {
    font-size: 42px;
    color: #f4d35e;
    margin: 0;
}

.section-box {
    background: rgba(7, 20, 33, 0.95);
    border: 1px solid rgba(212,175,55,0.30);
    border-radius: 24px;
    padding: 20px;
    margin-top: 15px;
    margin-bottom: 15px;
}

.small-card {
    background: linear-gradient(180deg, #102b47, #0b2034);
    border: 1px solid rgba(212,175,55,0.28);
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 12px;
    color: #f5f6f8;
}

.badge-line {
    background: rgba(212,175,55,0.12);
    border: 1px solid rgba(212,175,55,0.28);
    color: #f4d35e;
    padding: 10px 14px;
    border-radius: 999px;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 14px;
}

div[data-testid="stForm"] {
    border: none !important;
    background: transparent !important;
}

div.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(90deg, #d4af37, #f4d35e);
    color: #08111f !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 14px !important;
    min-height: 46px !important;
}

div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    filter: brightness(1.04);
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
textarea {
    border-radius: 14px !important;
}

.block-title {
    color: #f4d35e;
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 10px;
}

hr {
    border-color: rgba(212,175,55,0.22);
}
</style>
""", unsafe_allow_html=True)


# =========================
# Helpers
# =========================
def set_success(msg: str):
    st.session_state["flash_success"] = msg


def set_error(msg: str):
    st.session_state["flash_error"] = msg


def show_flash_messages():
    if st.session_state.get("flash_success"):
        st.success(st.session_state["flash_success"])
        st.session_state["flash_success"] = None

    if st.session_state.get("flash_error"):
        st.error(st.session_state["flash_error"])
        st.session_state["flash_error"] = None


def decode_jwt_payload(token: str):
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return {}

        payload_b64 = parts[1]
        padding = "=" * (-len(payload_b64) % 4)
        decoded = base64.urlsafe_b64decode(payload_b64 + padding)
        return json.loads(decoded.decode("utf-8"))
    except Exception:
        return {}


def get_headers():
    token = st.session_state.get("token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def check_backend():
    try:
        response = requests.get(f"{API_URL}/", timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False


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


def do_logout():
    st.session_state["logged_in"] = False
    st.session_state["token"] = None
    st.session_state["user_email"] = None
    st.session_state["user_role"] = None


def get_role_label(role: str):
    mapping = {
        "client": "عميل",
        "lawyer": "محامٍ",
        "admin": "إدارة"
    }
    return mapping.get(role, role)


# =========================
# Header
# =========================
st.markdown("""
<div class="main-brand">
    <h1>LEGAL MARKETPLACE</h1>
    <p>منصة قانونية رقمية احترافية بإشراف المستشار صبري رضوان</p>
</div>
""", unsafe_allow_html=True)

backend_ok = check_backend()
if not backend_ok:
    st.error("الـ Backend غير شغال. شغّل FastAPI أولًا بالأمر: uvicorn app.main:app --reload")
    st.stop()


# =========================
# Authentication Screen
# =========================
if not st.session_state["logged_in"]:
    show_flash_messages()

    left_col, right_col = st.columns([1.2, 1], gap="large")

    with left_col:
        st.markdown("""
        <div class="hero-card">
            <div class="hero-title">منظومة قانونية رقمية بمستوى مؤسسي</div>
            <div class="hero-text">
                تربط بين العملاء والمحامين داخل بيئة احترافية آمنة، مع تنظيم القضايا حسب التخصص،
                وإدارة العروض القانونية، وبنية تشغيل قابلة للتوسع.
            </div>
            <div class="feature-box">⚖️ إدارة طلبات الاستشارات والقضايا بشكل منظم</div>
            <div class="feature-box">🧑‍⚖️ توجيه القضايا حسب التخصص القانوني بدقة</div>
            <div class="feature-box">📑 استقبال عروض المحامين ومقارنتها</div>
            <div class="feature-box">🔐 تشغيل آمن وهوية بصرية احترافية</div>
            <div class="feature-box">🏛 مناسب للتطوير لاحقًا إلى تطبيق موبايل ومنصة كاملة</div>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        auth_tab_login, auth_tab_register = st.tabs(["تسجيل الدخول", "إنشاء حساب"])

        with auth_tab_login:
            st.markdown("""
            <div class="auth-card">
                <div class="card-title">بوابة الدخول</div>
                <div class="card-subtitle">ادخل إلى لوحة التحكم القانونية الاحترافية</div>
            """, unsafe_allow_html=True)

            with st.form("login_form"):
                login_email = st.text_input("البريد الإلكتروني")
                login_password = st.text_input("كلمة المرور", type="password")
                login_submit = st.form_submit_button("دخول")

                if login_submit:
                    if not login_email.strip() or not login_password.strip():
                        st.error("أدخل البريد الإلكتروني وكلمة المرور")
                    else:
                        response = login_api(login_email.strip(), login_password.strip())

                        if response is None:
                            st.error("تعذر الاتصال بالسيرفر")
                        elif response.status_code == 200:
                            data = response.json()
                            token = data["access_token"]
                            payload = decode_jwt_payload(token)

                            st.session_state["token"] = token
                            st.session_state["logged_in"] = True
                            st.session_state["user_email"] = payload.get("email", login_email.strip())
                            st.session_state["user_role"] = payload.get("role", "client")

                            set_success("تم تسجيل الدخول بنجاح")
                            st.rerun()
                        else:
                            try:
                                msg = response.json().get("detail", "فشل تسجيل الدخول")
                            except Exception:
                                msg = "فشل تسجيل الدخول"
                            st.error(msg)

            st.markdown("</div>", unsafe_allow_html=True)

        with auth_tab_register:
            st.markdown("""
            <div class="auth-card">
                <div class="card-title">إنشاء حساب جديد</div>
                <div class="card-subtitle">سجل كعميل أو محامٍ وابدأ استخدام المنصة</div>
            """, unsafe_allow_html=True)

            with st.form("register_form"):
                reg_full_name = st.text_input("الاسم الكامل")
                reg_email = st.text_input("البريد الإلكتروني")
                reg_password = st.text_input("كلمة المرور", type="password")
                reg_phone = st.text_input("رقم الهاتف")
                reg_role = st.selectbox("نوع الحساب", ["client", "lawyer"])

                reg_specialization = None
                if reg_role == "lawyer":
                    reg_specialization = st.selectbox("التخصص القانوني", SPECIALIZATIONS)

                reg_submit = st.form_submit_button("إنشاء الحساب")

                if reg_submit:
                    if not reg_full_name.strip() or not reg_email.strip() or not reg_password.strip():
                        st.error("أكمل البيانات الأساسية")
                    else:
                        response = register_api(
                            full_name=reg_full_name.strip(),
                            email=reg_email.strip(),
                            password=reg_password.strip(),
                            role=reg_role,
                            specialization=reg_specialization,
                            phone=reg_phone.strip() if reg_phone.strip() else None
                        )

                        if response is None:
                            st.error("تعذر الاتصال بالسيرفر")
                        elif response.status_code == 200:
                            set_success("تم إنشاء الحساب بنجاح. يمكنك الآن تسجيل الدخول.")
                            st.rerun()
                        else:
                            try:
                                msg = response.json().get("detail", "تعذر إنشاء الحساب")
                            except Exception:
                                msg = "تعذر إنشاء الحساب"
                            st.error(msg)

            st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# =========================
# Main App
# =========================
show_flash_messages()

cases = fetch_cases()
user_role = st.session_state.get("user_role", "client")
role_label = get_role_label(user_role)

all_proposals_count = 0
for case in cases:
    all_proposals_count += len(fetch_case_proposals(case["id"]))

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f'<div class="metric-card"><h3>📊 إجمالي القضايا</h3><h1>{len(cases)}</h1></div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="metric-card"><h3>🧾 إجمالي العروض</h3><h1>{all_proposals_count}</h1></div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<div class="metric-card"><h3>👤 نوع الحساب</h3><h1 style="font-size:30px">{role_label}</h1></div>',
        unsafe_allow_html=True
    )

st.markdown(
    f'<div class="badge-line">الحساب الحالي: {st.session_state["user_email"]} | الصفة: {role_label}</div>',
    unsafe_allow_html=True
)


# =========================
# Client View
# =========================
if user_role == "client":
    tab1, tab2 = st.tabs(["إضافة قضية جديدة", "قضاياي والعروض"])

    with tab1:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="block-title">إضافة قضية جديدة</div>', unsafe_allow_html=True)

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
                        set_success("تم إنشاء القضية بنجاح")
                        st.rerun()
                    else:
                        try:
                            msg = response.json().get("detail", "تعذر إنشاء القضية")
                        except Exception:
                            msg = "تعذر إنشاء القضية"
                        st.error(msg)

        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="block-title">قضاياي والعروض</div>', unsafe_allow_html=True)

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

                st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# =========================
# Lawyer View
# =========================
elif user_role == "lawyer":
    tab1, tab2 = st.tabs(["القضايا المتاحة", "تقديم عرض"])

    with tab1:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="block-title">القضايا المناسبة لتخصصك</div>', unsafe_allow_html=True)

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

        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="block-title">تقديم عرض على قضية</div>', unsafe_allow_html=True)

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
                            set_success("تم إرسال العرض بنجاح")
                            st.rerun()
                        else:
                            try:
                                msg = response.json().get("detail", "تعذر إرسال العرض")
                            except Exception:
                                msg = "تعذر إرسال العرض"
                            st.error(msg)

        st.markdown('</div>', unsafe_allow_html=True)


# =========================
# Admin View
# =========================
else:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="block-title">لوحة الإدارة</div>', unsafe_allow_html=True)

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

            st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# Footer
# =========================
st.divider()
if st.button("تسجيل الخروج", use_container_width=True):
    do_logout()
    st.rerun()
