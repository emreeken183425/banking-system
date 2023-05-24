 
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


MYSQL DATABSE BAĞLANTI İÇİN 


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',// DATABASE NAME
        'USER': 'root',
        'PASSWORD': 'admin', // KENDİ ŞİFREN 
        'HOST':'localhost',
        'PORT':'3306',
    }
}



SONRA 
python manage.py makemigrations
python manage.py migrate

 MODELSİ DATABSE KAYDETMEK İÇİN BUNU YAZ 


ADMİN OLUŞTURMAK İÇİN 
TERMİNALDE 

python manage.py createsuperuser YAZ VE GELEN ALANLARI DOLDUR .










