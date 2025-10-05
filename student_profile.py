from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
import re
from students_models import StudentModel, session, create_tables


ADMIN_PASSWORD = "123456"
def file():
    create_tables()
    def validate_form(data):
        required_fields = {
        'user': 'اسم الطالب',
        'address': 'حقل العنوان',
        'email': 'حقل البريد الإلكتروني',
        'phone': 'حقل رقم الهاتف',
        'certi': 'مؤهل الطالب',
        'gender': 'جنس الطالب',
    }
        for field, label in required_fields.items():
            if not data.get(field) or str(data[field]).strip() == "":
                return (field, f"⚠️ {label} مطلوب")
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.fullmatch(email_pattern, data['email'].strip()):
            return ('email', '✉️ يرجى إدخال بريد إلكتروني صحيح')
        phone_str = str(data['phone']).strip()
        if not re.fullmatch(r'\d{8,15}', phone_str):
            return ('phone', '📵 رقم الهاتف يجب أن يحتوي على أرقام فقط (8 إلى 15 رقمًا)')
        if len(data['user']) > 7:
            return ('user', 'اسم المستخدم يجب ان يكون اقل من 7 احرف')
        languages = data.get('language', [])
        if len(languages) == 0:
            return ('language', '⚠️ يجب اختيار لغة واحدة على الأقل')

    put_html('<h1 style="color:white; background-color: black; text-align: center; border-radius: 10px; padding: 20px 10px;">الملف التعريفي للطالب</h1>')
    put_text("تطبيق ويب لتصدير السير الذاتية للطلاب المؤهلين للدراسة لدينا").style("text-align:center;")
    with open('C:/Users/pc/Students_Management_sqlalchmy_pywebio/students.jpg', 'rb') as file:
        image_data = file.read()
    put_image(image_data, height='200px', width='300px').style("display: block; margin: 0 auto;")
    data = input_group(
        'املأ الحقول التالية للطالب المؤهل:',[
            input("اسم الطالب", name="user"),
            input("عنوان الطالب", name="address"),
            input("البريد الالكتروني", name="email"),
            input("رقم الهاتف", name="phone", type=NUMBER),
            radio("مؤهلات الطالب:", options=['Word','Excel','Powerpoint'], name="certi"),
            radio("جنس الطالب:", options=['Male','Female'], name="gender"),
            checkbox("اتقان اللغات :", options=['Arabic','English','German'], name="language"),
            ], validate=validate_form
    )

    new_student = StudentModel(name=data['user'], address=data['address'],email=data['email'],
                                phone=data['phone'], certification=data['certi'], gender=data['gender'])
    session.add(new_student)
    session.commit()

    file_image = file_upload("تحميل صورة شخصية","choose image")
    image = put_image(file_image['content']).style("width:100px; height:100px;")

    put_text("Student CV:")
    put_table([
        ['Profile', 'Name', 'Address', 'Phone', 'Email', 'Certificate', 'Gender', 'Language'],
        [image, data['user'], data['address'], data['phone'], data['email'], data['certi'], data['gender'], data['language']]
    ])
    put_success("تم حفظ بيانات الطالب في قاعدة البيانات").style("text-align:right;")

    choice = actions('خيارات إضافية:', [
        {'label': '🔐 عرض قاعدة البيانات (للمسؤولين)', 'value': 'admin'},
    ])

    if choice == 'admin':
        show_students_secure()

def show_students_secure():
    password = input("أدخل كلمة السر لعرض قاعدة البيانات:", type=PASSWORD)
    if password != ADMIN_PASSWORD:
        put_error("❌ كلمة السر غير صحيحة")
        return

    students = session.query(StudentModel).all()
    if not students:
        put_html("<p style='color:red; text-align:center;'>⚠ لا توجد بيانات طلاب حالياً</p>")
        return

    table_data = [['ID', 'الاسم', 'البريد الإلكتروني', 'الهاتف', 'الشهادة', 'النوع', 'العنوان']]
    for s in students:
        table_data.append([
            s.id, s.name, s.email, s.phone, s.certification, s.gender, s.address
        ])

    put_html("<h2 style='text-align:center;'>📋 قائمة الطلاب</h2>")
    put_table(table_data).style("width:100%; text-align:center;")
start_server(file, port=3000, debug=True)

# عرض قاعدة البيانات على صفحة الويب ولكن لا تعرض الا للمشرفين والاداريين عن طريق كلمة سر