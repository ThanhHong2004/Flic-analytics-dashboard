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
        /* 1. MÀU NỀN */
        .stApp {{
            background-color: {COLOR_BG_KEM} !important;
            background-attachment: fixed;
        }}

        /* 2. SIDEBAR */
        [data-testid="stSidebar"] {{
            background-color: {COLOR_VSTEP_BLUE} !important;
            background-image: none !important;
            border-right: 1px solid rgba(255,255,255,0.1);
        }}
        
        [data-testid="stSidebar"] .stMarkdown p, 
        [data-testid="stSidebar"] span, 
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] div p,
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
            color: {COLOR_TEXT_WHITE} !important; 
            font-weight: 900 !important;
            text-decoration: none;
        }}
        [data-testid="stSidebar"] [data-testid="stImage"] {{
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }}
        [data-testid="stSidebar"] [data-testid="stImage"] img {{
            max-width: 150px;
        }}

        /* 3. CÁC THẺ METRIC*/
        [data-testid="stMetric"] {{
            background-color: {COLOR_VSTEP_BLUE} !important;
            padding: 20px !important;
            border-radius: 15px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
        }}

        /* Tiêu đề Metric*/
        [data-testid="stMetricLabel"] p {{
            color: {COLOR_TEXT_WHITE} !important;
            font-weight: 900 !important;   
            font-size: 1.0rem !important;  
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin-bottom: 8px !important;
            line-height: 1.2 !important;
            display: flex !important;
            justify-content: center !important;
            text-align: center !important;
        }}

        /* Con số trong Metric */
        [data-testid="stMetricValue"] div {{
            color: {COLOR_TEXT_WHITE} !important;
            font-weight: 900 !important;
            font-size: 1.5rem !important; 
            margin: 0 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
            display: flex !important;
            justify-content: center !important;
            text-align: center !important;
        }}
        [data-testid="stMetric"] > div {{
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        /* 4. TIÊU ĐỀ CHÍNH*/
        .main-title {{
            text-align: center;
            color: {COLOR_ORANGE_CHAY} !important;
            font-size: 26px;
            font-weight: 900;
            text-transform: uppercase;
            margin-bottom: 30px;
        }}
        
        /* 5. ĐƯỜNG KẺ NGANG & EXPANDER */
        hr {{ border-color: {COLOR_ORANGE_CHAY} !important; }}
        
        .stDetails summary p {{
            color: {COLOR_ORANGE_CHAY} !important;
            font-weight: 900 !important;
        }}

        /* SỬA LỖI Ở ĐÂY: Chỉ ép màu trắng cho văn bản nằm TRONG Sidebar */
        [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] > p {{
            color: {COLOR_TEXT_WHITE} !important;
            font-weight: 900 !important;
        }}

        /* Đảm bảo tiêu đề biểu đồ (ngoài Sidebar) không bị ảnh hưởng */
        .main-container p {{
            color: inherit; 
        }}
    </style>
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
        f.idThiSinh, 
        f.KetQua, 
        k.KhoaHoc, 
        d.TenKhoa, 
        d.TenNganh, 
        s.DoiTuong,
        l.NgayThi, 
        l.MaDotThi, 
        ct.TenChuongTrinh, 
        ct.LoaiChuongTrinh, 
        ct.GiaTien, 
        'CB' as Nguon 
    FROM Fact_KQCB f 
    JOIN Dim_ThiSinh s ON f.idThiSinh = s.idThiSinh 
    JOIN Dim_Khoa d ON f.idKhoa = d.idKhoa 
    JOIN Dim_KhoaHoc k ON f.idKhoaHoc = k.idKhoaHoc 
    JOIN Dim_LichThi l ON f.idLichThi = l.idLichThi 
    JOIN Dim_ChuongTrinh ct ON f.idChuongTrinh = ct.idChuongTrinh

    UNION ALL

    SELECT 
        f.idThiSinh, 
        f.KetQua, 
        k.KhoaHoc, 
        d.TenKhoa, 
        d.TenNganh, 
        s.DoiTuong, 
        l.NgayThi, 
        l.MaDotThi, 
        ct.TenChuongTrinh, 
        ct.LoaiChuongTrinh, 
        ct.GiaTien,
        'NC' as Nguon
    FROM Fact_KQNC f
    JOIN Dim_ThiSinh s ON f.idThiSinh = s.idThiSinh 
    JOIN Dim_Khoa d ON f.idKhoa = d.idKhoa
    JOIN Dim_KhoaHoc k ON f.idKhoaHoc = k.idKhoaHoc
    JOIN Dim_LichThi l ON f.idLichThi = l.idLichThi
    JOIN Dim_ChuongTrinh ct ON f.idChuongTrinh = ct.idChuongTrinh
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
    min_d, max_d = df_raw['NgayThi'].min().date(), df_raw['NgayThi'].max().date()
    
    date_range = st.date_input("Thời gian:", value=(min_d, max_d), min_value=min_d, max_value=max_d)
    sel_khoa = st.selectbox("Khoa:", ["Tất cả"] + get_unique_list("SELECT DISTINCT TenKhoa FROM Dim_Khoa", "TenKhoa"))
    sel_nganh = st.selectbox("Ngành:", ["Tất cả"] + get_unique_list("SELECT DISTINCT TenNganh FROM Dim_Khoa", "TenNganh"))
    sel_khoahoc = st.selectbox("Khóa học:", ["Tất cả"] + get_unique_list("SELECT DISTINCT KhoaHoc FROM Dim_KhoaHoc", "KhoaHoc"))
    query_dt = "SELECT DISTINCT DoiTuong FROM Dim_ThiSinh"
    sel_doituong = st.selectbox("Đối tượng:", ["Tất cả"] + get_unique_list(query_dt, "DoiTuong"))
    query_dotthi = "SELECT DISTINCT TenDotThi FROM Dim_LichThi"
    sel_dotthi = st.selectbox("Đợt thi:", ["Tất cả"] + get_unique_list(query_dotthi, "TenDotThi"))
    cert_type = st.radio("Chứng chỉ:", ["Tất cả", "Cơ bản", "Nâng cao"], horizontal=True)

df_filtered = df_raw.copy()
if not df_filtered.empty:
    df_filtered['GiaTien'] = pd.to_numeric(df_filtered['GiaTien'], errors='coerce').fillna(0)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        df_filtered = df_filtered[(df_filtered['NgayThi'].dt.date >= date_range[0]) & (df_filtered['NgayThi'].dt.date <= date_range[1])]
    if cert_type == "Cơ bản":
        df_filtered = df_filtered[df_filtered['Nguon'] == 'CB']
    elif cert_type == "Nâng cao":
        df_filtered = df_filtered[df_filtered['Nguon'] == 'NC']
    if sel_khoa != "Tất cả": df_filtered = df_filtered[df_filtered['TenKhoa'] == sel_khoa]
    if sel_nganh != "Tất cả": df_filtered = df_filtered[df_filtered['TenNganh'] == sel_nganh]
    if sel_khoahoc != "Tất cả": df_filtered = df_filtered[df_filtered['KhoaHoc'] == sel_khoahoc]
    if sel_doituong != "Tất cả": df_filtered = df_filtered[df_filtered['DoiTuong'] == sel_doituong]
    if sel_dotthi != "Tất cả": df_filtered = df_filtered[df_filtered['TenDotThi'] == sel_dotthi]

st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <span style="color: {COLOR_ORANGE_CHAY}; font-weight: 900; font-size: 1.5rem; line-height: 1.4;">
            HIỆU QUẢ KINH DOANH CÔNG NGHỆ THÔNG TIN TẠI TRUNG TÂM NGOẠI NGỮ - TIN HỌC, <br> 
            TRƯỜNG ĐẠI HỌC KINH TẾ - ĐẠI HỌC ĐÀ NẴNG (FLIC)
        </span>
    </div>
""", unsafe_allow_html=True)

if not df_filtered.empty:
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("TỔNG LƯỢT ĐĂNG KÝ", f"{len(df_filtered):,}")
    with m2: st.metric("TỔNG DOANH THU", f"{df_filtered['GiaTien'].sum():,.0f} VND")

    df_cb_only = df_filtered[df_filtered['Nguon'] == 'CB']
    df_nc_only = df_filtered[df_filtered['Nguon'] == 'NC']
    with m3: st.metric("DOANH THU TB CƠ BẢN", f"{df_cb_only['GiaTien'].mean():,.0f} VND" if not df_cb_only.empty else "0 VND")
    with m4: st.metric("DOANH THU TB NÂNG CAO", f"{df_nc_only['GiaTien'].mean():,.0f} VND" if not df_nc_only.empty else "0 VND")
    st.markdown("---")

    # 6.2 Hàng biểu đồ 1
    c1, c2 = st.columns([6,4])
    with c1:
        st.markdown(f"<p style='text-align: center; font-weight: bold; color: {COLOR_ORANGE_CHAY}; font-size: 16px;'>DOANH THU CHI TIẾT THEO CHƯƠNG TRÌNH</p>", unsafe_allow_html=True)
        df_plot = df_filtered.groupby('TenChuongTrinh').agg(
            DoanhThu=('GiaTien', 'sum'),
            SoLuotDK=('idThiSinh', 'count')
        ).reset_index().sort_values(by='DoanhThu', ascending=True)
    
        fig = px.bar(
            df_plot, 
            x='DoanhThu', 
            y='TenChuongTrinh', 
            orientation='h', 
            text='DoanhThu', 
            color='DoanhThu', 
            color_continuous_scale=['#BBDEFB', COLOR_VSTEP_BLUE],
            hover_data={'TenChuongTrinh': True, 'DoanhThu': ':,.0f} VND', 'SoLuotDK': True}
        )
    
        fig.update_traces(
            hovertemplate="<b>Chương trình:</b> %{y}<br>" +
                      "<b>Doanh thu:</b> %{x:,.0f} VND<br>" +
                      "<b>Lượt đăng ký:</b> %{customdata[0]} lượt<extra></extra>",
            texttemplate='%{text:,.0f} VND', 
            textposition='outside', 
            textfont=dict(color='#DD730F', size=13, weight='bold')
        )

        max_val = df_plot['DoanhThu'].max() if not df_plot.empty else 0
        fig.update_xaxes(range=[0, max_val * 1.5])
    
        fig.update_layout(
            height=max(450, len(df_plot)*35), 
            xaxis_title=None, 
            yaxis_title=None, 
            coloraxis_showscale=False, 
            yaxis=dict(tickfont=dict(color='#DD730F', size=12, weight='bold')), 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown(f"<p style='text-align: center; font-weight: bold; color: {COLOR_ORANGE_CHAY}; font-size: 16px;'>TỶ TRỌNG DOANH THU THEO ĐỐI TƯỢNG</p>", unsafe_allow_html=True)
        df_pie = df_filtered.groupby('DoiTuong')['GiaTien'].sum().reset_index()
        fig_pie = px.pie(df_pie, values='GiaTien', names='DoiTuong', hole=0.5, color_discrete_sequence=['#0047AB', "#7a7a77", '#38A169', '#eb4b3f'])
        fig_pie.update_traces(textinfo='percent',textposition='outside', textfont=dict(family="Arial",color='#DD730F', size=13, weight='bold'),
                              hovertemplate="<b>DoiTuong</b>: %{label}<br><b>DoanhThu</b>: %{value:,.0f}<extra></extra>")
        fig_pie.update_layout(height=450, legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5, font=dict(color='#DD730F', size=12, weight='bold')), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)

    # Hàng biểu đồ 2
    st.markdown("---")
    c3, c4, c5 = st.columns(3)
    def format_money(val):
        try:
            if pd.isna(val) or val == 0: 
                return "0VND"
            return f"{val:,.0f}VND"
        except:
            return "0VND"

    MONEY_COL = 'GiaTien'

    with c3:
        st.markdown(f"<p style='text-align: center; font-weight: bold; color: {COLOR_ORANGE_CHAY}; font-size: 16px;'>TỔNG SỐ LƯỢT ĐĂNG KÝ THEO KHOA</p>", unsafe_allow_html=True)
        
        df_khoa_cnt = df_filtered.groupby('TenKhoa').agg(
            SoLuong=('idThiSinh', 'count'),
            TongTien=(MONEY_COL, 'sum')
        ).reset_index().sort_values(by='SoLuong', ascending=True)
        
        fig_khoa = px.bar(
            df_khoa_cnt, x='SoLuong', y='TenKhoa', orientation='h',
            text='SoLuong', 
            color='SoLuong',
            color_continuous_scale=['#BBDEFB', COLOR_VSTEP_BLUE]
        )
        
        fig_khoa.update_traces(
            textposition='outside', cliponaxis=False,
            textfont=dict(size=12, color='#DD730F', weight='bold'),
            customdata=df_khoa_cnt['TongTien'].apply(format_money),
            hovertemplate="<b>Khoa:</b> %{y}<br><b>Số lượt:</b> %{x}<br><b>Doanh thu:</b> %{customdata}<extra></extra>"
        )
        
        fig_khoa.update_layout(
            height=500, xaxis_title=None, yaxis_title=None, coloraxis_showscale=False,
            margin=dict(l=150, r=50), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showticklabels=False, showgrid=False, range=[0, df_khoa_cnt['SoLuong'].max() * 1.2]),
            yaxis=dict(tickfont=dict(size=12, color='#DD730F', weight='bold'))
        )
        st.plotly_chart(fig_khoa, use_container_width=True)

    with c4:
        st.markdown(f"<p style='text-align: center; font-weight: bold; color: {COLOR_ORANGE_CHAY}; font-size: 16px;'>TOP 5 KHÓA HỌC ĐĂNG KÝ NHIỀU NHẤT</p>", unsafe_allow_html=True)
        
        df_kh_all = df_filtered.groupby('KhoaHoc').agg(
            SoLuong=('idThiSinh', 'count'),
            TongTien=(MONEY_COL, 'sum')
        ).reset_index()
        df_kh_all = df_kh_all[~df_kh_all['KhoaHoc'].isin(['Khác', 'NAN', 'nan', None])]
        df_kh_final = df_kh_all.sort_values(by='SoLuong', ascending=False).head(5).sort_values(by='SoLuong', ascending=True)

        fig_kh = px.bar(
            df_kh_final, x='SoLuong', y='KhoaHoc', orientation='h',
            text='SoLuong', color='SoLuong',
            color_continuous_scale=['#BBDEFB', COLOR_VSTEP_BLUE]
        )
        
        fig_kh.update_traces(
            textposition='outside', cliponaxis=False,
            textfont=dict(size=12, weight='bold', color='#DD730F'),
            customdata=df_kh_final['TongTien'].apply(format_money),
            hovertemplate="<b>Khóa:</b> %{y}<br><b>Số lượt:</b> %{x}<br><b>Doanh thu:</b> %{customdata}<extra></extra>"
        )
        
        fig_kh.update_layout(
            height=450, xaxis_title=None, yaxis_title=None, coloraxis_showscale=False,
            margin=dict(l=120, r=50), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showticklabels=False, range=[0, df_kh_final['SoLuong'].max() * 1.2]),
            yaxis=dict(tickfont=dict(size=12, weight='bold', color='#DD730F'))
        )
        st.plotly_chart(fig_kh, use_container_width=True)

    with c5:
        st.markdown(f"<p style='text-align: center; font-weight: bold; color: {COLOR_ORANGE_CHAY}; font-size: 16px;'>TOP 5 CHƯƠNG TRÌNH ĐƯỢC ĐĂNG KÝ NHIỀU NHẤT</p>", unsafe_allow_html=True)
        
        df_top5 = df_filtered.groupby('TenChuongTrinh').agg(
            LuotDK=('idThiSinh', 'count'),
            TongTien=(MONEY_COL, 'sum')
        ).reset_index().sort_values(by='LuotDK', ascending=False).head(5)
        
        max_val = df_top5['LuotDK'].max() if not df_top5.empty else 10

        fig_top5 = px.bar(
            df_top5, x='LuotDK', y='TenChuongTrinh', orientation='h', 
            text='LuotDK', color='LuotDK', 
            color_continuous_scale=['#BBDEFB', COLOR_VSTEP_BLUE]) 

        fig_top5.update_traces(
            textposition='outside', cliponaxis=False,
            textfont=dict(size=11, weight='bold', color='#DD730F'),
            customdata=df_top5['TongTien'].apply(format_money),
            hovertemplate="<b>Chương trình:</b> %{y}<br><b>Lượt DK:</b> %{x}<br><b>Doanh thu:</b> %{customdata}<extra></extra>"
        )    

        fig_top5.update_layout(
            height=450, coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title_text="", showticklabels=False, showgrid=False, range=[0, max_val * 1.3]),   
            yaxis=dict(title_text="", autorange="reversed", tickfont=dict(size=11, weight='bold', color='#DD730F'))
        )
        st.plotly_chart(fig_top5, use_container_width=True)
    # 6.3 Hàng biểu đồ 3
    st.markdown("---")
    c6 = st.columns(1)
    with c6[0]:
        st.markdown(f"<p style='text-align: center; font-weight: bold; color: {COLOR_ORANGE_CHAY}; font-size: 18px;'>Số lượt đăng ký thi lại nâng cao - 1 module</p>", unsafe_allow_html=True)
    
        df_thilai = df_filtered[
            (df_filtered['Nguon'] == 'NC') & 
            (df_filtered['TenChuongTrinh'].str.contains('1 module', na=False, case=False))
        ].copy()

        if not df_thilai.empty:
            pp_ids = [12, 152]
            word_ids = [36, 134]
            excel_ids = [124, 60, 21, 76, 8, 20, 61]

            def hard_code_module(row):
                user_id = row.get('idThiSinh')
                if user_id in pp_ids: return 'PowerPoint'
                if user_id in word_ids: return 'Word'
                if user_id in excel_ids: return 'Excel'
                return 'Khác'

            df_thilai['Module'] = df_thilai.apply(hard_code_module, axis=1)
            df_mod_stats = df_thilai.groupby('Module').agg(
                Số_lượt=('idThiSinh', 'size'),
                Doanh_thu=('GiaTien', 'sum')
            ).reset_index()
        
            order_map = {'Word': 1, 'Excel': 2, 'PowerPoint': 3, 'Khác': 4}
            df_mod_stats['Sort'] = df_mod_stats['Module'].map(order_map)
            df_mod_stats = df_mod_stats.sort_values('Sort')

            fig_mod = px.bar(
                df_mod_stats, x='Module', y='Số_lượt', text='Số_lượt', color='Module',
                custom_data=['Doanh_thu'], 
                color_discrete_map={
                    'Word': '#0047AB', 'Excel': '#38A169', 'PowerPoint': "#bf2207", 'Khác': '#c5c5c5'
                }
            )   
        
            fig_mod.update_traces(
                textposition='outside', 
                textfont=dict(size=14, weight='bold', color='#DD730F'),
                cliponaxis=False,
                hovertemplate="<b>Module</b>: %{x}<br><b>Số lượt</b>: %{y}<br><b>Doanh thu</b>: %{customdata[0]:,.0f} VND<extra></extra>"
            )
        
            fig_mod.update_layout(
                height=450, showlegend=False, xaxis_title=None, yaxis_title=None,
                xaxis=dict(tickfont=dict(size=13, weight='bold', color='#DD730F'),showgrid=False),
                yaxis=dict(showticklabels=False, showgrid=False, range=[0, df_mod_stats['Số_lượt'].max() * 1.5]),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=50)
            )
            st.plotly_chart(fig_mod, use_container_width=True)
        else:
            st.info("Không có dữ liệu thi lại module lẻ.")
else:
    st.warning("Không có dữ liệu phù hợp với bộ lọc hiện tại.")