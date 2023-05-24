

************** RESTful API for USERS************

GET:http://localhost:8000/accounts/users     // TÜM USERLARI GETİRİR





GET FOR İD:http://localhost:8000/accounts/users/18  // 18 YERİNE USER İD YAZILACAK İD YE GÖRE USER GETİRİR

POST:http://localhost:8000/accounts/users/  // ÖRNEK AŞAĞIDA GMAİL UNİQE OLACAK POST İŞLEMİ

{
 
  "password": "Erzurum25!",
  "first_name": "Tayfun25",
  "last_name": "Eken",
  "username": "Taylor",
  "email": "Tayfu56n@gmail.com",
  "phone_number": 252355
}


PUT:http://localhost:8000/accounts/users/< WRİTE İD>/   // UPDATE İŞLEMİ DİĞER USER BİLGİLERİ DE GİRİLEBİLİR


{
      
        "password": "Erzurum25!",
        "last_login": "2023-04-15T04:05:59Z",
        "is_superuser": false,
        "first_name": "gggg",
        "last_name": "Eken",
        "is_staff": false,
        "is_active": true,
        "date_joined": "2023-04-15T04:05:54Z",
        "username": "hasan",
        "email": "emre@gmail.com",
        "phone_number": "05531588944",
        "groups": [],
        "user_permissions": []
    }

DELETE:http://localhost:8000/accounts/users/< WRİTE İD>  // SİLMEK İSTEDİĞİN USERA AİT İD YAZ SİL 


 

 ************** RESTful API for ACCOUNTS " user must be Login"  ************

GET:http://localhost:8000/accounts/user-bank-accounts/    // USER İD YAZILACAK İD YE GÖRE USER GETİRİR LOGİN OLMASI ŞART YOKSA HTML DÖNER

GET FOR İD://localhost:8000/accounts/user-bank-accounts/< WRİTE İD >

POST://localhost:8000/accounts/user-bank-accounts/

DELETE://localhost:8000/accounts/user-bank-accounts/< WRİTE İD >




************** RESTful API for ACCOUNTS TYPE  ************

GET:http://localhost:8000/accounts/bank-account-types/     

GET FOR İD:http://localhost:8000/accounts/bank-account-types/< WRİTE İD>  // İD YAZILACAK İD YE GÖRE  GETİRİR

POST:http://localhost:8000/accounts/bank-account-types/
 
DELETE:http://localhost:8000/accounts/bank-account-types/< WRİTE İD>  // SİLMEK İSTEDİĞİN USERA AİT İD YAZ SİL 


************** RESTful API for USER PROFİLE  TYPE  ************


GET:http://localhost:8000/accounts/user-profiles/

GET FOR İD:http://localhost:8000/accounts/user-profiles/< WRİTE İD>

PUT:http://localhost:8000/accounts/user-profiles/   // örnek aşağıda  adres user bancaccoutn uniqe dikkat 

{
       
        "first_name": "Turan",
        "last_name": "alkan",
        "image": null,
        "user_bank_account": 17,
        "user_address": 12,
        "user": 17
    }

POST:http://localhost:8000/accounts/user-profiles/   // örnek aşağıda  adres user bancaccoutn uniqe dikkat 

{
       
        "first_name": "Turan",
        "last_name": "alkan",
        "image": null,
        "user_bank_account": 17,
        "user_address": 12,
        "user": 17
    }

DELETE:http://localhost:8000/accounts/user-profiles/< WRİTE İD>  // SİLMEK İSTEDİĞİN USERA AİT İD YAZ SİL 




************** RESTful API for USER ADRESS  TYPE  ************


GET:http://localhost:8000/accounts/user-addresses/

GET FOR İD:http://localhost:8000/accounts/user-addresses/< WRİTE İD>

POST:http://localhost:8000/accounts/user-addresses/  // USER ADRES VARA BAŞKA USER OLACAK 

{
      
        "street_address": "MALEZYA",
        "city": "Ankara ALTINDAĞ",
        "postal_code": "060805",
        "country": "Türkiye",
        "user": 3
    }


PUT :http://localhost:8000/accounts/user-addresses/3  //3 YERİNE  İD YAZ BİLGİLERİ DEĞİŞTİR
 {
      
        "street_address": "Turkey",
        "city": "Ankara ALTINDAĞ",
        "postal_code": "060805",
        "country": "Türkiye",
        "user": 3
    }

DELETE:http://localhost:8000/accounts/user-addresses/< WRİTE İD>    // SİLMEK İSTEDİĞİN USERA AİT İD YAZ SİL 