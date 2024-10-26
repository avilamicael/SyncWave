from django import template
from datetime import datetime

register = template.Library()

# Custom tag para formatar data no formato dd/mm/yy
@register.filter
def formatar_data(value):
    if isinstance(value, datetime):
        return value.strftime('%d/%m/%y')
    return value

# Custom tag para formatar CPF/CNPJ
@register.filter
def formatar_cpf_cnpj(value):
    if len(value) == 11:
        return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"
    elif len(value) == 14:
        return f"{value[:2]}.{value[2:5]}.{value[5:8]}/{value[8:12]}-{value[12:]}"
    return value

# Custom tag para formatar telefone
@register.filter
def formatar_telefone(value):
    # Verifica se o telefone tem 11 dígitos (celular)
    if len(value) == 11:
        return f"({value[:2]}) {value[2:7]}-{value[7:]}"
    # Verifica se o telefone tem 10 dígitos (telefone fixo)
    elif len(value) == 10:
        return f"({value[:2]}) {value[2:6]}-{value[6:]}"
    # Caso não tenha nem 10 nem 11 dígitos, retorna o valor sem formatação
    return value
