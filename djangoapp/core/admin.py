from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario, Empresa

# Customizando a exibição de campos no Admin para o modelo de usuário
class UsuarioAdmin(UserAdmin):
    # Campos que aparecem ao editar um usuário
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Additional Info'), {'fields': ('empresa', 'is_trial')}),  # Incluímos empresa e is_trial
    )

    # Campos que aparecem na criação de um usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'empresa', 'password1', 'password2', 'is_trial', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # Configura os campos que aparecem na lista de usuários no admin
    list_display = ('username', 'email', 'first_name', 'last_name', 'empresa', 'is_trial', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'empresa__nome_fantasia')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'empresa')

# Registrando o modelo de Empresa no admin
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'razao_social', 'cnpj', 'telefone', 'email')
    search_fields = ('nome_fantasia', 'razao_social', 'cnpj')

# Registrando os modelos no admin
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Empresa, EmpresaAdmin)
