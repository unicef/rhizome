from os.path import dirname, basename, isfile
import glob

# Treat folder as module and access all the Clases in this folder
modules = glob.glob(dirname(__file__) + "/*.py")
__all__ = [basename(f)[:-3] for f in modules if isfile(f)]
