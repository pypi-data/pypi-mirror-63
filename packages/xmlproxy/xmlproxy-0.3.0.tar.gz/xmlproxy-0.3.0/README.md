# xmlproxy

``` py
import xml.etree.ElementTree as et

r = et.Element('root')
s = et.SubElement(r, 'tagname')
s.text = '123'

# use xmlproxy:

class Root(et.Element):
    tagname = text_property('tagname')

r = Root('root')
r.abc = '123'
```

forgot tag name and enjoy type hit!
