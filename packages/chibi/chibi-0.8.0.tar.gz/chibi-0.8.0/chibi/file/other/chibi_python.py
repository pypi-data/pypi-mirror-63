import json
from chibi.file import Chibi_file
from chibi.atlas import _wrap
from chibi.module import import_


__all__ = [ 'Chibi_python' ]


class Chibi_python( Chibi_file ):
    def read( self ):
        value = super().read()
        return value
