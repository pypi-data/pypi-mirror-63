# -*- coding: utf-8 -*-
"""Module for basic XTGeo interaction with OS/system files and folders"""

from __future__ import division, absolute_import
from __future__ import print_function

import os
import os.path
import io
from platform import system as plfsys
from tempfile import mkstemp

try:
    from pathlib import Path
except ImportError:
    pass

import six

import xtgeo.cxtgeo._cxtgeo as _cxtgeo
from .xtgeo_dialog import XTGeoDialog

xtg = XTGeoDialog()
logger = xtg.functionlogger(__name__)


def check_folder(fname, raiseerror=None):
    """General function to check folder"""
    _nn = _XTGeoCFile(fname)
    status = _nn.check_folder(raiseerror=raiseerror)
    del _nn
    return status


class _XTGeoCFile(object):
    """A private class for file handling of files in/out of CXTGeo"""

    def __init__(self, fobj, mode="rb"):

        self._name = fobj
        self._tmpfile = None
        self._delete_after = False  # delete file (e.g. tmp) afterwards
        self._fhandle = None
        self._mode = mode
        self._memstream = False
        logger.debug("Init ran for _XTGeoFile")

    @property
    def fhandle(self):  # was get_handle
        """File handle for CXTgeo, the filehandle is a read only property"""

        if self._fhandle and "Swig Object of type 'FILE" in str(self._fhandle):
            return self._fhandle

        fhandle = None
        if (
            isinstance(self._name, io.BytesIO)
            and self._mode == "rb"
            and plfsys() == "Linux"
        ):
            if six.PY2:
                raise NotImplementedError(
                    "Reading BytesIO not fully supported in Python 2"
                )

            fobj = self._name.getvalue()  # bytes type in Python3, str in Python2

            # note that the typemap in swig computes the length for the buf!
            self._memstream = True

        elif (
            isinstance(self._name, io.BytesIO)
            and self._mode == "wb"
            and plfsys() == "Linux"
        ):
            if six.PY2:
                raise NotImplementedError(
                    "Writing to BytesIO not supported in Python 2"
                )

            fobj = bytes()
            self._memstream = True

        elif (
            isinstance(self._name, io.BytesIO)
            and self._mode == "rb"
            and (plfsys() == "Windows" or plfsys() == "Darwin")
        ):
            # windows/mac miss fmemopen; write buffer to a tmp instead as workaround
            fds, fobj = mkstemp(prefix="tmpxtgeoio")
            os.close(fds)
            with open(fobj, "wb") as newfile:
                newfile.write(self._name.getvalue())

            self._tmpfile = fobj

        else:
            if six.PY3 and isinstance(self._name, Path):
                fobj = str(self._name.resolve())
            else:
                fobj = self._name

        if self._memstream:
            fhandle = _cxtgeo.xtg_fopen_bytestream(fobj, self._mode)

        else:
            try:
                fhandle = _cxtgeo.xtg_fopen(fobj, self._mode)
            except TypeError as err:
                reason = ""
                if six.PY2:
                    reason = "In Python 2, do not use __future__ UnicodeLiterals!"
                logger.critical("Cannot open file: %s. %s", err, reason)
            else:
                logger.critical("Cannot open file, unknown reason")

        self._fhandle = fhandle
        return self._fhandle

    def exists(self):  # was: file_exists
        """Check if file or memerory stream exists, and returns True of OK."""
        if "r" in self._mode:
            if isinstance(self._name, str) and os.path.isfile(self._name):
                return True

            if isinstance(self._name, io.BytesIO):
                return True

            return False

        return True

    def check_folder(self, raiseerror=None):
        """Check if folder given in xfile exists and is writeable.

        The file itself may not exist (yet), only the folder is checked

        Args:
            raiseerror (excpetion): If none, then return True or False, else raise the
                given Exception if False

        Return:
            status: True, if folder exists and is writable, False if not.

        """

        # Here are issues here on Windows/Mac in particular

        status = True

        if os.path.isdir(self._name):
            folder = self._name
        else:
            folder = os.path.dirname(self._name)
            if folder == "":
                folder = "."

        if not os.path.exists(folder):
            if raiseerror:
                raise raiseerror("Folder does not exist: <{}>".format(folder))

            status = False

        if os.path.exists(folder) and not os.access(folder, os.W_OK):
            if raiseerror:
                raise raiseerror(
                    "Folder does exist but is not writable: <{}>".format(folder)
                )

            status = False

        return status

    def has_fhandle(self):  # was is_fhandle
        """Return True if pfile is a filehandle, not a file"""

        if self._fhandle and "Swig Object of type 'FILE" in str(self._fhandle):
            return True

        return False

    def close(self, cond=True):
        """Close file handle given that filehandle exists (return True), otherwise do
        nothing (return False).

        If cond is False, nothing is done (made in order to avoid ifs in callers)
        """
        if not cond:
            return True

        if self._memstream and self._fhandle and "w" in self._mode:
            # this assumes that the file pointer is in the end of the current filehandle
            npos = _cxtgeo.xtg_ftell(self._fhandle)
            buf = bytes(npos)
            ier = _cxtgeo.xtg_get_fbuffer(self._fhandle, buf)
            if ier == 0:
                self._name.write(buf)  # write to bytesIO instance
                _cxtgeo.xtg_fflush(self._fhandle)
            else:
                raise RuntimeError("Could not write stream for unknown reasons")

        if self._fhandle:
            ier = _cxtgeo.xtg_fclose(self._fhandle)
            if ier != 0:
                raise RuntimeError("Could not close C file, code {}".format(ier))

            logger.debug("File is now closed %s", self._fhandle)

            if self._tmpfile:
                try:
                    os.remove(self._tmpfile)
                except Exception as ex:  # pylint: disable=W0703
                    logger.error("Could not remove tempfile for some reason: %s", ex)

            return True

        return False
