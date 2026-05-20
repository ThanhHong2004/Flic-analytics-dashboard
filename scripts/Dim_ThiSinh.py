import pandas as pd 
from ketnoi_sql import engine, file_path

try:
    df_dmkh = pd.read_excel(file_path, sheet_name='DMKH')
    df_dmkh.columns = df_dmkh.columns.str.strip()
    df_dmkh['KeyMatch'] = df_dmkh['Họ và tên'].astype(str).str.upper().str.replace(" ", "")
    sheets_diem = ['11-12.01_CB', '25-26.01_CB', '11-12.01_NC', '25-26.01_NC']
    list_temp = []

    for s in sheets_diem:
        try:
            temp = pd.read_excel(file_path, sheet_name=s)
            temp.columns = temp.columns.str.replace('\n', ' ').str.strip()
            
            t_xl = temp[['HỌ VÀ TÊN', 'SBD', 'Ng/SINH', 'NƠI SINH']].copy()
            t_xl['KeyMatch'] = t_xl['HỌ VÀ TÊN'].astype(str).str.upper().str.replace(" ", "")
            list_temp.append(t_xl)
        except Exception as e:
            print(f"Bỏ qua sheet {s} do: {e}")
    df_gop = pd.concat(list_temp).drop_duplicates(subset=['KeyMatch'])
    df_final = pd.merge(df_dmkh, df_gop[['KeyMatch', 'SBD', 'Ng/SINH', 'NƠI SINH']], on='KeyMatch', how='left')

    def xu_ly_mssv(dong):
        mssv = str(dong['Mã Sinh viên']).strip()
        id_hv = str(dong['ID']).strip()
        doi_tuong = str(dong['Đối tượng']).strip()
        
        if mssv != 'nan' and mssv != '' and mssv.lower() != 'none':
            return mssv       
        if "Người đi làm" in doi_tuong:
            return f"NĐL_{id_hv}"
        else:
            return f"VL_{id_hv}"
    df_final['MSSV_Final'] = df_final.apply(xu_ly_mssv, axis=1)
    df_to_sql = df_final[['ID', 'SBD', 'Họ và tên', 'Ng/SINH', 'NƠI SINH', 'Đối tượng', 'MSSV_Final']].copy()
    df_to_sql.columns = ['idHV', 'SBD', 'HoTen', 'NgaySinh', 'NoiSinh', 'DoiTuong', 'MSSV']
    df_to_sql['SBD'] = df_to_sql['SBD'].fillna('CHUA_THI')
    df_to_sql['NgaySinh'] = pd.to_datetime(df_to_sql['NgaySinh'], dayfirst=True, errors='coerce')
    df_to_sql.to_sql('Dim_ThiSinh', con=engine, if_exists='append', index=False)
    print("Nạp Dim_ThiSinh thành công!")

except Exception as e:
    print("Lỗi hệ thống: ", e)