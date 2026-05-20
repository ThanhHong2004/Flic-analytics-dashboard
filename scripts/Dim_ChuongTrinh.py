import pandas as pd 
from ketnoi_sql import engine, file_path
try:
    df_cb = pd.read_excel(file_path, sheet_name='HQKD_CB')
    df_nc = pd.read_excel(file_path, sheet_name='HQKD_NC')
    df_tl_pp = pd.read_excel(file_path, sheet_name='HQKD_NC_ThiLai_PP')
    df_tl_w = pd.read_excel(file_path, sheet_name='HQKD_NC_ThiLai_W')
    df_tl_e = pd.read_excel(file_path, sheet_name='HQKD_NC_ThiLai_E')
    
    def chuyen_doi(df, loai):
        co_ban = df[['Tên chương trình', 'Đã thu']].copy()
        co_ban['Tên chương trình'] = co_ban['Tên chương trình'].astype(str).str.strip()
        co_ban['Đã thu']= pd.to_numeric(co_ban['Đã thu'], errors='coerce').fillna(0)
        co_ban ['LoaiChuongTrinh'] = loai
        return co_ban
    df_loc_cb = chuyen_doi(df_cb, 'Thi cơ bản')
    df_loc_nc = chuyen_doi(df_nc, 'Thi nâng cao') 
    df_loc_tl_pp = chuyen_doi(df_tl_pp, "Thi lại_NC")
    df_loc_tl_w = chuyen_doi(df_tl_w, "Thi lại_NC")
    df_loc_tl_e = chuyen_doi(df_tl_e, "Thi lại_NC")
    
    df_gop = pd.concat([df_loc_cb, df_loc_nc, df_loc_tl_e, df_loc_tl_pp,df_loc_tl_w], ignore_index=True)
    
    df_final = df_gop.drop_duplicates(subset=['Tên chương trình','LoaiChuongTrinh']).reset_index(drop=True)
    df_final = df_final.rename(columns={
        'Tên chương trình': 'TenChuongTrinh',
        'Đã thu' : 'GiaTien'})  
    df_sql = df_final[['TenChuongTrinh', 'LoaiChuongTrinh', 'GiaTien']]
    df_db = pd.read_sql("SELECT TenChuongTrinh, LoaiChuongTrinh FROM Dim_ChuongTrinh",con=engine)
    df_new = pd.merge(df_sql,df_db,on=['TenChuongTrinh', 'LoaiChuongTrinh'],how='left',indicator=True)
    df_new = df_new[df_new['_merge'] == 'left_only'].drop(columns=['_merge'])

    df_new.to_sql('Dim_ChuongTrinh', con=engine, if_exists='append', index=False)
    print("Successful")
except Exception as e:
    print("Error: ",e)