#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from xml.dom import minidom


class Element(minidom.Element):
    class Position(object):
        BEFORE = "before"
        AFTER = "after"

    def _check_owner_document(self):
        if self.ownerDocument is None:
            raise ValueError("Can't call addSubElement, addTextNode or addAttribute when element.ownerDocument is None")

    def addSubElement(self, tagName, position=None, refChild=None):
        self._check_owner_document()
        subelement = self.ownerDocument.createElement(tagName)
        if position == Element.Position.BEFORE:
            self.insertBefore(subelement, refChild)
        elif position == Element.Position.AFTER:
            newRefChild = refChild.nextSibling
            self.insertBefore(subelement, newRefChild)
        else:
            self.appendChild(subelement)
        return subelement
    
    def addTextNode(self, data):
        self._check_owner_document()
        textnode = self.ownerDocument.createTextNode(data)
        self.appendChild(textnode)
        return textnode
    
    def addAttribute(self, name, value):
        self._check_owner_document()
        attr = self.ownerDocument.createAttribute(name)
        attr.value = value
        self.setAttributeNode(attr)
        return attr

#override original Element class
minidom.Element = Element

if __name__ == "__main__":
    pass