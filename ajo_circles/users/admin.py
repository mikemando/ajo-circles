from django.contrib import admin
from .models import User

class AccountAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "first_name", "id", "last_name", "credit_score", "last_login", "date_joined", "is_active")
    ordering = ("-date_joined",)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()    


admin.site.register(User, AccountAdmin)
