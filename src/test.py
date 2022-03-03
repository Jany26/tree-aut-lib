from format_vtf import *
from normalization import normalize
from ta_functions import *
from test_data import fullAlphabet

if __name__ == '__main__':
    ta = importTAfromVTF("tests/normalizationTest3.vtf", 'f')
    symbols = ta.getSymbolArityDict()
    variables = [f"x" + f"{i+1}" for i in range(3)]
    normalize(ta, symbols, variables)


# End of file main.py
