# Flask Register App

Энэ төсөл нь Flask + SQLite ашигласан бүртгэлийн веб систем юм.

## Боломжууд
- Бүртгэлийн хуудас
- Овог, нэр, утас, имэйл бүртгэнэ
- Имэйл форматыг шалгана
- Мэдээлэл `Register` гэсэн SQLite table-д хадгална
- Admin login хэсэгтэй
- Admin page дээр бүртгэгдсэн жагсаалт харна
- Excel (`.xlsx`) файлаар export хийж татаж авна
- Цэвэрхэн, бизнесийн өнгө аястай минимал дизайнтай
- Амжилттай / алдааны мэдээлэл харуулна

## Ашигласан технологи
- Python
- Flask
- SQLite
- openpyxl

## Төслийн бүтэц
```bash
register_app/
│ app.py
│ requirements.txt
│ README.md
│
├── instance/
│   └── register.db
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── index.html
    ├── admin_login.html
    └── admin_dashboard.html
```

## VS Code дээр ажиллуулах заавар

### 1. ZIP файлыг задлах
ZIP файлаа задлаад `register_app` хавтсыг VS Code-оор нээнэ.

### 2. Terminal нээх
VS Code дотор:
- **Terminal > New Terminal**

### 3. Virtual environment үүсгэх
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Mac / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Сангууд суулгах
```bash
pip install -r requirements.txt
```

### 5. Апп ажиллуулах
```bash
python app.py
```

### 6. Browser-оор нээх
```text
http://127.0.0.1:5000/
```

## Admin хэсэг
Admin login:
```text
http://127.0.0.1:5000/admin/login
```

Default admin мэдээлэл:
- Username: `admin`
- Password: `admin123`

## Хэрэв admin нууц үг солих бол
Environment variable ашиглаж болно.

Windows CMD:
```bash
set ADMIN_USERNAME=myadmin
set ADMIN_PASSWORD=mypassword
python app.py
```

PowerShell:
```powershell
$env:ADMIN_USERNAME="myadmin"
$env:ADMIN_PASSWORD="mypassword"
python app.py
```

Mac / Linux:
```bash
export ADMIN_USERNAME=myadmin
export ADMIN_PASSWORD=mypassword
python app.py
```

## SQLite database
Database файл:
```text
instance/register.db
```

Table нэр:
```text
Register
```

## Excel export
Admin page руу орж **Excel татах** товч дээр дарж `.xlsx` файлаар бүртгэлийн мэдээлэл татаж авна.

## Тэмдэглэл
- Нэг имэйл давхар бүртгэгдэхгүй
- Имэйл формат жишээ: `example@company.com`
- Database файл анхны ажиллуулах үед автоматаар үүснэ
