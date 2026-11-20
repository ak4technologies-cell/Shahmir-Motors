import streamlit as st
import os
import json
import urllib.parse

st.set_page_config(
    page_title="Shahmir Motors",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown(
    """
    <style>
   @media (max-width: 768px) {
        .block-container {
            padding-top: 1.2rem !important;
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
        }
        .block-container p,
        .block-container span,
        .block-container label {
            color: #111827 !important;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.35rem !important;
        }
        button[kind="primary"], button[kind="secondary"], .stButton > button {
            min-height: 44px !important;
            font-size: 0.95rem !important;
        }
    }       
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================== ADMIN SECURITY ====================
ADMIN_PASSCODE = "admin123"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 12% 8%, rgba(239, 68, 68, 0.08), transparent 34%),
            radial-gradient(circle at 88% 12%, rgba(59, 130, 246, 0.08), transparent 36%),
            linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }

    /* New-Gen Digital Hero Banner */
    .sm-header {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #090d16 0%, #161f33 48%, #7f1d1d 100%);
        border: 1px solid rgba(255, 255, 255, 0.14);
        box-shadow: 0 22px 45px -15px rgba(15, 23, 42, 0.45);
        padding: 28px 32px;
        border-radius: 22px;
        color: #ffffff;
        margin-bottom: 18px;
    }
    .sm-badge {
        display: inline-block;
        background: rgba(239, 68, 68, 0.22);
        border: 1px solid rgba(248, 113, 113, 0.45);
        color: #fecaca;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 5px 12px;
        border-radius: 999px;
        margin-bottom: 10px;
    }
    .sm-header h1 {
        color: #ffffff;
        margin: 0;
        font-size: 2.15rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    .sm-sub {
        color: #e2e8f0;
        margin: 8px 0 14px 0;
        font-size: 1rem;
        line-height: 1.55;
        max-width: 880px;
    }
    .sm-meta {
        display: inline-block;
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #fde68a;
        font-size: 0.9rem;
        font-weight: 600;
        padding: 8px 14px;
        border-radius: 12px;
    }

    /* Metric Cards Styling */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 18px;
        padding: 16px 20px;
        box-shadow: 0 10px 24px -12px rgba(15, 23, 42, 0.14);
    }
    [data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #475569;
    }
    [data-testid="stMetricValue"] {
        font-weight: 800;
        color: #0f172a;
    }

    /* Price Pill */
    .sm-price {
        display: inline-block;
        font-size: 1.12rem;
        font-weight: 800;
        color: #dc2626;
        background: #fef2f2;
        border: 1px solid #fecaca;
        padding: 4px 12px;
        border-radius: 10px;
        margin: 6px 0 10px 0;
    }

    /* Team Card */
    .team-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-left: 4px solid #ef4444;
        padding: 12px 14px;
        border-radius: 14px;
        margin-bottom: 8px;
        box-shadow: 0 6px 16px -10px rgba(15, 23, 42, 0.18);
    }
    .team-name {
        font-weight: 700;
        color: #0f172a;
        font-size: 0.95rem;
        margin: 0;
    }
    .team-phone {
        color: #dc2626;
        font-weight: 700;
        font-size: 0.88rem;
        margin: 3px 0 0 0;
    }

    /* New-Gen Buttons & Link Buttons */
    .stButton > button,
    [data-testid="stLinkButton"] > a {
        border-radius: 999px !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em !important;
        padding: 0.55rem 1.15rem !important;
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        box-shadow: 0 10px 20px -8px rgba(220, 38, 38, 0.55) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover,
    [data-testid="stLinkButton"] > a:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 14px 26px -8px rgba(220, 38, 38, 0.72) !important;
        filter: brightness(1.05);
    }
    .stButton > button:active,
    [data-testid="stLinkButton"] > a:active {
        transform: translateY(0px) scale(0.99) !important;
    }

    /* Bordered Vehicle Cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        background: rgba(255, 255, 255, 0.92) !important;
        border: 1px solid rgba(148, 163, 184, 0.24) !important;
        box-shadow: 0 12px 28px -14px rgba(15, 23, 42, 0.18) !important;
        transition: transform 0.22s ease, box-shadow 0.22s ease !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 36px -14px rgba(15, 23, 42, 0.25) !important;
    }

    /* Rounded Images */
    [data-testid="stImage"] img {
        border-radius: 14px;
    }
    </style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "shahmir_cars.json")
IMAGE_DIR = os.path.join(BASE_DIR, "car_images")
TEAM_IMAGE = os.path.join(BASE_DIR, "team.jpg")

TEAM_MEMBERS = [
    {"name": "SHAFIQ KHAN", "display_phone": "0334-9510205", "wa": "923349510205"},
    {"name": "MUHAMMAD KHAN", "display_phone": "0333-5003222", "wa": "923335003222"},
    {"name": "SHAHBAZ KHAN", "display_phone": "0301-5124347", "wa": "923015124347"},
]

os.makedirs(IMAGE_DIR, exist_ok=True)


def _index_repo_images():
    """Scan BASE_DIR and IMAGE_DIR so images work whether in root or car_images/."""
    found = {}
    search_dirs = [IMAGE_DIR, BASE_DIR]
    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}
    for folder in search_dirs:
        if os.path.isdir(folder):
            for fname in os.listdir(folder):
                full_p = os.path.join(folder, fname)
                if os.path.isfile(full_p):
                    ext = os.path.splitext(fname)[1].lower()
                    if ext in valid_exts:
                        found.setdefault(fname.lower(), full_p)
    return found


def resolve_image_path(img_path):
    if not img_path:
        return None
    raw_str = str(img_path)
    base_name = os.path.basename(raw_str)
    candidates = [
        raw_str,
        os.path.join(BASE_DIR, raw_str),
        os.path.join(IMAGE_DIR, base_name),
        os.path.join(BASE_DIR, base_name),
    ]
    for p in candidates:
        if os.path.exists(p) and os.path.isfile(p):
            return p

    repo_map = _index_repo_images()
    if base_name.lower() in repo_map:
        return repo_map[base_name.lower()]
    return None


def load_cars():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            if "images" not in item:
                single = item.get("image")
                item["images"] = [single] if single else []
        return data
    return []


def save_cars(cars_data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cars_data, f, indent=4, ensure_ascii=False)


cars = load_cars()

if "selected_car_id" not in st.session_state:
    st.session_state.selected_car_id = None
if "active_page" not in st.session_state:
    st.session_state.active_page = "home"
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "editing_car_id" not in st.session_state:
    st.session_state.editing_car_id = None


def go_home():
    st.session_state.selected_car_id = None
    st.session_state.editing_car_id = None
    st.session_state.active_page = "home"


def go_add():
    st.session_state.selected_car_id = None
    st.session_state.editing_car_id = None
    st.session_state.active_page = "add"


# ==================== LEFT SIDEBAR ====================
st.sidebar.title("⚡ Shahmir Motors")
st.sidebar.caption("Lehtrar Road, Near Paracha Chok, Islamabad")

if st.sidebar.button("🏠 Home (Showroom & Fleet)", use_container_width=True):
    go_home()
    st.rerun()

if st.sidebar.button("➕ Add New Vehicle", use_container_width=True):
    go_add()
    st.rerun()

st.sidebar.divider()
st.sidebar.subheader("🔐 Admin Access (Edit / Delete)")

if not st.session_state.is_admin:
    with st.sidebar.form("admin_login_form", clear_on_submit=True):
        pass_input = st.text_input("Admin Password", type="password", placeholder="Password enter karein...")
        unlock_btn = st.form_submit_button("🔓 Unlock Admin", use_container_width=True)
        if unlock_btn:
            if pass_input == ADMIN_PASSCODE:
                st.session_state.is_admin = True
                st.success("Admin access unlocked!")
                st.rerun()
            else:
                st.error("Galat password! Sirf admin edit/delete kar sakta hai.")
else:
    st.sidebar.success("🟢 Admin Mode Active (Edit & Delete Enabled)")
    if st.sidebar.button("🔒 Lock Admin Mode", use_container_width=True):
        st.session_state.is_admin = False
        st.session_state.editing_car_id = None
        st.rerun()

st.sidebar.divider()
st.sidebar.subheader("👥 Our Team")

team_img_resolved = resolve_image_path(TEAM_IMAGE)
if team_img_resolved:
    st.sidebar.image(team_img_resolved, use_container_width=True)

for member in TEAM_MEMBERS:
    st.sidebar.markdown(f"""
        <div class="team-card">
            <p class="team-name">{member['name']}</p>
            <p class="team-phone">📞 {member['display_phone']}</p>
        </div>
    """, unsafe_allow_html=True)
    wa_url = f"https://wa.me/{member['wa']}?text={urllib.parse.quote('Assalam-o-Alaikum ' + member['name'] + ', Shahmir Motors se maloomat chahiye.')}"
    st.sidebar.link_button(f"💬 WhatsApp {member['name'].split()[0]}", wa_url, use_container_width=True)

st.sidebar.divider()
st.sidebar.caption("Services: Sale & Purchase • Rent A Car • Tour & Travels • Real Estate")

# ==================== MAIN HEADER ====================
st.markdown("""
    <div class="sm-header">
        <div class="sm-badge">✨ Digital Showroom • All Pakistan Fleet</div>
        <h1>🚗 SHAHMIR MOTORS</h1>
        <div class="sm-sub">Tour & Travels • Real Estate — Pakistan ke tamam shehron ke liye gariyan rent par dastiyab hain, aur choti bari gariyon ki kharid-o-farokht ka ba-aitmad idara.</div>
        <div class="sm-meta">📍 Lehtrar Road, Near Paracha Chok, Islamabad &nbsp;|&nbsp; 📞 0334-9510205 • 0333-5003222 • 0301-5124347</div>
    </div>
""", unsafe_allow_html=True)

# Top Quick Home / Add Bar
nav1, nav2, nav3 = st.columns([1.3, 1.4, 3.3])
with nav1:
    if st.button("🏠 Home", key="top_home_btn", use_container_width=True):
        go_home()
        st.rerun()
with nav2:
    if st.button("➕ Add Vehicle", key="top_add_btn", use_container_width=True):
        go_add()
        st.rerun()

# Metrics Row
sale_count = sum(1 for c in cars if c.get("category") == "For Sale" and c.get("status", "Available") == "Available")
rent_count = sum(1 for c in cars if c.get("category") == "Rent A Car" and c.get("status", "Available") == "Available")
m1, m2, m3 = st.columns(3)
m1.metric("Total Vehicles", len(cars))
m2.metric("Available for Sale", sale_count)
m3.metric("Available for Rent", rent_count)

st.divider()

# ==================== PAGE ROUTING ====================
if st.session_state.active_page == "add":
    st.subheader("➕ Nayi Gari Add Karein")

    with st.form("add_vehicle_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Gari ka Naam (e.g., Toyota Corolla XLi)")
            category = st.selectbox("Category", ["For Sale", "Rent A Car"])
            model = st.text_input("Model Year (e.g., 2013)")
            price = st.text_input("Price / Rent Rate (e.g., 25.5 Lac ya 8,000/day)")
        with c2:
            status = st.selectbox("Status", ["Available", "Booked / Sold"])
            mileage = st.text_input("Mileage (e.g., 85,000 km)")
            color = st.text_input("Color (e.g., White)")
            registration = st.text_input("Registration / City (e.g., Punjab / Islamabad)")

        uploaded_files = st.file_uploader(
            "Gari ki Tasweerein Upload Karein (Ek ya zyada select karein)",
            type=["jpg", "png", "jpeg", "webp"],
            accept_multiple_files=True
        )
        details = st.text_area("Mazeed Tafseelat (Condition, Seals, Touching, Engine, Documents, etc.)")
        submitted = st.form_submit_button("💾 Save Vehicle", use_container_width=True)

        if submitted:
            if not name or not uploaded_files:
                st.error("Baraye meharbani gari ka naam aur kam az kam ek tasweer lazmi add karein.")
            else:
                next_id = max([c.get("id", 0) for c in cars], default=0) + 1
                saved_images = []
                for idx_img, up_file in enumerate(uploaded_files, start=1):
                    safe_name = f"car{next_id}_{idx_img}_{up_file.name}"
                    img_path = os.path.join(IMAGE_DIR, safe_name)
                    with open(img_path, "wb") as f:
                        f.write(up_file.getbuffer())
                    saved_images.append(os.path.join("car_images", safe_name))

                new_car = {
                    "id": next_id,
                    "name": name.strip(),
                    "category": category,
                    "model": model.strip() or "N/A",
                    "price": price.strip() or "On Call",
                    "status": status,
                    "mileage": mileage.strip() or "N/A",
                    "color": color.strip() or "N/A",
                    "registration": registration.strip() or "Islamabad",
                    "details": details.strip() or "Rabta karein: 0334-9510205 / 0333-5003222 / 0301-5124347",
                    "images": saved_images
                }
                cars.append(new_car)
                save_cars(cars)
                st.success(f"✅ {new_car['name']} ({len(saved_images)} photos ke sath) add ho gayi hai!")

    if st.button("🏠 Back to Home", key="add_bottom_home"):
        go_home()
        st.rerun()

elif st.session_state.selected_car_id is not None:
    selected_car = next((c for c in cars if c.get("id") == st.session_state.selected_car_id), None)

    if selected_car is None:
        go_home()
        st.rerun()

    # Top action row
    if st.session_state.is_admin:
        b1, b2, b3 = st.columns([1.6, 1.6, 2.8])
    else:
        b1, b3 = st.columns([1.8, 4.2])

    with b1:
        if st.button("🏠 Back to Home", key="detail_top_home", use_container_width=True):
            go_home()
            st.rerun()

    if st.session_state.is_admin:
        with b2:
            if st.button("✏️ Edit Vehicle", key="detail_edit_btn", use_container_width=True):
                st.session_state.editing_car_id = selected_car.get("id")
                st.rerun()
        with b3:
            if st.button("🗑️ Delete Vehicle", key="detail_delete_btn"):
                cars = [c for c in cars if c.get("id") != selected_car.get("id")]
                save_cars(cars)
                go_home()
                st.rerun()
    else:
        with b3:
            st.caption("🔒 Edit & Delete sirf Admin password enter karne ke baad sidebar se unlock honge.")

    # Admin Edit Mode Form
    if st.session_state.is_admin and st.session_state.editing_car_id == selected_car.get("id"):
        st.divider()
        st.subheader(f"✏️ Edit Vehicle — {selected_car['name']}")

        existing_imgs = selected_car.get("images", [])
        keep_imgs = st.multiselect(
            "Mojooda Tasweerein Rakhein (Jo hatani ho unhein unselect karein)",
            options=existing_imgs,
            default=existing_imgs
        )

        with st.form("edit_vehicle_form"):
            ec1, ec2 = st.columns(2)
            with ec1:
                e_name = st.text_input("Gari ka Naam", value=selected_car.get("name", ""))
                cat_options = ["For Sale", "Rent A Car"]
                cur_cat = selected_car.get("category", "For Sale")
                e_cat = st.selectbox("Category", cat_options, index=cat_options.index(cur_cat) if cur_cat in cat_options else 0)
                e_model = st.text_input("Model Year", value=selected_car.get("model", ""))
                e_price = st.text_input("Price / Rent Rate", value=selected_car.get("price", ""))
            with ec2:
                st_options = ["Available", "Booked / Sold"]
                cur_st = selected_car.get("status", "Available")
                e_status = st.selectbox("Status", st_options, index=st_options.index(cur_st) if cur_st in st_options else 0)
                e_mileage = st.text_input("Mileage", value=selected_car.get("mileage", ""))
                e_color = st.text_input("Color", value=selected_car.get("color", ""))
                e_reg = st.text_input("Registration / City", value=selected_car.get("registration", ""))

            new_photos = st.file_uploader(
                "Mazeed Tasweerein Add Karein (Optional)",
                type=["jpg", "png", "jpeg", "webp"],
                accept_multiple_files=True
            )
            e_details = st.text_area("Mazeed Tafseelat", value=selected_car.get("details", ""))

            save_edit_btn = st.form_submit_button("💾 Update Vehicle Changes", use_container_width=True)
            if save_edit_btn:
                updated_img_list = list(keep_imgs)
                for idx_img, up_file in enumerate(new_photos or [], start=1):
                    safe_name = f"car{selected_car.get('id')}_edit_{idx_img}_{up_file.name}"
                    img_path = os.path.join(IMAGE_DIR, safe_name)
                    with open(img_path, "wb") as f:
                        f.write(up_file.getbuffer())
                    updated_img_list.append(os.path.join("car_images", safe_name))

                for c in cars:
                    if c.get("id") == selected_car.get("id"):
                        c["name"] = e_name.strip() or c.get("name", "")
                        c["category"] = e_cat
                        c["model"] = e_model.strip() or "N/A"
                        c["price"] = e_price.strip() or "On Call"
                        c["status"] = e_status
                        c["mileage"] = e_mileage.strip() or "N/A"
                        c["color"] = e_color.strip() or "N/A"
                        c["registration"] = e_reg.strip() or "Islamabad"
                        c["details"] = e_details.strip()
                        c["images"] = updated_img_list
                        break

                save_cars(cars)
                st.session_state.editing_car_id = None
                st.success("✅ Gari ki details update ho gayi hain!")
                st.rerun()

        if st.button("❌ Cancel Edit", key="cancel_edit_btn"):
            st.session_state.editing_car_id = None
            st.rerun()

    st.divider()
    st.subheader(f"{selected_car['name']} ({selected_car['model']})")

    img_col, info_col = st.columns([1.3, 1])
    valid_imgs = [
        resolved
        for p in selected_car.get("images", [])
        if (resolved := resolve_image_path(p)) is not None
    ]

    with img_col:
        if valid_imgs:
            photo_labels = [f"Photo {i + 1}" for i in range(len(valid_imgs))]
            selected_idx = st.selectbox(
                "Tasweer Select Karein",
                options=range(len(valid_imgs)),
                format_func=lambda i: photo_labels[i]
            )
            st.image(valid_imgs[selected_idx], use_container_width=True)

            if len(valid_imgs) > 1:
                st.caption(f"All Photos ({len(valid_imgs)}):")
                thumb_cols = st.columns(min(4, len(valid_imgs)))
                for i, img_p in enumerate(valid_imgs):
                    with thumb_cols[i % len(thumb_cols)]:
                        st.image(img_p, caption=f"#{i + 1}", use_container_width=True)
        else:
            st.info("Tasweer mojood nahi hai.")

    with info_col:
        st.markdown(f"<div class='sm-price'>{selected_car['price']}</div>", unsafe_allow_html=True)
        st.write(f"**Category:** {selected_car.get('category', 'For Sale')}")
        st.write(f"**Status:** {selected_car.get('status', 'Available')}")
        st.write(f"**Model:** {selected_car['model']}")
        st.write(f"**Mileage:** {selected_car['mileage']}")
        st.write(f"**Color:** {selected_car['color']}")
        st.write(f"**Registration / City:** {selected_car.get('registration', 'Islamabad')}")

        st.divider()
        st.write("**Details:**")
        st.write(selected_car["details"])

        st.write("**Contact Team on WhatsApp:**")
        msg = (
            f"Assalam-o-Alaikum Shahmir Motors, mujhe {selected_car['name']} "
            f"({selected_car['model']}) [{selected_car.get('category', 'For Sale')} - {selected_car['price']}] "
            f"ke baray mein maloomat chahiye."
        )
        w_cols = st.columns(3)
        for i, member in enumerate(TEAM_MEMBERS):
            with w_cols[i]:
                link = f"https://wa.me/{member['wa']}?text={urllib.parse.quote(msg)}"
                st.link_button(f"💬 {member['name'].split()[0]}", link, use_container_width=True)

    st.divider()
    if st.button("🏠 Back to Home", key="detail_bottom_home", use_container_width=True):
        go_home()
        st.rerun()

else:
    if not cars:
        st.info("Abhi koi gari add nahi ki gayi. Upar **➕ Add Vehicle** button par click kar ke gariyan add karein.")
    else:
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1:
            search_q = st.text_input("🔍 Search Car / Model", placeholder="Corolla, Civic, Prado, Coaster, 2013...")
        with f2:
            cat_filter = st.selectbox("Category", ["All", "For Sale", "Rent A Car"])
        with f3:
            status_filter = st.selectbox("Status", ["All", "Available", "Booked / Sold"])

        filtered = []
        for c in cars:
            q_ok = (
                not search_q
                or search_q.lower() in c.get("name", "").lower()
                or search_q.lower() in str(c.get("model", "")).lower()
            )
            c_ok = cat_filter == "All" or c.get("category", "For Sale") == cat_filter
            s_ok = status_filter == "All" or c.get("status", "Available") == status_filter
            if q_ok and c_ok and s_ok:
                filtered.append(c)

        filtered = list(reversed(filtered))

        if not filtered:
            st.warning("Is filter ke mutabiq koi gari nahi mili.")
        else:
            cols = st.columns(3)
            for idx, car in enumerate(filtered):
                with cols[idx % 3]:
                    with st.container(border=True):
                        imgs = [
                            resolved
                            for p in car.get("images", [])
                            if (resolved := resolve_image_path(p)) is not None
                        ]
                        if imgs:
                            st.image(imgs[0], use_container_width=True)
                        st.markdown(f"**{car['name']}** ({car['model']})")
                        st.markdown(f"<div class='sm-price'>{car['price']}</div>", unsafe_allow_html=True)
                        photo_badge = f" • 📷 {len(imgs)} Photos" if imgs else ""
                        st.caption(
                            f"{car.get('category', 'For Sale')}  •  {car.get('status', 'Available')}  •  "
                            f"{car.get('registration', 'Islamabad')}{photo_badge}"
                        )

                        if st.button("View Details →", key=f"car_{car['id']}", use_container_width=True):
                            st.session_state.selected_car_id = car["id"]
                            st.rerun()
