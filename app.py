amlit as st
import datetime

# --- Trang trí & Cấu hình Trang ---
st.set_page_config(page_title="Tính Hóa Đơn Trà Sữa", page_icon="🧋", layout="centered")

st.title("🧋 Ứng Dụng Tính Hóa Đơn Trà Sữa")
st.markdown("Vui lòng nhập thông tin đơn hàng bên dưới:")

# --- Dữ liệu giá cả ---
MENU_TEA = {
    "Trà sữa Truyền thống": 30000,
    "Trà sữa Ô long": 35000,
    "Trà sữa Trái cây (Đào/Vải)": 38000,
    "Trà sữa Matcha": 40000,
    "Trà sữa Hạt dẻ": 42000
}

TOPPING_PRICE = 5000  # Giá mỗi loại topping

# --- Form Nhập Thông Tin ---
with st.form(key="order_form"):
    st.subheader("👤 Thông tin khách hàng")
    customer_name = st.text_input("Tên khách hàng:", value="Khách hàng")

    st.subheader("🧋 Chi tiết món")
    col1, col2 = st.columns(2)
    
    with col1:
        tea_type = st.selectbox("Chọn loại trà sữa:", list(MENU_TEA.keys()))
        sugar = st.radio("Mức độ đường:", ["100%", "70%", "0%"], horizontal=True)
    
    with col2:
        quantity = st.number_input("Số lượng:", min_value=1, max_value=50, value=1, step=1)
        ice = st.radio("Mức độ đá:", ["100%", "70%", "0%"], horizontal=True)

    toppings = st.multiselect(
        "Thêm Topping (5,000 VNĐ / loại):",
        ["Trân châu đen", "Trân châu trắng", "Thạch trái cây", "Pudding trứng", "Kem Cheese"]
    )

    submit_button = st.form_submit_button(label="🛒 Tính hóa đơn")

# --- Xử lý tính toán và hiển thị ---
if submit_button:
    price_per_tea = MENU_TEA[tea_type]
    price_topping = len(toppings) * TOPPING_PRICE
    unit_price = price_per_tea + price_topping
    total_amount = unit_price * quantity
    
    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    st.success("Tạo hóa đơn thành công!")
    st.subheader("📋 Chi Tiết Hóa Đơn")

    # Hiển thị thông tin tổng quan
    st.write(f"**Tên khách hàng:** {customer_name}")
    st.write(f"**Thời gian:** {current_time}")
    st.write(f"**Loại trà sữa:** {tea_type} ({price_per_tea:,} VNĐ)")
    st.write(f"**Số lượng:** {quantity}")
    st.write(f"**Mức đường:** {sugar} | **Mức đá:** {ice}")
    
    if toppings:
        st.write(f"**Topping chọn thêm:** {', '.join(toppings)} (+{price_topping:,} VNĐ/ly)")
    else:
        st.write("**Topping:** Không chọn")

    st.markdown("---")
    st.subheader(f"💰 Tổng tiền thanh toán: {total_amount:,} VNĐ")

    # Nội dung file hóa đơn xuất ra
    receipt_text = f"""===================================
        HÓA ĐƠN TRÀ SỮA
===================================
Khách hàng   : {customer_name}
Thời gian    : {current_time}
-----------------------------------
Món          : {tea_type}
Số lượng     : {quantity}
Mức đường    : {sugar}
Mức đá       : {ice}
Topping      : {', '.join(toppings) if toppings else 'Không có'}
-----------------------------------
Đơn giá ly   : {unit_price:,} VNĐ
TỔNG CỘNG    : {total_amount:,} VNĐ
===================================
Cảm ơn quý khách và hẹn gặp lại!
"""

    # Nút tải file hóa đơn TXT
    st.download_button(
        label="📥 Tải hóa đơn (.txt)",
        data=receipt_text,
        file_name=f"HoaDon_{customer_name.replace(' ', '_')}.txt",
        mime="text/plain"
    )
