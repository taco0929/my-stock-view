from django.template.defaulttags import register

@register.filter
def get_tuple_item_first(tup:tuple):
    return tup[0]
