CREATE DATABASE FLIC_3
GO
USE FLIC_3
GO

--1. Tạo bảng Dim_ThiSinh
CREATE TABLE Dim_ThiSinh(
idThiSinh int IDENTITY(1,1) primary key not null,
idHV varchar (10) not null,
HoTen nvarchar(511) not null,
SBD varchar (20) not null,
MSSV varchar (20)not null,
NgaySinh date not null,
NoiSinh nvarchar (255) not null,
DoiTuong nvarchar(255) not null);

--2.Tạo bảng Dim_Khoa
CREATE TABLE Dim_Khoa(
idKhoa int IDENTITY(1,1) primary key not null,
TenNganh nvarchar(200) not null,
TenKhoa nvarchar(200)not null );

--3. Tạo bảng Dim_Khóa học 
CREATE TABLE Dim_KhoaHoc(
idKhoaHoc int IDENTITY(1,1) primary key not null,
KhoaHoc varchar(50) not null);

--4. Tạo bảng Dim_ChuongTrinh
CREATE TABLE Dim_ChuongTrinh(
idChuongTrinh int IDENTITY(1,1) primary key not null,
TenChuongTrinh nvarchar(100) not null,
LoaiChuongTrinh nvarchar(20) not null,
GiaTien decimal(18, 2) not null);

--5. Tạo bảng Dim_LichThi
CREATE TABLE Dim_LichThi (
idLichThi int IDENTITY(1,1) PRIMARY KEY not null,
MaDotThi nvarchar(100) not null,
TenDotThi nvarchar(50) not null,
NgayThi date not null,
Thang as MONTH(NgayThi),
Nam AS YEAR(NgayThi),
TenQuy as 'Quy ' + CAST(DATEPART(QUARTER, NgayThi) as nvarchar(1)));

--6. Tạo bảng Fact_KQCB
CREATE TABLE Fact_KQCB(
idFact int IDENTITY(1,1) PRIMARY KEY, 
idThiSinh int not null,
idKhoa int not null,
idKhoaHoc int not null,
idLichThi int not null,
idChuongTrinh int not null,
LanThi int not null,
DiemLT float not null,
DiemTH float not null,
KetQua nvarchar(50),
Constraint FK_KQCB_ThiSinh foreign key (idThiSinh) references Dim_ThiSinh(idThiSinh),
Constraint FK_KQCB_Khoa foreign key (idKhoa) references Dim_Khoa(idKhoa),
Constraint FK_KQCB_KhoaHoc foreign key(idKhoaHoc) references Dim_KhoaHoc(idKhoaHoc),
Constraint FK_KQCB_LichThi foreign key (idLichThi) references Dim_LichThi(idLichThi),
Constraint FK_KQCB_ChuongTrinh foreign key (idChuongTrinh) references Dim_ChuongTrinh(idChuongTrinh));

UPDATE f
SET f.idChuongTrinh = ct_dung.idChuongTrinh
FROM Fact_KQNC f
JOIN Dim_ChuongTrinh ct_sai ON f.idChuongTrinh = ct_sai.idChuongTrinh
JOIN Dim_ChuongTrinh ct_dung ON ct_sai.TenChuongTrinh = ct_dung.TenChuongTrinh
WHERE ct_dung.LoaiChuongTrinh = N'Thi nâng cao' 
  AND ct_sai.LoaiChuongTrinh = N'Thi cơ bản';
--7. Tạo bảng Fact_KQNC
CREATE TABLE Fact_KQNC(
idFact int IDENTITY(1,1) PRIMARY KEY,
idThiSinh int not null,
idKhoa int not null,
idKhoaHoc int not null,
idLichThi int not null,
idChuongTrinh int not null,
LanThi int not null,
W_LT float not null, 
W_TH float not null, 
E_LT float not null, 
E_TH float not null, 
P_LT float not null, 
P_TH float not null,
KetQua nvarchar(50) not null,
Constraint FK_KQNC_ThiSinh foreign key (idThiSinh) references Dim_ThiSinh(idThiSinh),
Constraint FK_KQNC_Khoa foreign key (idKhoa) references Dim_Khoa(idKhoa),
Constraint FK_KQNC_KhoaHoc foreign key(idKhoaHoc) references Dim_KhoaHoc(idKhoaHoc),
Constraint FK_KQNC_LichThi foreign key (idLichThi) references Dim_LichThi(idLichThi),
Constraint FK_KQNC_ChuongTrinh foreign key (idChuongTrinh) references Dim_ChuongTrinh(idChuongTrinh));

select * from Dim_ThiSinh
select * from Dim_Khoa
select * from Dim_KhoaHoc
select * from Dim_ChuongTrinh
select * from Dim_LichThi
select * from Fact_KQCB
select * from Fact_KQNC


