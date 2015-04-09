#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)


def trimHexString(s):
    return hex(int(s, 16))


def trimMacAddress(addr):
    new = []
    addr = addr.strip()
    if ":" in addr:
        old = addr.split(":")
        for item in old:
            if len(item) == 1:
                item = "0" + item
            item = item.upper()
            new.append(item)
        return ":".join(new)
    else:
        return ':'.join(s.encode('hex').upper() for s in addr.decode('hex'))


def quote(s):
    logger.debug("string before quote: %s", s)
    bytelist = s.encode("ascii")
    ret = ""
    for asc in bytelist:
        ascint = None
        if isinstance(asc, str):
            ascint = ord(asc)
        elif isinstance(asc, int):
            ascint = asc
        else:
            raise
        ascstr = chr(ascint)
        if ascstr in """!#$%&'()*+,/:;=?@[] "%-.<>\^_`{|}~""":
            ascstr = hex(ascint).replace("0x", "%").upper()
        ret += ascstr
    logger.debug("string after quote: %s", ret)
    return ret


def unquote(s):
    pass


def get_boolean(s):
    boolean_states = {'1': True, 'yes': True, 'true': True, 'on': True,
                      '0': False, 'no': False, 'false': False, 'off': False}
    if s.lower() not in boolean_states:
        raise ValueError('Not a boolean: %s' % s)
    return boolean_states[s.lower()]

if __name__ == "__main__":
    print trimMacAddress("0dd694ca4f00")
