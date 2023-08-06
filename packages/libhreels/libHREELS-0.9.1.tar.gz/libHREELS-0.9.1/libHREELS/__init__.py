# necessary for this directory to be a module
# __init__.py

from libHREELS.HREELS import HREELS
from libHREELS.HREELS import offset, createDataDictionary, HREELS_elog_Dictionary
from libHREELS.LEED import LEED, LEED_elog_Dictionary
from libHREELS.Auger.Auger import Auger, Auger_elog_Dictionary
from libHREELS.ViewHREELS import HREELS_Window
import libHREELS.ViewHREELS as ViewHREELS
import libHREELS.ViewAuger as ViewAuger

from libHREELS.calcHREELS import importMaterials
from libHREELS.calcHREELS import lambin
import libHREELS.myEels2 as myEels2    # wrapper for myEels2.f90
import libHREELS.myBoson as myBoson  # wrapper for myBoson.f90

# __all__ = ["HREELS","LEED", "Auger/Auger", "ViewHREELS"]

__version__ = '0.9.1'
