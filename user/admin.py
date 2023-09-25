from django.contrib import admin

from user.models import User


class UserRegistrationAdmin(admin.ModelAdmin):
    search_fields = ("email", "first_name", "phone_number")
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "uuid",
        "passport_id",
        "birth_date",
        "phone_number",
        "is_staff",
        "is_admin",
        "create_at",
        "is_active",
    )


admin.site.register(User, UserRegistrationAdmin)
