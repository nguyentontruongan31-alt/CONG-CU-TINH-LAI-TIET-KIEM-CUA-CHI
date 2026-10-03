# CONG-CU-TINH-LAI-TIET-KIEM-CUA-CHIimport streamlit as st

# 1. Cấu hình trang ứng dụng
st.set_page_config(
    page_title="Tính Lãi Tiết Kiệm - Kiều Nữ Sài Gòn",
    page_icon="💰",
    layout="centered"
)

# 2. Tùy chỉnh CSS giao diện hiện đại & trực quan
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #dfb15b;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #a0aec0;
        font-size: 0.95em;
        margin-bottom: 25px;
    }
    .metric-card {
        background: #1a1e29;
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #2d3748;
        border-left: 5px solid #dfb15b;
        margin-bottom: 15px;
    }
    .metric-label {
        font-size: 0.85em;
        color: #a0aec0;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 1.35em;
        font-weight: bold;
        color: #48bb78;
    }
    .highlight-value {
        color: #dfb15b !important;
    }
    </style>
""", unsafe_style_html=True)

# 3. Tiêu đề ứng dụng
st.markdown("<h1 class='main-title'>🏦 Công Cụ Tính Lãi Gửi Tiết Kiệm</h1>", unsafe_style_html=True)
st.markdown("<p class='sub-title'>Nhà Hàng Kiều Nữ Sài Gòn - Hỗ Trợ Tính Lãi Đơn & Lãi Kép Linh Hoạt</p>", unsafe_style_html=True)
st.write("---")

# 4. Nhập liệu thông tin tính toán
st.subheader("📋 Thông Tin Khoản Gửi")

col1, col2 = st.columns(2)

with col1:
    principal = st.number_input(
        "💰 Số tiền gửi gốc (VNĐ):", 
        min_value=0, 
        value=100000000, 
        step=1000000, 
        format="%d"
    )
    
    interest_rate = st.number_input(
        "📈 Lãi suất (%/năm):", 
        min_value=0.0, 
        max_value=30.0, 
        value=6.5, 
        step=0.1, 
        format="%.2f"
    )

    interest_method = st.radio(
        "⚙️ Phương pháp tính lãi:",
        ["Lãi đơn", "Lãi kép (Tái nhập gốc)"],
        help="Lãi đơn: Tiền lãi không gộp vào gốc. Lãi kép: Tiền lãi định kỳ được cộng dồn vào gốc để tính lãi cho kỳ tiếp theo."
    )

with col2:
    months = st.number_input(
        "📅 Kỳ hạn gửi (tháng):", 
        min_value=1, 
        max_value=360, 
        value=12, 
        step=1
    )
    
    pay_period = st.selectbox(
        "🔄 Hình thức nhận lãi:",
        ["Cuối kỳ", "Hàng tháng", "Hàng quý (3 tháng)"]
    )

# 5. Logic xử lý tính toán Lãi Đơn & Lãi Kép
# Chuyển đổi lãi suất năm -> lãi suất tháng
monthly_rate = (interest_rate / 100) / 12

if interest_method == "Lãi đơn":
    # Công thức Lãi đơn: Tổng lãi = Gốc * (Lãi suất/12) * Số tháng
    total_interest = principal * monthly_rate * months
    total_amount = principal + total_interest

    if pay_period == "Hàng tháng":
        periodic_interest = total_interest / months
        period_label = "Lãi nhận định kỳ (hàng tháng)"
    elif pay_period == "Hàng quý (3 tháng)":
        num_quarters = months / 3
        periodic_interest = (total_interest / months) * 3
        period_label = "Lãi nhận định kỳ (mỗi quý / 3 tháng)"
    else:  # Cuối kỳ
        periodic_interest = total_interest
        period_label = "Lãi nhận khi đáo hạn (cuối kỳ)"

else:
    # Công thức Lãi kép (Compound Interest)
    if pay_period == "Hàng tháng":
        # Ghép lãi hàng tháng: A = P * (1 + r/12)^n
        total_amount = principal * ((1 + monthly_rate) ** months)
        total_interest = total_amount - principal
        
        # Tiền lãi định kỳ tháng đầu tiên
        periodic_interest = principal * monthly_rate
        period_label = "Lãi nhận tháng đầu tiên (tăng dần các tháng sau)"

    elif pay_period == "Hàng quý (3 tháng)":
        # Ghép lãi hàng quý (1 quý = 3 tháng): A = P * (1 + r/4)^(n/3)
        quarterly_rate = (interest_rate / 100) / 4
        quarters = months / 3
        total_amount = principal * ((1 + quarterly_rate) ** quarters)
        total_interest = total_amount - principal
        
        # Tiền lãi định kỳ quý đầu tiên
        periodic_interest = principal * quarterly_rate
        period_label = "Lãi nhận quý đầu tiên (tăng dần các quý sau)"

    else:  # Cuối kỳ
        # Với nhận lãi cuối kỳ thì Lãi kép bằng Lãi đơn (do không rút/tái nhập gốc giữa kỳ)
        total_interest = principal * monthly_rate * months
        total_amount = principal + total_interest
        periodic_interest = total_interest
        period_label = "Lãi nhận khi đáo hạn (cuối kỳ)"

# 6. Hiển thị kết quả tính toán
st.write("---")
st.subheader("📊 Kết Quả Dự Tính Lãi Tiết Kiệm")

res_col1, res_col2 = st.columns(2)

with res_col1:
    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>💵 Số tiền gửi gốc</div>
            <div class='metric-value' style='color: #e2e8f0;'>{principal:,.0f} VNĐ</div>
        </div>
    """, unsafe_style_html=True)

    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>🗓️ {period_label}</div>
            <div class='metric-value'>{periodic_interest:,.0f} VNĐ</div>
        </div>
    """, unsafe_style_html=True)

with res_col2:
    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>🎁 Tổng tiền lãi thu được</div>
            <div class='metric-value'>{total_interest:,.0f} VNĐ</div>
        </div>
    """, unsafe_style_html=True)

    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>💎 Tổng số tiền gốc + tiền lãi</div>
            <div class='metric-value highlight-value'>{total_amount:,.0f} VNĐ</div>
        </div>
    """, unsafe_style_html=True)

# 7. Lưu ý bổ sung
if interest_method == "Lãi kép (Tái nhập gốc)" and pay_period != "Cuối kỳ":
    st.info("💡 **Ghi chú về Lãi kép:** Số tiền lãi định kỳ hiển thị ở trên là của kỳ đầu tiên. Các kỳ tiếp theo, tiền lãi sẽ tự động cộng dồn vào gốc nên tiền lãi nhận được của các kỳ sau sẽ cao hơn kỳ trước.")
else:
    st.caption("💡 *Ghi chú: Kết quả tính toán mang tính chất tham khảo dựa trên công thức chuẩn. Lãi thực tế nhận tại ngân hàng có thể chênh lệch tùy theo số ngày thực tế của từng tháng.*")
