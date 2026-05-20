import pandas as pd
from ketnoi_sql import engine, file_path

sheets_can_nap = ['11-12.01_CB', '25-26.01_CB']
nganh_dict = {
    '03': ('QT kinh doanh du lịch', 'Du lịch'), '23': ('QT khách sạn', 'Du lịch'), '26': ('QT sự kiện', 'Du lịch'),
    '01': ('Ngoại thương', 'Kinh doanh quốc tế'), '06': ('Kế toán', 'Kế toán'), '18': ('Kiểm toán', 'Kế toán'),
    '04': ('Kinh tế phát triển', 'Kinh tế'), '11': ('Kinh tế & quản lý công', 'Kinh tế'), '20': ('Kinh tế đầu tư', 'Kinh tế'),
    '32': ('Kinh tế quốc tế', 'Kinh tế'), '09': ('Hành chính công', 'Lý luận chính trị'), '27': ('Kinh tế chính trị', 'Lý luận chính trị'),
    '19': ('Luật học', 'Luật'), '13': ('Luật kinh doanh', 'Luật'), '12': ('Quản trị Marketing', 'Marketing'),
    '28': ('Truyền thông Marketing', 'Marketing'), '31': ('Marketing số', 'Marketing'), '07': ('Ngân hàng', 'Ngân hàng'),
    '24': ('Tài chính công', 'Ngân hàng'), '02': ('Quản trị kinh doanh tổng quát', 'Quản trị kinh doanh'),
    '17': ('QT nguồn nhân lực', 'Quản trị kinh doanh'), '25': ('QT chuỗi cung ứng & logistics', 'Quản trị kinh doanh'),
    '30': ('Kinh doanh số', 'Quản trị kinh doanh'), '16': ('QT tài chính', 'Tài chính'), '15': ('Tài chính doanh nghiệp', 'Tài chính'),
    '33': ('Công nghệ tài chính', 'Tài chính'), '14': ('Tin học quản lý', 'Thống kê - Tin học'), '21': ('QT hệ thống thông tin', 'Thống kê - Tin học'),
    '05': ('Thống kê kinh tế - xã hội', 'Thống kê - Tin học'), '08': ('QT kinh doanh thương mại', 'Thương mại điện tử'),
    '22': ('Thương mại điện tử', 'Thương mại điện tử'), '29': ('Khoa học dữ liệu', 'Thương mại điện tử')
}

def clean_key(text):
    return str(text).strip().upper().replace(" ", "")

def get_combined_info(row):
    ten_lop = str(row['Lớp']).strip().upper()
    doi_tuong = str(row['Đối tượng']).strip()
    nam_sinh = str(row.get('NamSinh', 'NAN')).strip()

    if ten_lop != 'NAN' and ten_lop != '' and len(ten_lop) >= 5:
        ma_nganh = ten_lop[3:5]
        ten_nganh, ten_khoa = nganh_dict.get(ma_nganh, ('Ngành khác', 'Khối DUE'))
    else:
        if "Người đi làm" in doi_tuong: ten_nganh, ten_khoa = 'Vãng lai', 'Người đi làm'
        elif "Sinh viên - UD" in doi_tuong: ten_nganh, ten_khoa = 'Đa ngành', 'Khối ĐH Đà Nẵng'
        elif "Sinh viên khác" in doi_tuong: ten_nganh, ten_khoa = 'Vãng lai', 'Sinh viên khác'
        else: ten_nganh, ten_khoa = 'Vãng lai', 'Khác'

    if ten_lop != 'NAN' and len(ten_lop) >= 3 and ten_lop[0:2].isdigit():
        khoa_hoc = ten_lop[0:3]
    elif nam_sinh.isdigit() and len(nam_sinh) == 4:
        if "Người đi làm" in doi_tuong: khoa_hoc = f"NDL_{nam_sinh}"
        elif "Sinh viên - UD" in doi_tuong: khoa_hoc = f"UD_{nam_sinh}"
        elif "Sinh viên khác" in doi_tuong: khoa_hoc = f"SVK_{nam_sinh}"
        else: khoa_hoc = f"SVK_{nam_sinh}"
    else: 
        khoa_hoc = "Khác"     
    return pd.Series([ten_nganh, ten_khoa, khoa_hoc])

