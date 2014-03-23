from django import template
register = template.Library()

@register.filter(name='value_at')
def value_at(mylist, index):
    try:
        return mylist[index]
    except:
        return None

@register.simple_tag
def get_list_value(mylist, index):
    try:
        return mylist[index]
    except:
        return None
