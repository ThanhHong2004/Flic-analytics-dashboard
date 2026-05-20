import pandas as pd
from ketnoi_sql import engine, file_path
sheets_nc = ['11-12.01_NC', '25-26.01_NC']
map_lich_thi_chuan = {
    '11-12.01_NC': 'ThiNC25_11.01', 
    '25-26.01_NC': 'ThiNC25_25.01',
}

sheets_hq_names = ['HQKD_NC', 'HQKD_NC_ThiLai_E', 'HQKD_NC_ThiLai_W', 'HQKD_NC_ThiLai_PP']
nganh_dict = {
    '01': ('Ngoại thương', 'Kinh doanh quốc tế'), '02': ('Quản trị kinh doanh tổng quát', 'Quản trị kinh doanh'),
    '03': ('QT kinh doanh du lịch', 'Du lịch'), '04': ('Kinh tế phát triển', 'Kinh tế'),
    '05': ('Thống kê kinh tế - xã hội', 'Thống kê - Tin học'), '06': ('Kế toán', 'Kế toán'),
    '07': ('Ngân hàng', 'Ngân hàng'), '08': ('QT kinh doanh thương mại', 'Thương mại điện tử'),
    '09': ('Hành chính công', 'Lý luận chính trị'), '11': ('Kinh tế & quản lý công', 'Kinh tế'),
    '12': ('Quản trị Marketing', 'Marketing'), '13': ('Luật kinh doanh', 'Luật'),
    '14': ('Tin học quản lý', 'Thống kê - Tin học'), '15': ('Tài chính doanh nghiệp', 'Tài chính'),
    '16': ('QT tài chính', 'Tài chính'), '17': ('QT nguồn nhân lực', 'Quản trị kinh doanh'),
    '18': ('Kiểm toán', 'Kế toán'), '19': ('Luật học', 'Luật'),
    '20': ('Kinh tế đầu tư', 'Kinh tế'), '21': ('QT hệ thống thông tin', 'Thống kê - Tin học'),
    '22': ('Thương mại điện tử', 'Thương mại điện tử'), '23': ('QT khách sạn', 'Du lịch'),
    '24': ('Tài chính công', 'Ngân hàng'), '25': ('QT chuỗi cung ứng & logistics', 'Quản trị kinh doanh'),
    '26': ('QT sự kiện', 'Du lịch'), '27': ('Kinh tế chính trị', 'Lý luận chính trị'),
    '28': ('Truyền thông Marketing', 'Marketing'), '29': ('Khoa học dữ liệu', 'Thương mại điện tử'),
    '30': ('Kinh doanh số', 'Quản trị kinh doanh'), '31': ('Marketing số', 'Marketing'),
    '32': ('Kinh tế quốc tế', 'Kinh tế'), '33': ('Công nghệ tài chính', 'Tài chính')
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
        else: khoa_hoc = f"SVK_{nam_sinh}"
    else: 
        khoa_hoc = "Khác"     
    return pd.Series([ten_nganh, ten_khoa, khoa_hoc])

try:
    dim_ts = pd.read_sql("SELECT idThiSinh, HoTen FROM Dim_ThiSinh", engine)
    dim_ts['Key'] = dim_ts['HoTen'].apply(clean_key)
    map_ts = pd.Series(dim_ts.idThiSinh.values, index=dim_ts.Key).to_dict()

    dim_lichthi = pd.read_sql("SELECT idLichThi, MaDotThi FROM Dim_LichThi", engine).drop_duplicates('MaDotThi')
    dim_khoa = pd.read_sql("SELECT idKhoa, TenNganh, TenKhoa FROM Dim_Khoa", engine).drop_duplicates(['TenNganh', 'TenKhoa'])
    dim_ct = pd.read_sql("SELECT idChuongTrinh, TenChuongTrinh FROM Dim_ChuongTrinh", engine).drop_duplicates('TenChuongTrinh')

    list_all_nc = []
    for sheet in sheets_nc:
        df_t = pd.read_excel(file_path, sheet_name=sheet)
        df_t.columns = df_t.columns.str.replace('\n', ' ').str.strip()
        df_t = df_t[df_t['HỌ VÀ TÊN'].notna()]
        df_t['Key'] = df_t['HỌ VÀ TÊN'].apply(clean_key)
        df_t['SourceSheet'] = sheet
        df_t['NamSinh_Raw'] = df_t['Ng/SINH'].astype(str).str.strip().str[-4:]
        list_all_nc.append(df_t)

    df_nc_all = pd.concat(list_all_nc, ignore_index=True)
    df_nc_all['LanThi'] = df_nc_all.groupby('Key').cumcount() + 1

    df_dmkh = pd.read_excel(file_path, sheet_name='DMKH')
    df_dmkh.columns = df_dmkh.columns.str.strip()
    df_dmkh['Key'] = df_dmkh['Họ và tên'].apply(clean_key)
    ns_lookup = df_nc_all[['Key', 'NamSinh_Raw']].drop_duplicates('Key')
    df_dmkh = pd.merge(df_dmkh, ns_lookup, on='Key', how='left').rename(columns={'NamSinh_Raw': 'NamSinh'})
    
    df_dmkh[['TenNganh_C', 'TenKhoa_C', 'KhoaHoc_C']] = df_dmkh.apply(get_combined_info, axis=1)
    new_kh = df_dmkh[['KhoaHoc_C']].drop_duplicates().rename(columns={'KhoaHoc_C': 'KhoaHoc'})
    existing_kh = pd.read_sql("SELECT KhoaHoc FROM Dim_KhoaHoc", engine)
    missing_kh = new_kh[~new_kh['KhoaHoc'].isin(existing_kh['KhoaHoc'])]
    if not missing_kh.empty:
        missing_kh.to_sql('Dim_KhoaHoc', con=engine, if_exists='append', index=False)
    dim_khoahoc = pd.read_sql("SELECT idKhoaHoc, KhoaHoc FROM Dim_KhoaHoc", engine)
    df_dmkh['LanThi'] = df_dmkh.groupby('Key').cumcount() + 1
    list_hq = []
    for s in sheets_hq_names:
        try:
            temp_hq = pd.read_excel(file_path, sheet_name=s)
            temp_hq.columns = temp_hq.columns.str.strip()
            temp_hq['Key'] = (temp_hq['Họ'].astype(str) + temp_hq['Tên'].astype(str)).apply(clean_key)
            list_hq.append(temp_hq[['Key', 'Tên chương trình']])
        except: pass
    
    df_hq_combined = pd.concat(list_hq, ignore_index=True)
    df_hq_combined['LanThi'] = df_hq_combined.groupby('Key').cumcount() + 1
    df_nc_all['MaDotThi_Sheet'] = df_nc_all['SourceSheet'].map(map_lich_thi_chuan)

    df = pd.merge(df_nc_all, df_dmkh[['Key', 'LanThi', 'TenNganh_C', 'TenKhoa_C', 'KhoaHoc_C']], on=['Key', 'LanThi'], how='left')
    df = pd.merge(df, df_hq_combined[['Key', 'LanThi', 'Tên chương trình']], on=['Key', 'LanThi'], how='left')

    df['idThiSinh'] = df['Key'].map(map_ts)
    df = pd.merge(df, dim_lichthi, left_on='MaDotThi_Sheet', right_on='MaDotThi', how='left')
    df = pd.merge(df, dim_khoa, left_on=['TenNganh_C', 'TenKhoa_C'], right_on=['TenNganh', 'TenKhoa'], how='left')
    df = pd.merge(df, dim_khoahoc, left_on='KhoaHoc_C', right_on='KhoaHoc', how='left')
    df = pd.merge(df, dim_ct, left_on='Tên chương trình', right_on='TenChuongTrinh', how='left')

    df_fact = pd.DataFrame({
        'idThiSinh': df['idThiSinh'].fillna(0).astype(int),
        'idKhoa': df['idKhoa'].fillna(0).astype(int),
        'idKhoaHoc': df['idKhoaHoc'].fillna(0).astype(int),
        'idLichThi': df['idLichThi'].fillna(0).astype(int),
        'idChuongTrinh': df['idChuongTrinh'].fillna(0).astype(int),
        'LanThi': df['LanThi'].astype(int),
        'W_LT': pd.to_numeric(df['LT WORD'], errors='coerce').fillna(0),
        'W_TH': pd.to_numeric(df['TH WORD'], errors='coerce').fillna(0),
        'E_LT': pd.to_numeric(df['LT EXCEL'], errors='coerce').fillna(0),
        'E_TH': pd.to_numeric(df['TH EXCEL'], errors='coerce').fillna(0),
        'P_LT': pd.to_numeric(df['LT PPOINT'], errors='coerce').fillna(0),
        'P_TH': pd.to_numeric(df['TH PPOINT'], errors='coerce').fillna(0),
        'KetQua': df['XẾP LOẠI'].astype(str).str.strip(),
        'SourceSheet': df['SourceSheet']
    })

    def clean_kq(val):
        v = val.upper()
        if v.startswith('Đ'): return 'Đạt'
        if 'VẮNG' in v: return 'Vắng thi'
        return 'Không đạt'
    df_fact['KetQua'] = df_fact['KetQua'].apply(clean_kq)

    df_fact = df_fact[(df_fact['idThiSinh'] != 0) & (df_fact['idLichThi'] != 0)]

    try:
        existing = pd.read_sql("SELECT idThiSinh, idLichThi, LanThi FROM Fact_KQNC", engine)
        df_final = pd.merge(df_fact, existing, on=['idThiSinh', 'idLichThi', 'LanThi'], how='left', indicator=True)
        df_final = df_final[df_final['_merge'] == 'left_only'].drop(columns=['_merge'])
    except:
        df_final = df_fact

    if not df_final.empty:
        df_final.drop(columns=['SourceSheet']).to_sql('Fact_KQNC', con=engine, if_exists='append', index=False)
        print(f"Thành công: Đã nạp {len(df_final)} dòng vào Fact_KQNC.")
    else:
        print("Không có dữ liệu mới để nạp.")

except Exception as e:
    print(f"Error: {e}")