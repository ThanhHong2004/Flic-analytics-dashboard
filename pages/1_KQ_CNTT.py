import streamlit as st
import pandas as pd
import plotly.express as px
from scripts.ketnoi_sql import get_connection
st.set_page_config(layout="wide", page_title="FLIC Dashboard - Kết quả CNTT")

COLOR_ORANGE_CHAY = "#DD730F"  
COLOR_VSTEP_BLUE = "#0047AB"   
COLOR_TEXT_WHITE = "#FFFFFF"   
COLOR_BG_KEM = "#FCF8F2"       

st.markdown(f"""
    <style>
        /* A. NỀN CHÍNH: Màu kem phẳng */
        .stApp {{
            background-color: {COLOR_BG_KEM} !important;
            background-image: none !important;
        }}

        /* B. SIDEBAR: Xanh VSTEP & Chữ trắng in đậm toàn bộ */
        [data-testid="stSidebar"] {{
            background-color: {COLOR_VSTEP_BLUE} !important;
            background-image: none !important;
        }}
        
        /* Cải thiện: Ép tất cả các thẻ chữ, nhãn, và nội dung radio trong Sidebar sang TRẮNG */
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {{
            color: {COLOR_TEXT_WHITE} !important;
            font-weight: 900 !important;
            text-shadow: none !important;
        }}

        /* Đảm bảo các icon SVG (mũi tên, lịch...) cũng màu trắng */
        [data-testid="stSidebar"] svg {{
            fill: {COLOR_TEXT_WHITE} !important;
        }}

        /* C. METRICS: */
        .flic-metric-card {{
            background: {COLOR_ORANGE_CHAY} !important;
            padding: 15px 5px !important;
            border-radius: 15px !important;
            text-align: center !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
            min-height: 120px !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            margin-bottom: 15px !important;
        }}

        .flic-metric-label {{
            color: white !important;
            font-weight: 900 !important;
            font-size: 1.0rem !important;
            text-transform: uppercase !important;
        }}

        .flic-metric-value {{
            color: white !important;
            font-weight: 900 !important;
            font-size: 2.1rem !important;
        }}

        /* D. CHỮ Ở NỀN CHÍNH: Màu CAM CHÁY */
        /* Loại trừ sidebar để không bị ghi đè màu trắng đã thiết lập ở trên */
        .main .stMarkdown, .main .stText, .main h1, .main h2, .main h3, .main p, .main label, .main .stSelectbox label p {{
            color: {COLOR_ORANGE_CHAY} !important;
        }}

        /* E. FOOTER ĐỊNH DANH: Võ Thanh Hồng - 48K29.1 */
        .footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            color: {COLOR_ORANGE_CHAY}; 
            text-align: right;
            padding: 10px 20px;
            font-size: 0.8rem;
            font-style: italic;
            font-weight: bold;
            z-index: 100;
            background-color: transparent;
        }}
    </style>
    <div class="footer">
        Sinh viên thực hiện: Võ Thanh Hồng | Lớp: 48K29.1 | DUE - FLIC
    </div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(query):
    try:
        conn = get_connection()
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Lỗi truy vấn SQL: {e}")
        return pd.DataFrame()

def get_unique_list(query, column_name):
    df = load_data(query)
    if not df.empty:
        return sorted(df[column_name].dropna().unique().tolist())
    return []

main_query = """
    SELECT
        f.idThiSinh, s.HoTen, f.KetQua, f.idChuongTrinh, k.KhoaHoc, d.TenKhoa, d.TenNganh,
        s.DoiTuong, s.idHV,
        s.NoiSinh,
        l.NgayThi, l.Thang, l.TenQuy, l.TenDotThi, YEAR(l.NgayThi) AS Nam,
        N'Cơ bản' as LoaiChungChi,
        f.DiemLT as LT, f.DiemTH as TH,
        NULL as W_LT, NULL as W_TH, NULL as E_LT, NULL as E_TH, NULL as P_LT, NULL as P_TH
    FROM Fact_KQCB f
    JOIN Dim_KhoaHoc k ON f.idKhoaHoc = k.idKhoaHoc
    JOIN Dim_Khoa d ON f.idKhoa = d.idKhoa
    JOIN Dim_ThiSinh s ON f.idThiSinh = s.idThiSinh
    JOIN Dim_LichThi l ON f.idLichThi = l.idLichThi
    UNION ALL
    SELECT
        f.idThiSinh, s.HoTen, f.KetQua, f.idChuongTrinh, k.KhoaHoc, d.TenKhoa, d.TenNganh,
        s.DoiTuong, s.idHV,
        s.NoiSinh,
        l.NgayThi, l.Thang, l.TenQuy, l.TenDotThi, YEAR(l.NgayThi) AS Nam,
        N'Nâng cao' as LoaiChungChi,
        NULL as LT, NULL as TH,
        f.W_LT, f.W_TH, f.E_LT, f.E_TH, f.P_LT, f.P_TH
    FROM Fact_KQNC f
    JOIN Dim_KhoaHoc k ON f.idKhoaHoc = k.idKhoaHoc
    JOIN Dim_Khoa d ON f.idKhoa = d.idKhoa
    JOIN Dim_ThiSinh s ON f.idThiSinh = s.idThiSinh
    JOIN Dim_LichThi l ON f.idLichThi = l.idLichThi
"""
df_raw = load_data(main_query)

with st.sidebar:
    with st.sidebar:
        st.markdown(
            """
            <style>
                [data-testid="stSidebar"] [data-testid="stImage"] {
                    display: flex;
                    justify-content: center;
                    margin-left: auto;
                    margin-right: auto;
                    width: 50%;
                }
                [data-testid="stSidebar"] [data-testid="stImage"] img {
                    max-width: 50px; /
                }
            </style>
            """,
            unsafe_allow_html=True
        )
    st.image("Logo_FLIC.png")
    df_raw['NgayThi'] = pd.to_datetime(df_raw['NgayThi'])
    min_date, max_date = df_raw['NgayThi'].min().date(), df_raw['NgayThi'].max().date()
    date_range = st.date_input("Thời gian:", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    sel_khoa = st.selectbox("Khoa:", ["Tất cả"] + get_unique_list("SELECT DISTINCT TenKhoa FROM Dim_Khoa", "TenKhoa"))
    sel_nganh = st.selectbox("Ngành:", ["Tất cả"] + get_unique_list("SELECT DISTINCT TenNganh FROM Dim_Khoa", "TenNganh"))
    sel_khoahoc = st.selectbox("Khóa học:", ["Tất cả"] + get_unique_list("SELECT DISTINCT KhoaHoc FROM Dim_KhoaHoc", "KhoaHoc"))
    query_dotthi = "SELECT DISTINCT TenDotThi FROM Dim_LichThi"
    sel_dotthi = st.selectbox("Đợt thi:", ["Tất cả"] + get_unique_list(query_dotthi, "TenDotThi"))
    query_doituong = "SELECT DISTINCT DoiTuong FROM Dim_ThiSinh"
    sel_doituong = st.selectbox("Đối tượng:", ["Tất cả"] + get_unique_list(query_doituong, "DoiTuong"))
    cert_type = st.radio("Chứng chỉ:", ["Tất cả", "Cơ bản", "Nâng cao"], horizontal=True)

df_filtered = df_raw.copy()
if not df_filtered.empty:
    if isinstance(date_range, tuple) and len(date_range) == 2:
        df_filtered = df_filtered[(df_filtered['NgayThi'].dt.date >= date_range[0]) & (df_filtered['NgayThi'].dt.date <= date_range[1])]
    if cert_type != "Tất cả": df_filtered = df_filtered[df_filtered['LoaiChungChi'] == cert_type]
    if sel_khoa != "Tất cả": df_filtered = df_filtered[df_filtered['TenKhoa'] == sel_khoa]
    if sel_khoahoc != "Tất cả": df_filtered = df_filtered[df_filtered['KhoaHoc'] == sel_khoahoc]
    if sel_doituong != "Tất cả": df_filtered = df_filtered[df_filtered['DoiTuong'] == sel_doituong]
    if sel_nganh != "Tất cả": df_filtered = df_filtered[df_filtered['TenNganh'] == sel_nganh]
    if sel_dotthi != "Tất cả": df_filtered = df_filtered[df_filtered['TenDotThi'] == sel_dotthi]
    
st.markdown(f"""
<style>
    /* Khung chứa Metric: Chuyển sang nền XANH VSTEP */
    .flic-metric-card {{
        background: {COLOR_VSTEP_BLUE} !important; /* Sử dụng màu xanh biến đã thiết lập */
        padding: 15px 5px !important; 
        border-radius: 15px !important;
        text-align: center !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        min-height: 120px !important; 
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        margin-bottom: 15px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }}

    /* Tiêu đề Metric: Chữ TRẮNG cực đậm */
    .flic-metric-label {{
        color: {COLOR_TEXT_WHITE} !important;
        font-weight: 900 !important;   
        font-size: 1.0rem !important;  
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin-bottom: 8px !important;
        line-height: 1.2 !important;   
    }}

    /* Con số hiển thị: Chuyển từ Navy sang TRẮNG */
    .flic-metric-value {{
        color: {COLOR_TEXT_WHITE} !important;
        font-weight: 900 !important;
        font-size: 2.1rem !important; 
        margin: 0 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important; /* Thêm bóng nhẹ cho số nổi bật */
    }}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <span style="color: {COLOR_ORANGE_CHAY}; font-weight: 900; font-size: 1.5rem; line-height: 1.4;">
            KẾT QUẢ SÁT HẠCH CÔNG NGHỆ THÔNG TIN TẠI TRUNG TÂM NGOẠI NGỮ - TIN HỌC, <br> 
            TRƯỜNG ĐẠI HỌC KINH TẾ - ĐẠI HỌC ĐÀ NẴNG (FLIC)
        </span>
    </div>
""", unsafe_allow_html=True)

if not df_filtered.empty:
    df_calc = df_filtered.copy()
    df_calc['idThiSinh'] = df_calc['idThiSinh'].fillna(0).astype(int).astype(str).str.strip()
    df_calc = df_calc[df_calc['idThiSinh'] != '0']
    df_calc['KetQua'] = df_calc['KetQua'].astype(str).str.strip()
    
    df_calc = df_calc.sort_values(by=['idThiSinh', 'NgayThi'])
    df_calc['IsReExam'] = (df_calc['idChuongTrinh'] == 17) | \
                          (df_calc.duplicated(subset=['idThiSinh', 'LoaiChungChi'], keep='first'))

    total_reg = len(df_calc)                        
    mask_participated = ~df_calc['KetQua'].str.contains('Vắng', case=False, na=False)
    part_count = len(df_calc[mask_participated])
    rate_p = (part_count / total_reg * 100) if total_reg > 0 else 0
    re_count = df_calc['IsReExam'].sum()
    rate_re = (re_count / total_reg * 100) if total_reg > 0 else 0

# Biểu đồ hàng 1
    m1, m2, m3 = st.columns(3)
    
    metrics_data = [
        ("TỔNG LƯỢT ĐĂNG KÝ", f"{total_reg:,}", "Tổng số lượt đăng ký ghi nhận"),
        ("TỶ LỆ THAM GIA", f"{rate_p:.2f}%", f"Cụ thể: {part_count} lượt có mặt"),
        ("TỶ LỆ THI LẠI", f"{rate_re:.2f}%", f"Gồm {re_count} lượt đăng ký thi lại")
    ]

    for col, (label, value, tooltip) in zip([m1, m2, m3], metrics_data):
        with col:
            st.markdown(f'''
                <div class="flic-metric-card" title="{tooltip}">
                    <div class="flic-metric-label">{label}</div>
                    <div class="flic-metric-value">{value}</div>
                </div>
            ''', unsafe_allow_html=True)

# Biểu đồ hàng thứ hai
    st.markdown("---")
    CHART_HEIGHT = 400
    c1, c2= st.columns(2)
    with c1:
        st.markdown(f"<p style='text-align: center;font-weight: bold;color: {COLOR_ORANGE_CHAY};'>PHÂN BỔ NƠI SINH</p>", unsafe_allow_html=True)
        if 'NoiSinh' in df_filtered.columns and 'idThiSinh' in df_filtered.columns:
            df_clean = df_filtered.copy()
            df_clean['NoiSinh'] = df_clean['NoiSinh'].astype(str).str.strip()
            df_clean['NoiSinh'] = df_clean['NoiSinh'].replace('Quãng Nam', 'Quảng Nam')
            df_unique = df_clean.drop_duplicates(subset=['idThiSinh'])
            df_bar = df_unique['NoiSinh'].value_counts().reset_index()
            df_bar.columns = ['Tỉnh thành', 'Số lượng']
            fig_bar = px.bar(
                df_bar, x='Tỉnh thành', y='Số lượng', text='Số lượng',
                color='Số lượng',
                color_continuous_scale=['#E3F2FD', COLOR_VSTEP_BLUE],
                template='plotly_white'
            )
            fig_bar.update_traces(
                textposition='outside',
                textfont=dict(color='#DD730F', size=12, weight='bold'),
                hovertemplate="<b>Tỉnh thành:</b> %{x}<br><b>Số lượng:</b> %{y}<extra></extra>"
            )
            fig_bar.update_layout(
                height=CHART_HEIGHT + 100,
                margin=dict(l=40, r=20, t=30, b=50),
                coloraxis_showscale=False,
                xaxis_title=None,
                yaxis_title=None,
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    range=[0, df_bar['Số lượng'].max() * 1.3]
                ),
                xaxis=dict(
                    tickangle=-45,
                    tickfont=dict(color='#DD730F', size=11, weight='bold'),
                    rangeslider=dict(visible=True, thickness=0.05),
                    range=[-0.5, 9.5] if len(df_bar) > 10 else None
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
            
with c2:
        st.markdown(f"<p style='text-align: center; font-weight: bold;color: {COLOR_ORANGE_CHAY};'>TỶ LỆ KẾT QUẢ THI</p>", unsafe_allow_html=True)
        df_pie = df_filtered['KetQua'].value_counts().reset_index()
        df_pie.columns = ['Kết quả', 'Số lượng']
        fig_pie = px.pie(
            df_pie, values='Số lượng', names='Kết quả', hole=0.5,
            color='Kết quả',
            color_discrete_map={'Đạt':'#0047AB', 'Không đạt': '#c30303', 'Vắng thi': "#868381"}
        )
        fig_pie.update_traces(
            textinfo='percent',
            texttemplate='<b>%{percent:.1%}</b>',
            textfont=dict(
                size=11,
                color='#DD730F', 
                family="Arial Black"
            ),
            textposition='outside'
        )
        fig_pie.update_layout(
            height=CHART_HEIGHT+100,
            margin=dict(l=10, r=10, t=50, b=100),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(
                    family="Arial",
                    size=12,
                    color="#DD730F",
                    weight="bold"
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})

#Biểu đồ hàng thứ 3
st.markdown("---")
col_new1, col_new2 = st.columns(2)
with col_new1:
    st.markdown(f"<p style='text-align: center; font-weight: bold; color: {COLOR_ORANGE_CHAY};'>KẾT QUẢ THI THEO NHÓM ĐỐI TƯỢNG</p>", unsafe_allow_html=True)
    df_obj = df_filtered.groupby(['DoiTuong', 'KetQua']).size().reset_index(name='Số lượng')
    fig_obj = px.bar(
        df_obj, x='DoiTuong', y='Số lượng', color='KetQua', barmode='group', text='Số lượng',
        color_discrete_map={'Đạt':'#0047AB', 'Không đạt': "#c30303", 'Vắng thi': '#868381'}
    )
    fig_obj.update_traces(
        textposition='outside',
        cliponaxis=False,
        textfont=dict(size=12, color='#DD730F', weight='bold') # Đã thêm bold
    )
    fig_obj.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(t=50),
        xaxis=dict(
            tickfont=dict(color='#DD730F', size=12, family="Arial", weight='bold')
        ),
        legend=dict(
            title_text='',
            font=dict(color='#DD730F', size=12, weight='bold'),
            orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5
        ),
        yaxis=dict(showticklabels=False, showgrid=False)
    )
    st.plotly_chart(fig_obj, use_container_width=True, config={'displayModeBar': False})

with col_new2:
    st.markdown(f"<p style='text-align: center; font-weight: bold; color: {COLOR_ORANGE_CHAY};'>KẾT QUẢ THI CHI TIẾT THEO KHOA</p>", unsafe_allow_html=True)
    status_options = ['Đạt', 'Không đạt', 'Vắng thi']
    st.markdown("""
    <style>
    .stSelectbox label p {
        size: 14px;
        color: #DD730F;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    selected_status = st.selectbox("Chọn trạng thái hiển thị:", options=status_options, index=0)
    df_khoa = df_filtered.groupby(['TenKhoa', 'KetQua']).size().reset_index(name='Số lượng')
    df_khoa_filtered = df_khoa[df_khoa['KetQua'] == selected_status].sort_values(by='Số lượng', ascending=True)
    fig_khoa = px.bar(
        df_khoa_filtered, 
        x='Số lượng', 
        y='TenKhoa', 
        orientation='h',
        text='Số lượng',
        color='Số lượng', 
        color_continuous_scale=['#BBDEFB', COLOR_VSTEP_BLUE] 
    )
    fig_khoa.update_traces(
        textposition='outside',
        cliponaxis=False,
        textfont=dict(size=12, color='#DD730F', weight='bold')
    )

    fig_khoa.update_layout(
        coloraxis_showscale=False,
        height=max(400, len(df_khoa_filtered) * 30), 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(t=20, l=150),
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(
            tickfont=dict(color='#DD730F', size=12, family="Arial", weight='bold')
        )
    )

    st.plotly_chart(fig_khoa, use_container_width=True, config={'displayModeBar': False})
def phan_loai(diem):
    if pd.isna(diem): return None
    if diem >= 9.5: return 'Xuất sắc'
    if diem >= 8.0: return 'Giỏi'
    if diem >= 6.5: return 'Khá'
    return 'Trung bình'

color_map_rank = {
    'Xuất sắc': "#c30303", 
    'Giỏi': '#38A169',    
    'Khá': '#0047AB',     
    'Trung bình': "#7a7a77" 
}


st.markdown("---")
st.markdown(f"<h3 style='text-align: center; color: {COLOR_ORANGE_CHAY}; margin-bottom: 25px;'>PHÂN HẠNG NĂNG LỰC THÍ SINH ĐẠT CHUẨN THEO PHÂN KHÚC KỸ NĂNG</h3>", unsafe_allow_html=True)
color_map_rank = {
    'Xuất sắc': '#c30303',
    'Giỏi': '#38A169',      
    'Khá': '#0047AB',      
    'Trung bình': '#7a7a77'
}
if not df_filtered.empty:
    df_passed = df_filtered[df_filtered['KetQua'] == 'Đạt'].copy()
    if cert_type in ["Cơ bản", "Nâng cao"]:
        if df_passed.empty:
            st.warning("Không có dữ liệu thí sinh 'Đạt' để phân tích năng lực.")
        else:
            prefix = ""
            if cert_type == "Nâng cao":
                module_sel = st.radio("Chọn Module phân tích:", ["Word", "Excel", "PowerPoint"], horizontal=True)
                prefix = module_sel[0]
            c1, c2 = st.columns(2, gap="large")
            for col_ui, kieu, label in zip([c1, c2], ['LT', 'TH'], ['Lý thuyết', 'Thực hành']):
                with col_ui:
                    col_target = f"{prefix}_{kieu}" if cert_type == "Nâng cao" else kieu
                    if col_target in df_passed.columns:
                        st.markdown(f"<p style='text-align: center; font-weight: bold; color: #DD730F; margin-bottom: 0px; font-size: 18px;'>{label}</p>", unsafe_allow_html=True)
                        df_passed['Rank'] = df_passed[col_target].apply(phan_loai)
                        df_rank = df_passed.groupby('Rank').agg(
                            count=('idThiSinh', 'size'),
                            names=('idThiSinh', lambda x: ", ".join(x.head(5).astype(str)) + ("..." if len(x) > 5 else ""))
                        ).reindex(['Xuất sắc', 'Giỏi', 'Khá', 'Trung bình']).reset_index()
                        df_rank['count'] = df_rank['count'].fillna(0)
                        fig = px.bar(
                            df_rank, x='Rank', y='count',
                            color='Rank', color_discrete_map=color_map_rank,
                            text='count',
                            custom_data=['names']
                        )                        
                        fig.update_traces(
                            textposition='outside',
                            cliponaxis=False,
                            textfont=dict(
                                size=14,
                                color='#DD730F',
                                family="Arial",
                                weight='bold' 
                            ),
                            marker_line_width=0,
                            hovertemplate="<b>Hạng: %{x}</b><br>Số lượng: %{y}<br>DS: %{customdata[0]}<extra></extra>"
                        )
                        fig.update_layout(
                            height=400,
                            bargap=0.2,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            xaxis_title=None,
                            yaxis_title=None,
                            showlegend=True,
                            margin=dict(l=10, r=10, t=50, b=80),
                            legend=dict(
                                font=dict(size=12, color='#DD730F', family="Arial", weight='bold'),
                                orientation="h",
                                yanchor="bottom",
                                y=-0.3,
                                xanchor="center",
                                x=0.5,
                                title=None
                            ),
                            yaxis=dict(
                                showticklabels=True,
                                tickfont=dict(color='#DD730F', size=11, weight='bold'),
                                showgrid=True,
                                gridcolor='rgba(200, 200, 200, 0.2)', 
                                fixedrange=True
                            ),
                            xaxis=dict(
                                showticklabels=False,
                                fixedrange=True,
                                showgrid=False
                            )
                        )
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
st.markdown(f"""
    <style>
    /* Đổi màu tiêu đề của Expander */
    .st-emotion-cache-p4mowd p {{
        color: #3b5998 !important;
        font-weight: bold !important;
    }}
    /* Đổi màu icon mũi tên của Expander */
    .st-emotion-cache-p4mowd svg {{
        fill: #3b5998 !important;
    }}

    /* Màu nhãn (Label) của selectbox bên trong */
    [data-testid="stWidgetLabel"] p {{
        color: #3b5998 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Biểu đồ hàng thú 5: Chi tiết danh sách---

with st.expander("XEM DANH SÁCH THÍ SINH ĐẠT CHI TIẾT"):
    col_filter1, col_filter2 = st.columns([1, 2])
    with col_filter1:
        view_mode = st.selectbox(
            "Chọn dữ liệu hiển thị:",
            ["Lý thuyết", "Thực hành"],
            key="view_mode_detail"
        )
    st.markdown(f"<p style='color: #DD730F; font-size: 0.85rem;'>Đang hiển thị danh sách xếp loại dựa trên điểm <b>{view_mode}</b>.</p>", unsafe_allow_html=True)
    kieu_sel = 'LT' if view_mode == "Lý thuyết" else 'TH'
    col_final = f"{prefix}_{kieu_sel}" if cert_type == "Nâng cao" else kieu_sel
    df_detail = df_passed.copy()
    df_detail['Rank_Detail'] = df_detail[col_final].apply(phan_loai)
    cols_detail = st.columns(4)
    ranks = ['Xuất sắc', 'Giỏi', 'Khá', 'Trung bình']
    rank_icons = {'Xuất sắc': '🏆', 'Giỏi': '🌟', 'Khá': '📘', 'Trung bình': '📙'}

    for i, r in enumerate(ranks):
        with cols_detail[i]:
            df_rank_r = df_detail[df_detail['Rank_Detail'] == r]
            ds_hien_thi = (df_rank_r['idHV'].astype(str) + " - " + df_rank_r['HoTen']).tolist()
            st.markdown(f"<p style='color: #DD730F; font-weight: bold; margin-bottom: 8px;'>{rank_icons[r]} {r} ({len(ds_hien_thi)})</p>", unsafe_allow_html=True)
            if ds_hien_thi:
                list_html = "".join([
                    f"<li style='font-size: 0.82rem; color: #3b5998; margin-bottom: 4px;'>{item}</li>"
                    for item in ds_hien_thi
                ])
                st.markdown(f"""
                    <div style="background-color: #F8FAFC; padding: 12px; border-radius: 10px;
                                border-left: 5px solid {color_map_rank[r]}; max-height: 400px; overflow-y: auto;
                                box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.05);">
                        <ul style="margin: 0; padding-left: 25px; list-style-type: decimal; color: #DD730F;">
                            {list_html}
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown("<p style='color: #3b5998; font-size: 0.8rem; font-style: italic;'>Chưa có dữ liệu</p>", unsafe_allow_html=True)