import pandas as pd
from ketnoi_sql import engine, file_path

nganh = {
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

try:
    df_dmkh = pd.read_excel(file_path, sheet_name='DMKH')
    df_dmkh.columns = df_dmkh.columns.str.strip()
    df_dmkh['KeyMatch'] = df_dmkh['Họ và tên'].astype(str).str.upper().str.replace(" ", "")
    sheets_diem = ['11-12.01_CB', '25-26.01_CB', '11-12.01_NC', '25-26.01_NC']
    list_birth = []

    for s in sheets_diem:
        try:
            temp = pd.read_excel(file_path, sheet_name=s)
            temp.columns = temp.columns.str.replace('\n', ' ').str.strip()
            t_xl = temp[['HỌ VÀ TÊN']].copy()
            t_xl['KeyMatch'] = t_xl['HỌ VÀ TÊN'].astype(str).str.upper().str.replace(" ", "")
            list_birth.append(t_xl)
        except:
            pass
    df_birthday = pd.concat(list_birth).drop_duplicates(subset=['KeyMatch'])
    df_gop = pd.merge(df_dmkh, df_birthday, on='KeyMatch', how='left')

    def lay_thong_tin_khoa(dong):
        ten_lop = str(dong['Lớp']).strip()
        doi_tuong = str(dong['Đối tượng']).strip()

        if ten_lop != 'nan' and ten_lop != '' and len(ten_lop) >= 5:
            ma_nganh = ten_lop[3:5]
            ten_nganh, ten_khoa = nganh.get(ma_nganh, ('Ngành khác', 'Khối DUE'))
            return pd.Series([ten_nganh, ten_khoa])
        
        else:
            if "Người đi làm" in doi_tuong:
                return pd.Series(['Vãng lai', 'Người đi làm'])
            elif "Sinh viên - UD" in doi_tuong:
                return pd.Series(['Đa ngành', 'Khối ĐH Đà Nẵng'])
            else:
                return pd.Series(['Vãng lai', 'Sinh viên khác'])

    df_gop[['TenNganh', 'TenKhoa']] = df_gop.apply(lay_thong_tin_khoa, axis=1)
    df_dim_khoa = df_gop[['TenNganh', 'TenKhoa']].drop_duplicates().reset_index(drop=True)
    df_dim_khoa.to_sql('Dim_Khoa', con=engine, if_exists='append', index=False)
    
    print(f"Thành công! Đã nạp {len(df_dim_khoa)} dòng vào Dim_Khoa.")
except Exception as e:
    print("Lỗi khi xử lý Dim_Khoa: ", e)
    
    