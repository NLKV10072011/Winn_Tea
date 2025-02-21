import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config("Trà Sữa Toca", "🍹", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .header { color: #ff4b4b; }
    .highlight { color: #ff4b4b; font-weight: bold; }
    .success-box { background-color: #dfffdf; padding: 20px; border-radius: 10px; }
    .price { color: #666; font-size: 0.9em; }
    .footer { text-align: center; padding: 20px; color: #666; }
</style>
""", unsafe_allow_html=True)

# Danh sách sản phẩm
milk_tea = {
    "🧉 Hồng Trà Sữa Kim Tuyên": 35000,
    "🧉 Oolong Sữa Túc Tắc": 40000,
    "🧉 Trà Sữa Hồng Kông Phô Mai Tươi": 45000,
    "🧉 Trà Sữa Hồng Kông": 30000
}

fruit_tea = {
    "🍋 Hồng Trà Chanh Mật Ong": 30000,
    "🍓 Hồng Trà Trân Châu": 35000,
    "🍑 Trà Đào": 40000,
    "🍇 Trà Mận Hoa Hồng": 45000,
    "🍒 Trà Vải Lài": 40000,
    "🍵 Trà Xanh Lài": 35000
}

topping_prices = {
    "🍑 Đào Lát (3 lát)": 7000,
    "🍵 Oolong Mochi": 10000,
    "🧀 Phô Mai Tươi": 15000,
    "🍮 Sương Sáo": 5000,
    "☕ Thạch Cà Phê": 10000,
    "🥥 Thạch Coco": 10000,
    "🔹 Trân Châu Đen": 10000,
    "⚪ Trân Châu Trắng": 10000,
    "🍈 Vải Trái (2 trái)": 15000
}

st.title("🍹 Trà Sữa Toca - Đặt Hàng Online")
st.markdown("---")

tab1, tab2 = st.tabs(["🛒 Đặt Hàng", "💳 Thanh Toán"])

with tab1:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("1. Chọn Đồ Uống")
        drink_type = st.radio(
            "Loại đồ uống:",
            ["Trà Sữa 🧋", "Trà Trái Cây 🍹"],
            horizontal=True
        )
        
        # Hiển thị đồ uống kèm giá
        if drink_type == "Trà Sữa 🧋":
            drinks = list(milk_tea.items())
            display_options = [f"{name} - {price:,.0f} VNĐ" for name, price in drinks]
            selected = st.selectbox("Chọn đồ uống:", range(len(display_options)), 
                            format_func=lambda x: display_options[x])
            drink, base_price = drinks[selected]
        else:
            drinks = list(fruit_tea.items())
            display_options = [f"{name} - {price:,.0f} VNĐ" for name, price in drinks]
            selected = st.selectbox("Chọn đồ uống:", range(len(display_options)), 
                            format_func=lambda x: display_options[x])
            drink, base_price = drinks[selected]
        
        st.subheader("2. Tuỳ Chọn")
        col_size, col_num = st.columns(2)
        with col_size:
            # Hiển thị giá từng size
            size_multiplier = {"Nhỏ": 0.9, "Vừa": 1.0, "Lớn": 1.2}
            size_prices = {size: base_price * mult for size, mult in size_multiplier.items()}
            size = st.radio(
                "Size:",
                options=list(size_multiplier.keys()),
                index=1,
                format_func=lambda x: f"{x} ({size_prices[x]:,.0f} VNĐ)"
            )
        with col_num:
            quantity = st.number_input("Số lượng:", 1, 10, 1)
        
        st.subheader("3. Topping")
        # Hiển thị topping kèm giá
        toppings = [
            f"{name} - {price:,.0f} VNĐ" 
            for name, price in topping_prices.items()
        ]
        selected_toppings = st.multiselect(
            "Thêm topping (tuỳ chọn):", 
            toppings
        )
        # Lọc tên topping từ lựa chọn
        toppings = [t.split(" - ")[0] for t in selected_toppings]
        total_topping = sum(topping_prices[t.split(" - ")[0]] for t in selected_toppings)
        
    with col2:
        st.subheader("4. Thông Tin Giao Hàng")
        address = st.text_input("Địa chỉ nhận hàng:")
        delivery_time = st.time_input("Thời gian giao hàng:")
        
        st.subheader("📝 Tóm Tắt Đơn Hàng")
        # Tính toán giá
        size_price = size_prices[size]
        total_price = (size_price + total_topping) * quantity
        
        st.markdown(f"""
        - **Đồ uống:** {drink} ({size})
        - **Topping:** {', '.join(toppings) if toppings else 'Không có'}
        - **Số lượng:** {quantity}
        - **Thành tiền:** {total_price:,.0f} VNĐ
        """)
        
        if st.button("📥 Đặt Hàng", type="primary", use_container_width=True):
            if not address.strip():
                st.error("Vui lòng nhập địa chỉ giao hàng!")
            else:
                st.session_state.order = {
                    "drink": drink,
                    "size": size,
                    "toppings": toppings,
                    "quantity": quantity,
                    "address": address,
                    "delivery_time": delivery_time.strftime("%H:%M"),
                    "original_total_price": total_price,
                    "total_price": total_price,
                    "discount_applied": None
                }
                st.success("Đặt hàng thành công! Vui lòng chuyển sang tab Thanh Toán.")

with tab2:
    if "order" not in st.session_state:
        st.warning("Vui lòng đặt hàng trước khi thanh toán")
    else:
        order = st.session_state.order
        st.subheader("💳 Phương Thức Thanh Toán")
        
        # Discount code section
        with st.expander("🎁 Áp dụng mã giảm giá"):
            discount_code = st.text_input("Nhập mã giảm giá:")
            if st.button("Áp dụng mã"):
                valid_codes = {
                    "TOCA10": 0.1,
                    "FREESHIP": 20000,
                    "TEA20": 0.2
                }
                # Reset về giá gốc trước khi áp dụng mã mới
                order["total_price"] = order["original_total_price"]
                order["discount_applied"] = None
                
                if discount_code in valid_codes:
                    discount = valid_codes[discount_code]
                    original_total = order["original_total_price"]
                    
                    if isinstance(discount, float):
                        new_total = original_total * (1 - discount)
                        new_total = int(round(new_total))
                    else:
                        new_total = original_total - discount
                    
                    new_total = max(new_total, 0)  # Đảm bảo không âm
                    order["total_price"] = new_total
                    order["discount_applied"] = discount_code
                    st.success(f"Áp dụng thành công! Tổng cộng: {new_total:,.0f} VNĐ")
                else:
                    st.error("Mã không hợp lệ")
        
        st.markdown(f"""
        ### Tổng thanh toán
        **{order['total_price']:,.0f} VNĐ**
        """)
        
        payment_method = st.radio(
            "Chọn phương thức:",
            ["Momo", "ZaloPay", "Chuyển khoản ngân hàng", "Tiền mặt khi nhận hàng"]
        )
        
        if payment_method in ["Momo", "ZaloPay"]:
            # Tạo QR code động
            qr_data = {
                "Momo": f"https://momo.vn?amount={order['total_price']}",
                "ZaloPay": f"zalopay://payment?amount={order['total_price']}"
            }[payment_method]
            
            qr = qrcode.make(qr_data)
            img_bytes = BytesIO()
            qr.save(img_bytes, format="PNG")
            
            col_qr, col_info = st.columns([1, 3])
            with col_qr:
                st.image(img_bytes.getvalue(), caption=f"{payment_method} QR", width=200)
            with col_info:
                st.markdown(f"""
                ### Hướng dẫn:
                1. Mở ứng dụng {payment_method}
                2. Quét mã QR
                3. Xác nhận thanh toán **{order['total_price']:,.0f} VNĐ**
                """)
        
        # Nút tải hóa đơn
        receipt = f"""
        === HÓA ĐƠN TOCA TEA ===
        
        Món đã đặt: {order['drink']} ({order['size']})
        Topping: {', '.join(order['toppings']) if order['toppings'] else 'Không có'}
        Số lượng: {order['quantity']}
        Thời gian giao: {order['delivery_time']}
        Địa chỉ: {order['address']}
        Mã giảm giá: {order.get('discount_applied', 'Không có')}
        ----------------------------------
        TỔNG CỘNG: {order['total_price']:,.0f} VNĐ
        """
        st.download_button("📥 Tải hóa đơn", receipt, file_name="Toca_Tea_Receipt.txt")
        
        if st.button("✅ Xác Nhận Thanh Toán", type="primary"):
            st.balloons()
            st.success("Thanh toán thành công! Đơn hàng đang được chuẩn bị...")
            del st.session_state.order

st.markdown("---")
st.markdown("""
<div class="footer">
    © 2024 Trà Sữa Toca - Hotline: 1900 9999
</div>
""", unsafe_allow_html=True)