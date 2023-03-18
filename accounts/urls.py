from django.urls import path
from django.contrib import admin
from .views import UserRegistrationView, LogoutView, UserLoginView


app_name = 'accounts'

urlpatterns = [
    path("login/", UserLoginView.as_view(),name="user_login"),
    path("logout/", LogoutView.as_view(),name="user_logout"),
    path("register/", UserRegistrationView.as_view(),name="user_registration"),
]



admin.site.site_title = "Techtorial Banking"
admin.site.site_header = "Techtorial Banking Admin Portal"  
admin.site.index_title = "Welcome to Techtorial Banking Admin Portal"

# list_display=("user","customer","account_type","balance") # admin tarafında hangi model başlığını göremek istiyorsak
#    # list_display_links=("name","city")# admin tarafında görünen link olması için
#   #  readonly_fields=("name","state")
# list_filter=("user","customer") # istediğimi models alanına göre filtreleme
#   #  ordering=('email ','gender')
# search_fields=('user',"customer")# hangi fielde göre arama yapsın istiyorsak
# list_per_page=10 # sayfa başına ne kadar data gelsin istiyorsak pagination için
# date_hierarchy=("balance",)# güncellenme tarihi hangi fielde göre istiyorsak
#  # fields=("name","email","phone_number") # burada istediğimiz fieldse göre sıralarız
#  # fields=(("name","email"),"phone_number") # burada istediğimiz fieldse göre yan yana gelir
