import streamlit as st
import os
import json
import urllib.parse

st.set_page_config(
    page_title="Shahmir Motors & Rent A Car",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .sm-header {
        background: linear-gradient(120deg, #991b1b 0%, #dc2626 55%, #1e293b 100%);
        padding: 24px 28px;
        border-radius: 14px;
        color: white;
        margin-bottom: 14px;
    }
    .sm-header h1 {
        color: white;
        margin: 0;
        font-size: 2rem;
    }
    .sm-sub {
        color: #fef2f2;
        margin: 6px 0 10px 0;
        font-size: 1rem;
    }
    .sm-meta {
        color: #fde68a;
        font-size: 0.92rem;
        font-weight: 600;
    }
    .sm-price {
        font-size: 1.15rem;
        font-weight: 700;
        color: #b91c1c;
        margin: 4px 0 8px 0;
    }
    .team-card {
        background-color: #f8fafc;
        border-left: 4px solid #dc2626;
        padding: 10px 12px;
        border-radius: 8px;
        margin-bottom: 8px;
    }
    .team-name {
        font-weight: 700;
        color: #0f172a;
        font-size: 0.95rem;
        margin: 0;
    }
    .team-phone {
        color: #b91c1c;
        font-weight: 600;
        font-size: 0.88rem;
        margin: 2px 0 0 0;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "shahmir_cars.json"
IMAGE_DIR = "car_images"
TEAM_IMAGE = "team.jpg"

TEAM_MEMBERS = [
    {"name": "SHAFIQ KHAN", "display_phone": "0334-9510205", "wa": "923349510205"},
    {"name": "MUHAMMAD KHAN", "display_phone": "0333-5003222", "wa": "923335003222"},
    {"name": "SHAHBAZ KHAN", "display_phone": "0301-5124347", "wa": "923015124347"},
]

os.makedirs(IMAGE_DIR, exist_ok=True)


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


def save_cars(cars):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cars, f, indent=4, ensure_ascii=False)


cars = load_cars()

if "selected_car_id" not in st.session_state:
    st.session_state.selected_car_id = None
if "active_page" not in st.session_state:
    st.session_state.active_page = "home"


def go_home():
    st.session_state.selected_car_id = None
    st.session_state.active_page = "home"


def go_add():
    st.session_state.selected_car_id = None
    st.session_state.active_page = "add"


# ==================== LEFT SIDEBAR ====================
st.sidebar.title("SK • Shahmir Motors")
st.sidebar.caption("Lehtrar Road, Near Paracha Chok, Islamabad")

if st.sidebar.button("🏠 Home (Showroom & Fleet)", use_container_width=True):
    go_home()
    st.rerun()

if st.sidebar.button("➕ Add New Vehicle", use_container_width=True):
    go_add()
    st.rerun()

st.sidebar.divider()
st.sidebar.subheader("👥 Our Team")

if os.path.exists(TEAM_IMAGE):
    st.sidebar.image(TEAM_IMAGE, use_container_width=True)

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
        <h1>🚗 SHAHMIR MOTORS & RENT A CAR</h1>
        <div class="sm-sub">Tour & Travels • Real Estate — Pakistan ke tamam shehron ke liye gariyan rent par dastiyab hain, aur choti bari gariyon ki kharid-o-farokht ka ba-aitmad idara.</div>
        <div class="sm-meta">📍 Lehtrar Road, Near Paracha Chok, Islamabad &nbsp;|&nbsp; 📞 0334-9510205 • 0333-5003222 • 0301-5124347</div>
    </div>
""", unsafe_allow_html=True)

# Top Quick Home / Add Bar
nav1, nav2, nav3 = st.columns([1.2, 1.2, 4])
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
                    saved_images.append(img_path)

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

    b1, b2 = st.columns([1.5, 4.5])
    with b1:
        if st.button("🏠 Back to Home", key="detail_top_home", use_container_width=True):
            go_home()
            st.rerun()
    with b2:
        if st.button("🗑️ Delete Vehicle", type="secondary"):
            cars = [c for c in cars if c.get("id") != selected_car.get("id")]
            save_cars(cars)
            go_home()
            st.rerun()

    st.subheader(f"{selected_car['name']} ({selected_car['model']})")

    img_col, info_col = st.columns([1.3, 1])
    valid_imgs = [p for p in selected_car.get("images", []) if p and os.path.exists(p)]

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
                        imgs = [p for p in car.get("images", []) if p and os.path.exists(p)]
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