
def write_tag_files( conf):
    c = ""
    txt = """-   content: %s
    path: /etc/tags/%s
    permissions: '0644'\n"""
    for i in conf['tags']:
        c += txt % (conf['tags'][i], i)
    return c[:-1]
