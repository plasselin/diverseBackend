from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AIThread


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_superuser', 'is_validated', 'user_limit', 'current_prompt_count', 'is_prompt_disabled')
    list_filter = ('is_staff', 'is_superuser', 'is_validated')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'profilepic', 'user_limit', 'current_prompt_count', 'is_prompt_disabled')}),  # Add the new fields
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_validated', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_validated', 'user_limit', 'current_prompt_count', 'is_prompt_disabled'),  # Add the new fields
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(AIThread)
class AIThreadAdmin(admin.ModelAdmin):
    list_display = ('thread_id', 'user', 'created_at', 'is_deleted')
    list_filter = ('is_deleted', 'created_at')
    search_fields = ('thread_id', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


admin.site.register(CustomUser, CustomUserAdmin)
