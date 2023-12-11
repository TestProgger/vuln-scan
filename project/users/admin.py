from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from project.users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ('id', )
    list_display = (
        'username',
        'role',
        'is_staff',
        'is_superuser',
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return (
            (
                "ФИО",
                {
                    "fields": (
                        "last_name",
                        "first_name",
                        "middle_name"
                    )
                }
            ),
            (
                "Данные для авторизации",
                {
                    "fields": ("username", "password", "role", "is_active")
                }
            ),
        )

    add_fieldsets = (
        (
            "ФИО",
            {
                "fields": (
                    "last_name",
                    "first_name",
                    "middle_name"
                )
            }
        ),
        (
            "Данные для авторизации",
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "role",
                    "password1",
                    "password2",
                    'is_active'
                ),
            },
        ),

    )