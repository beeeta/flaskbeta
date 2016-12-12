import re

def str_wrapper(outer,inner):
    tagre = re.compile('^<(.*)>$')
    res = re.match(tagre,outer)
    if res:
        lefts = '<'
        rigths = '>'
        slash = '/'
        tagName = res.group(1)
        return outer + inner + lefts + slash + tagName + rigths
    else:
        raise Exception("Invalid input,param outer should like <tag>!")

def build_mail_content(title,content):
    # head = str_wrapper('<h>',title)
    # ts =str(time.time())
    # cs = str_wrapper('<body>',content)
    # return r'<br/>'.join([head,ts,cs])
    return r'<br/>'.join([title,content])

if __name__ == '__main__':
    str_wrapper('<body>','test')