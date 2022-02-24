from format_vtf import *
from format_dot import *

if __name__ == '__main__':
    ta = importTAfromVTF("tests/unfoldingTest3.vtf", 'f')
    exportTreeAutToDOT(ta, "unfoldingTest4.dot")    


# End of file main.py
