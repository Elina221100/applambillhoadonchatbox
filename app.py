import streamlit as st
from datetime import datetime
from io import BytesIO

# =========================
# CẤU HÌNH
# =========================
st.set_page_config(
    page_title="Bill Trà Sữa",
    page_icon="🧋",
    layout="centered"
)

# =========================
# DỮ LIỆU MENU
# =========================
MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa khoai môn": 38000,
    "Trà sữa ô long": 40000,
}

TOPPINGS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 6000,
    "Thạch dừa": 5000,
    "Thạch trái cây": 6000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
}

SUGAR_LEVELS = ["100%", "70%", "0%"]
ICE_LEVELS = ["100%", "70%", "0%"]


# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")


# =========================
# TIÊU ĐỀ
# =========================
st.title("🧋 BILL TRÀ SỮA")
st.caption("Ứng dụng tính hóa đơn trà sữa")

st.divider()


# =========================
# THÔNG TIN KHÁCH HÀNG
# =========================
st.subheader("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)


# =========================
# CHỌN MÓN
# =========================
st.subheader("🧋 Chọn trà sữa")

drink = st.selectbox(
    "Loại trà sữa",
    list(MENU.keys())
)

quantity = st.number_input(
    "Số lượng",
    min_value=1,
    max_value=50,
    value=1,
    step=1
)

# =========================
# TOPPING
# =========================
st.subheader("🍡 Chọn topping")

selected_toppings = st.multiselect(
    "Topping",
    list(TOPPINGS.keys()),
    help="Có thể chọn nhiều loại topping"
)


# =========================
# ĐƯỜNG & ĐÁ
# =========================
col1, col2 = st.columns(2)

with col1:
    sugar = st.selectbox(
        "🍬 Mức đường",
        SUGAR_LEVELS
    )

with col2:
    ice = st.selectbox(
        "🧊 Mức đá",
        ICE_LEVELS
    )


# =========================
# TÍNH TIỀN
# =========================
drink_price = MENU[drink]
drink_total = drink_price * quantity

topping_total_one = sum(
    TOPPINGS[topping] for topping in selected_toppings
)

topping_total = topping_total_one * quantity

grand_total = drink_total + topping_total


# =========================
# HIỂN THỊ KẾT QUẢ
# =========================
st.divider()

st.subheader("🧾 Thông tin đơn hàng")

if customer_name.strip():
    st.write(f"**Khách hàng:** {customer_name}")
else:
    st.write("**Khách hàng:** Chưa nhập tên")

st.write(f"**Trà sữa:** {drink}")
st.write(f"**Số lượng:** {quantity}")
st.write(f"**Đơn giá:** {format_money(drink_price)}")

if selected_toppings:
    topping_text = ", ".join(selected_toppings)
    st.write(f"**Topping:** {topping_text}")
else:
    st.write("**Topping:** Không có")

st.write(f"**Mức đường:** {sugar}")
st.write(f"**Mức đá:** {ice}")

st.divider()

st.write(f"**Tiền trà sữa:** {format_money(drink_total)}")
st.write(f"**Tiền topping:** {format_money(topping_total)}")

st.subheader(
    f"💰 Tổng thanh toán: {format_money(grand_total)}"
)


# =========================
# TẠO NỘI DUNG HÓA ĐƠN
# =========================
def create_invoice():
    now = datetime.now()

    topping_text = ", ".join(selected_toppings) \
        if selected_toppings else "Không có"

    invoice = f"""
========================================
          HÓA ĐƠN TRÀ SỮA
========================================

Thời gian: {now.strftime("%d/%m/%Y %H:%M:%S")}

Khách hàng: {customer_name if customer_name.strip() else "Khách lẻ"}

----------------------------------------
THÔNG TIN ĐƠN HÀNG
----------------------------------------

Trà sữa       : {drink}
Số lượng      : {quantity}
Đơn giá       : {format_money(drink_price)}

Topping       : {topping_text}
Mức đường     : {sugar}
Mức đá        : {ice}

----------------------------------------
CHI TIẾT THANH TOÁN
----------------------------------------

Tiền trà sữa  : {format_money(drink_total)}
Tiền topping  : {format_money(topping_total)}

----------------------------------------
TỔNG THANH TOÁN: {format_money(grand_total)}
----------------------------------------

        CẢM ƠN QUÝ KHÁCH!
       HẸN GẶP LẠI ❤️

========================================
"""

    return invoice


# =========================
# THANH TOÁN
# =========================
st.divider()

if st.button(
    "💳 THANH TOÁN",
    type="primary",
    use_container_width=True
):

    if not customer_name.strip():
        st.warning("Vui lòng nhập tên khách hàng trước khi thanh toán.")
    else:
        invoice_content = create_invoice()

        st.success("✅ Thanh toán thành công!")

        st.text_area(
            "🧾 Hóa đơn",
            invoice_content,
            height=450
        )

        # Tạo file để tải xuống
        invoice_bytes = invoice_content.encode("utf-8")

        filename = (
            f"hoa_don_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        st.download_button(
            label="📥 TẢI HÓA ĐƠN",
            data=invoice_bytes,
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )
