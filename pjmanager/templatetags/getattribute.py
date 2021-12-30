import re
from django import template

numeric_test = re.compile("^\d+$")
register = template.Library()

@register.filter(name='getattribute')
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    try:
    	return value[arg]
    except:
    	return ''
    