try:
    dict_ts = pd.read_sql("SELECT idThiSinh, HoTen FROM Dim_ThiSinh", engine)
    dict_ts['Key'] = dict_ts['HoTen'].apply(lambda x: str(x).strip().upper().replace(" ", ""))
    map_ts = pd.Series(dict_ts.idThiSinh.values, index=dict_ts.Key).to_dict()

    dim_lichthi = pd.read_sql("SELECT idLichThi, MaDotThi FROM Dim_LichThi", engine).drop_duplicates('MaDotThi')
    dim_khoa = pd.read_sql("SELECT idKhoa, TenNganh, TenKhoa FROM Dim_Khoa", engine).drop_duplicates(['TenNganh', 'TenKhoa'])
    dim_khoahoc = pd.read_sql("SELECT idKhoaHoc, KhoaHoc FROM Dim_KhoaHoc", engine).drop_duplicates('KhoaHoc')
    dim_ct = pd.read_sql("SELECT idChuongTrinh, TenChuongTrinh FROM Dim_ChuongTrinh", engine).drop_duplicates('TenChuongTrinh')
    list_all_df = []
    for sheet in sheets_can_nap:
        df_tmp = pd.read_excel(file_path, sheet_name=sheet)
        df_tmp.columns = df_tmp.columns.str.strip()
        df_tmp = df_tmp.dropna(subset=['HỌ VÀ TÊN'])
        df_tmp['Key'] = df_tmp['HỌ VÀ TÊN'].apply(lambda x: str(x).strip().upper().replace(" ", ""))
        df_tmp['SourceSheet'] = sheet 
        list_all_df.append(df_tmp)

    df_cb_all = pd.concat(list_all_df, ignore_index=True)
    df_cb_all['LanThi'] = df_cb_all.groupby('Key').cumcount() + 1
    df_cb_all['NamSinh'] = df_cb_all['Ng/SINH'].astype(str).str.strip().str[-4:]
    df_dmkh = pd.read_excel(file_path, sheet_name='DMKH')
    df_dmkh.columns = df_dmkh.columns.str.strip()
    df_dmkh['Key'] = df_dmkh['Họ và tên'].apply(lambda x: str(x).strip().upper().replace(" ", ""))
    df_dmkh['LanThi'] = df_dmkh.groupby('Key').cumcount() + 1

    df_hq = pd.read_excel(file_path, sheet_name='HQKD_CB')
    df_hq.columns = df_hq.columns.str.strip()
    df_hq['Key'] = (df_hq['Họ'].astype(str) + df_hq['Tên'].astype(str)).apply(lambda x: str(x).strip().upper().replace(" ", ""))
    df_hq['LanThi'] = df_hq.groupby('Key').cumcount() + 1

    df = pd.merge(df_cb_all, df_dmkh[['Key', 'LanThi', 'Lớp FLIC', 'Lớp', 'Đối tượng']], on=['Key', 'LanThi'], how='left')
    df = pd.merge(df, df_hq[['Key', 'LanThi', 'Tên chương trình']], on=['Key', 'LanThi'], how='left')

    df[['TenNganh_C', 'TenKhoa_C', 'KhoaHoc_C']] = df.apply(get_combined_info, axis=1)
    df['idThiSinh'] = df['Key'].map(map_ts)
    df = pd.merge(df, dim_lichthi, left_on='Lớp FLIC', right_on='MaDotThi', how='left')
    df = pd.merge(df, dim_khoa, left_on=['TenNganh_C', 'TenKhoa_C'], right_on=['TenNganh', 'TenKhoa'], how='left')
    df = pd.merge(df, dim_khoahoc, left_on='KhoaHoc_C', right_on='KhoaHoc', how='left')
    df = pd.merge(df, dim_ct, left_on='Tên chương trình', right_on='TenChuongTrinh', how='left')

    df_fact = pd.DataFrame({
        'idThiSinh': df['idThiSinh'].fillna(0).astype(int),
        'idLichThi': df['idLichThi'].fillna(0).astype(int),
        'idKhoa': df['idKhoa'].fillna(0).astype(int),
        'idKhoaHoc': df['idKhoaHoc'].fillna(0).astype(int),
        'idChuongTrinh': df['idChuongTrinh'].fillna(0).astype(int),
        'LanThi': df['LanThi'].astype(int),
        'DiemLT': pd.to_numeric(df['LT'], errors='coerce').fillna(0),
        'DiemTH': pd.to_numeric(df['TH'], errors='coerce').fillna(0),
        'KetQua': df['XẾP LOẠI'].astype(str).str.strip(),
        'SourceSheet': df['SourceSheet']
    })

    df_fact = df_fact[(df_fact['idThiSinh'] != 0) & (df_fact['idLichThi'] != 0)]
    print("--- KẾT QUẢ ĐỐI SOÁT ---")
    for s in sheets_can_nap:
        count = len(df_fact[df_fact['SourceSheet'] == s])
        print(f"Sheet {s}: Đã xử lý thành công {count} dòng.")

    df_fact_final = df_fact.drop(columns=['SourceSheet'])
    try:
        existing = pd.read_sql("SELECT idThiSinh, idLichThi, LanThi FROM Fact_KQCB", engine)
        df_final = pd.merge(df_fact_final, existing, on=['idThiSinh', 'idLichThi', 'LanThi'], how='left', indicator=True)
        df_final = df_final[df_final['_merge'] == 'left_only'].drop(columns=['_merge'])
    except:
        df_final = df_fact_final

    if not df_final.empty:
        df_final.to_sql('Fact_KQCB', con=engine, if_exists='append', index=False)
        print(f"Thành công! Đã nạp thêm {len(df_final)} dòng mới.")
    else:
        print("Không có dữ liệu mới.")

except Exception as e:
    print(f"Lỗi: {e}")