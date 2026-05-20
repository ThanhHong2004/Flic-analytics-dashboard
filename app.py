import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide", page_title="FLIC Management System")

COLOR_BG_KEM = "#FCF8F2"       
COLOR_VSTEP_BLUE = "#0047AB"  
COLOR_ORANGE_CHAY = "#DD730F"  
COLOR_TEXT_WHITE = "#FFFFFF"   

st.markdown(f"""
    <style>
        /* 1. Nền chính Dashboard */
        .stApp {{
            background-color: {COLOR_BG_KEM} !important;
            background-image: none !important;
        }}

        /* 2. Sidebar: Màu xanh VSTEP phẳng lì */
        [data-testid="stSidebar"] {{
            background-color: {COLOR_VSTEP_BLUE} !important;
            background-image: none !important;
            box-shadow: none !important;
        }}

        /* 3. CHỮ TRONG SIDEBAR: Màu TRẮNG */
        [data-testid="stSidebarNav"] span, 
        [data-testid="stSidebarNav"] div,
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] label,
        [data-testid="stWidgetLabel"] p,
        [data-testid="stSidebar"] li div span {{
            color: {COLOR_TEXT_WHITE} !important;
            font-weight: bold !important;
        }}

        /* 4. CHỮ Ở NỀN CHÍNH: Màu CAM CHÁY */
        .stMarkdown, .stText, h1, h2, h3, p, label {{
            color: {COLOR_ORANGE_CHAY} !important;
        }}

        /* 5. Khối hướng dẫn Sidebar */
        .sidebar-instruction {{
            background-color: rgba(255, 255, 255, 0.15) !important;
            padding: 15px; 
            border-radius: 10px; 
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-top: 10px;
            color: {COLOR_TEXT_WHITE} !important;
        }}

        /* 6. Footer định danh */
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
        }}
        
        .block-container {{
            padding-top: 3.5rem !important; 
        }}

        [data-testid="stSidebarNav"] svg {{
            fill: {COLOR_TEXT_WHITE} !important;
        }}
    </style>
    
    <div class="footer">
        Sinh viên thực hiện: Võ Thanh Hồng | Lớp: 48K29.1 | DUE - FLIC
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sidebar-instruction">
            <b style="color: {COLOR_TEXT_WHITE};">HƯỚNG DẪN</b><br>
            <span style="font-size: 0.9rem;">Chọn phân hệ bên trái để xem chi tiết dữ liệu.</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='margin: 20px 0; border: 0.5px solid rgba(255,255,255,0.3);'>", unsafe_allow_html=True)

header_container = st.container()
with header_container:
    col_logo, col_text = st.columns([1.0, 7])
    with col_logo:
        st.markdown('<div style="padding-top: 5px;"></div>', unsafe_allow_html=True)
        st.image("Logo_FLIC.png", width=100) 
    with col_text:
        st.markdown(f"""
            <div style="text-align: left; margin-left: -10px; padding-top: 15px; font-family: 'Segoe UI', sans-serif;">
                <div style="color: {COLOR_ORANGE_CHAY}; font-size: 1.1rem; font-weight: bold; line-height: 1.2;">
                    TRƯỜNG ĐẠI HỌC KINH TẾ - ĐẠI HỌC ĐÀ NẴNG
                </div>
                <div style="color: {COLOR_ORANGE_CHAY}; font-size: 1.1rem; font-weight: bold; margin-top: 5px;">
                    TRUNG TÂM NGOẠI NGỮ - TIN HỌC
                </div>
                <div style="color: #64748B; font-size: 0.85rem; font-style: italic; margin-top: 5px;">
                    FOREIGN LANGUAGES - INFORMATICS CENTRE
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown(f"""
    <div style="text-align: center; margin-top: 20px; margin-bottom: 30px;">
        <h1 style="color: {COLOR_ORANGE_CHAY}; font-size: 2.3rem; font-weight: bold;">
            NỀN TẢNG DASHBOARD QUẢN TRỊ THÔNG MINH – TRUNG TÂM NGOẠI NGỮ - TIN HỌC, TRƯỜNG ĐẠI HỌC KINH TẾ (FLIC)
        </h1>
        <div style="height: 3px; background-color: {COLOR_ORANGE_CHAY}; width: 15%; margin: 10px auto; border-radius: 2px;"></div>
    </div>
""", unsafe_allow_html=True)

st.success("**Trạng thái:** Kết nối dữ liệu SQL Server ổn định.")