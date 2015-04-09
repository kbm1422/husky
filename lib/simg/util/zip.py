#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os
import zipfile
import tarfile

import simg.fs as fs


class Type(object):
    ZIP = 1
    TGZ = 2
    TBZ = 3


def extract(zippath, dest=None, members=None):
    if dest is None:
        dest = os.path.dirname(zippath)

    logger.info("extract: zippath=[%s], dest=[%s]", zippath, dest)

    if tarfile.is_tarfile(zippath):
        tarobj = tarfile.open(zippath)
        tarobj.extractall(dest)
        tarobj.close()
    elif zipfile.is_zipfile(zippath):
        zipobj = zipfile.ZipFile(zippath)
        if members is None:
            zipobj.extractall(dest)
        else:
            for member in members:
                zipobj.extract(member, dest)
        zipobj.close()
    else:
        raise ValueError("unsupported archive type")


def archive(src, zippath, exclude=None, ziptype=Type.ZIP):
    logger.info("archive: src=[%s], zippath=[%s], exclude=[%s], type=[%s]", src, zippath, exclude, ziptype)

    dirpath = os.path.dirname(zippath)
    if not os.path.exists(dirpath):
        fs.mkpath(dirpath)

    if ziptype == Type.ZIP:
        zipobj = zipfile.ZipFile(zippath, "w")
        if os.path.isdir(src):
            for found in fs.find(src, exclude=exclude):
                logger.debug("found: %s", found)
                relname = os.path.relpath(found, src)
                if relname != ".":
                    relname = relname.replace("\\", "/")
                    if os.path.isdir(found):
                        relname += "/"
                    zipobj.write(found, relname)
        else:
            zipobj.write(src, os.path.basename(src))
        zipobj.close()
    elif ziptype == Type.TGZ or ziptype == Type.TBZ:
        raise NotImplementedError
    else:
        raise ValueError("unsupported archive type")


import ctypes
def retrieve_struct(struct_obj):
    """
    This function is used to extract data from a C construct.
    :param struct_obj: a C construct object with the "_fields_" attribute.
    :return: a nested python dictionary to represent the construct data.
    """
    assert len(struct_obj._fields_) > 0, "The input [%s] is not a C struct object" % struct_obj
    ret = dict()
    for f in struct_obj._fields_:
        field_name = f[0]
        field_type = f[1]
        try:
            if len(field_type._fields_) > 0:
                ret[field_name] = retrieve_struct(getattr(struct_obj, field_name))
        except AttributeError:
            field_value = getattr(struct_obj, field_name)
            if getattr(field_value, "_type_", None) == ctypes.c_ubyte:
                field_value = bytearray(field_value)
            ret[field_name] = field_value
    return ret


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )

