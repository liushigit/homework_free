import re
from django.utils.safestring import mark_safe
from django import template
register = template.Library()

class_re = re.compile(r'input.*?(?<=class=["\'])(.*?)(?=["\'])')
@register.filter
def add_class(value, css_class):
    string = unicode(value)
    match = class_re.search(string)
    if match:
        m = re.search(r'^%s$|^%s\s|\s%s\s|\s%s$' % (css_class, css_class, 
                                                    css_class, css_class), 
                                                    match.group(1))
        # print match.group(1)

        if not m:
            return mark_safe(class_re.sub(match.group(1) + " " + css_class, 
                                          string))
    else:
        return mark_safe(string.replace('input ', 'input class="%s" ' % css_class, 2)
                               .replace('select ', 'select class="%s" ' % css_class, 1)
                               .replace('textarea', 'textarea class="%s" ' %css_class, 1)
                        )
    return value
