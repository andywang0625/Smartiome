import sys
import platform

SYSTEMVERSION = "April(Beta)"

def getSystemVersion():
    return SYSTEMVERSION

def getLastSupportedVersion():
    return SYSTEMVERSION

def getPythonVersionInfo():
    a = sys.version.split(" ", maxsplit=1)
    b = a[1].split(")", maxsplit=1)
    c = b[1].split("[")
    verstr = a[0]
    detailver = b[0].lstrip("(")
    compiler = c[1].rstrip("]")
    return verstr, detailver, compiler

def getPlatform():
    return platform.platform()
