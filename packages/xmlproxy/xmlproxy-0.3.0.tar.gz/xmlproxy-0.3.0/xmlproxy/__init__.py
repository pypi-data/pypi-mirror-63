# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import typing
import xml.etree.ElementTree as et


def filter_by_tag(tag):
    'create a filter which filter by tag'
    return lambda x: et.iselement(x) and x.tag == tag


class ElementsFilterProxy:
    __slots__ = ('element', 'filter')

    def __init__(self, element: et.Element, filter):
        super().__init__()
        self.element = element
        self.filter = filter

    def __iter__(self):
        for item in self.element:
            if self.filter(item):
                yield item

    def __len__(self):
        return len(list(iter(self)))

    def first(self):
        'get the first matched element or `None`'
        return next(iter(self), None)


class SubElementsProxy(ElementsFilterProxy):
    __slots__ = ('tag', 'eltype')

    def __init__(self, element: et.Element, tag: str, eltype=et.Element):
        assert issubclass(eltype, et.Element)
        super().__init__(element, filter_by_tag(tag))
        self.tag = tag
        self.eltype = eltype

    def append(self, element: et.Element):
        'add sub element to the end.'
        assert element.tag == self.tag, 'tag name does not match.'
        if not isinstance(element, self.eltype):
            raise TypeError(f'expected {self.eltype} type, got {type(element)}.')

        self.element.append(element)

    def new_sub(self) -> et.Element:
        'create a sub element and append it than return it.'
        sub_element = self.eltype(self.tag)
        self.element.append(sub_element)
        return sub_element

    def extend(self, elements):
        'append elements one by one.'
        for element in elements:
            assert element.tag == self.tag, 'tag name does not match.'
        self.element.extend(elements)

    def clear(self):
        'remove all matched sub elements.'
        self.element[:] = [t for t in self.element if not self.filter(t)]

    def replace(self, elements):
        'equals call `clear()` then `extend()`'
        self.clear()
        self.extend(elements)


def view_property(filter: typing.Callable[[et.Element], bool]) -> ElementsFilterProxy:
    '''
    a view property for view sub elements by give filter.
    '''

    def fget(self: et.Element):
        return ElementsFilterProxy(self, filter)

    return property(fget)

def element_list_property(tag: str, eltype: type=et.Element) -> SubElementsProxy:
    '''
    get or set the first matched element.

    arguments:

    - `eltype` - sub element type.

    usage:

    ``` py
    class Name(et.Element):
        ...

    class Root(et.Element):
        name = element_list_property('name', Name)
    ```
    '''

    def fget(self: et.Element):
        return SubElementsProxy(self, tag, eltype)

    return property(fget)


def element_property(tag: str) -> et.Element:
    '''
    get or set the first matched element.

    usage:

    ``` py
    class Root(et.Element):
        abc = element_property('abc')
    ```
    '''

    if not isinstance(tag, str):
        raise TypeError(f'expected str type, got {type(tag)}.')

    def fget(self: et.Element):
        return SubElementsProxy(self, tag).first()

    def fset(self: et.Element, node: et.Element):
        assert node.tag == tag, 'tag name does not match.'
        proxy = SubElementsProxy(self, tag)
        proxy.replace([node])

    return property(fget, fset)


class SubElementsTextProxy:
    __slots__ = ('_proxy', )

    def __init__(self, element: et.Element, tag: str):
        super().__init__()
        self._proxy = SubElementsProxy(element, tag)

    def append(self, text: str):
        'add text to the end.'
        if not isinstance(text, str):
            raise TypeError(f'expected str type, got {type(text)}.')
        self._proxy.new_sub().text = text

    def extend(self, texts: list):
        'append texts one by one.'
        for text in texts:
            self.append(text)

    def clear(self):
        'remove all matched sub elements.'
        self._proxy.clear()

    def replace(self, elements):
        'equals call `clear()` then `extend()`'
        self.clear()
        self.extend(elements)

    def __iter__(self):
        for item in self._proxy:
            if self.filter(item):
                yield item.text

    def __len__(self):
        return len(self._proxy)

    def first(self):
        'get the first matched text or `None`'
        return next(iter(self), None)


def text_list_property(tag: str) -> SubElementsTextProxy:
    '''
    get or set the matched element like a text collection.

    this is helpful if you don't care element attrib and they childs.

    usage:

    ``` py
    class Root(et.Element):
        abc = text_list_property('abc')
    ```
    '''

    if not isinstance(tag, str):
        raise TypeError(f'expected str type, got {type(tag)}')

    def fget(self: et.Element):
        return SubElementsTextProxy(self, tag)

    def fset(self: et.Element, texts: typing.List[str]):
        SubElementsTextProxy(self, tag).replace(texts)

    def fdel(self: et.Element):
        SubElementsTextProxy(self, tag).clear()

    return property(fget, fset, fdel)


def text_property(tag: str) -> str:
    '''
    get or set the first matched element like a text.

    this is helpful if you don't care element attrib and they childs.

    usage:

    ``` py
    class Root(et.Element):
        abc = text_property('abc')
    ```
    '''
    if not isinstance(tag, str):
        raise TypeError(f'expected str type, got {type(tag)}')

    def fget(self: et.Element):
        el = SubElementsProxy(self, tag).first()
        if el is not None:
            return el.text

    def fset(self: et.Element, text):
        if not isinstance(text, str):
            raise TypeError(f'excepted str, got {text}')

        proxy = SubElementsProxy(self, tag)
        el = proxy.first()
        if el is None:
            proxy.new_sub().text = text
        else:
            el.text = text

    return property(fget, fset)

def tostring(el: et.Element, *,
        xml_declaration=None,
        default_namespace=None,
        method=None,
        short_empty_elements=True) -> str:
    'convert `Element` to str.'

    from io import StringIO
    sb = StringIO()
    tr = et.ElementTree(el)
    tr.write(sb, encoding='unicode',
        xml_declaration=xml_declaration,
        default_namespace=default_namespace,
        method=method,
        short_empty_elements=False)
    return sb.getvalue()
