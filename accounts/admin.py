from django.contrib import admin




from .models import BankAccountType, User, UserAddress, UserBankAccount,UserProfile


class UserAdmin(admin.ModelAdmin):
    
    list_display=("username","email")
    list_filter=("username","email")
    list_per_page=10
    search_fields=("username","email")


class UserBankAccountAdmin(admin.ModelAdmin):
    
    list_display=("user","account_no")
    list_filter=("user",)
    list_per_page=10
    search_fields=("user__username",)

class UserAdresAdmin(admin.ModelAdmin):
    
    list_display=("user","city")
    list_filter=("user","country")
    list_per_page=10
    search_fields=("user__username","city")

class UserProfileAdmin(admin.ModelAdmin):
    
    list_display=("user","first_name","user_bank_account")
    list_filter=("user","first_name")
    list_per_page=10
    search_fields=("user__username","first_name")


admin.site.register(BankAccountType)
admin.site.register(User,UserAdmin)
admin.site.register(UserAddress,UserAdresAdmin)
admin.site.register(UserBankAccount,UserBankAccountAdmin)
admin.site.register(UserProfile,UserProfileAdmin)





admin.site.site_title = "Techtorial Banking"
admin.site.site_header = "Techtorial Banking Admin Portal"  
admin.site.index_title = "Welcome to Techtorial Banking Admin Portal"