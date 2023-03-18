 
 DJANGO PROJE AYAĞA KALDIRMA KOMUTLARI 

 1  python -m venv env
 2  .\env\Scripts\activate
 3  pip install django
 4  python -m pip install --upgrade pip
 5  history
 6  clear
 7  pip list
 8  pip freeze
 9  pip freeze > requirements.txt
 10  django-admin startproject main .
 11  python manage.py runserver
 12 python manage.py startapp student(app ismi) 
 
 pip install python-decouple >> import et
gitignore ile aynı konumda env dosyası oluştur

setting.py içerisindeki SECRET KEY'i >>>>> env file taşı

setting.py file içerisine aşağıdaki komutları çalıştır.

from decouple import config

SECRET_KEY = config('SECRET_KEY')
!!!! SECRET KEY TIRNAKLARINI KALDIR.!!!

 GİTHUB REPODAN PROJE ÇEKİNCE YAPILACAK ADIMLAR

1-python -m venv env
2-env/Scripts/activate
3-pip install -r requirements.txt
4-python.exe -m pip install --upgrade pip
5-pip install python-decouple
6-pip freeze > requirements.txt
7-python manage.py migrate
8-python manage.py createsuperuser
9-python manage.py runserver


 templates ve static dosyaları ayarlamak için main deki 
 setting.py git  ve bunu yapıştır mainle aynı dizinde templates klasörü oluştur 

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ os.path.join(BASE_DIR,"templates") ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


STATİC DOSYALARI İÇİN
 MAİNDE  STATIC_URL = "static/" ALTINA AŞAĞIDAKİNİ YAĞIŞTIR MAİNLE AYN DİZİNDE STATİC KLASÖRÜ AÇ

 STATICFILES_DIRS=[
    os.path.join(BASE_DIR,"static")
]


REACT İLE DJANGO ARASINDA BAĞLANTI KURMAK İÇİN 


*** shell comutları OOREM ***
```
python manage.py shell  # yazarak shell e gir
exit() ile çıkış yapabilirsin
from fscohort.modls import Student(models ismi databsede oluşturduğun tabloyu çağırdık)
 print(Student) ile yazdırdık
  s1=Student(first_name="victor",last_name="abc",number=5)databsede ki kolonlar yada modelsdeki isimler ile yei bir öğrenci oluşturduk
  s1 yazarak terminalde gördük
  s1.save() ile databese kaydettik
s1.first_name="henry" ile first_name değiştirdik
s1.save() ile databese kaydettik
s2=Student.objects.create (first_name= 'kadir',last_name="abc",number=55 ) buşekilde save() e gerek kalmadan direkt kaydeder
 alls=Student.objects.all()
 alls bu şekilde databsedeki tüm bilgileri görebiliriz
for x in alls:x  bu şekilde döngü ile de çağırabiliriz
g1=Student.objects.get(number=55) #aynı numaradan fazla varsa filter kullanırız
g1 buşeklide numarası 55 olan kişiyi getirdik
 f1=Student.objects.filter(number=77)
>>> f1  aynı numaradan fazla varsa filter kullanırız
 f2=Student.objects.exclude(number=55)
>>> f2 bu şekilde numarası 55 olmayanları getirdik exclude fonksiyonu ile
 f3=Student.objects.filter(first_name__startswith="E") 
>>> f3 baş harfi e ile başlayanları getir örneği
f3=Student.objects.filter(last_name__startswith="E")  
>>> f3 burada ise last namei e ile başlayanlar getirilir
f4=Student.objects.filter(last_name__endswith="E")  
>>> f4 burada ise last namei e ile BİTEN getirir.
 

```
# resim yükleme için aşağıdaki adımlar

modelse avatar=models.ImageField('resim',blank=True,null=True,upload_to="meida/")# 
pip install pillow resim yüklemek için indirmemiz gereken paket

MEDIA_URL='media/' setting.py a da bunu yazman gerekli main settings.py
sonra main urls.py a gidip 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns +=static(settings.MEDIA_URL,document_roor=settings.MEDIA_ROOT) bunu yaz
 yada settings py da 
 MEDIA_URL="/media/"
MEDIA_ROOR=os.path.join(BASE_DIR,"media") bunları yaz mainle aynı dizinde media klasörü aç

**** DATABSE İLE BAĞLANMA NASIL*****
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
#  pip install psycopg2  postgresql için bu İNECEK ve aşağıdaki bağlantı
 MAİNDEKİ STTİNGS.PY A AŞAĞIDAKİ BAĞLAANTILARI EKLE DOLDUR
DATABASES = {
    "default": {
       'ENGINE': 'django.db.backends.postgresql',
        "NAME": "models",# databse ismini buraya
        "USER":"postgres",#login username
        "PASSWORD":"183425",# GİRİŞ ŞİFREN
        "HOST":"localhost",
        "PORT":"5433",
        
    }
}
YUKARIDAKİLERDEN SONRA DATABSE KAYIT İÇİN python manage.py migrate YAP


Templates
Variables: {{ variable }}
Tags: {% tag %}
Filters : {{ dict1.django|title }}
Comments:: Single line: {# this won't be rendered #}
{# This is a single line comment #}

Multi line: {% comment %}
{% comment %} This is a multi line comment, you can't see it on the page! {% endcomment %}











