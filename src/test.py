from format_vtf import *
from normalization import compressVariables, normalize
from ta_functions import *
from test_data import fullAlphabet

if __name__ == '__main__':
    ta = importTAfromVTF("tests/normalizationTest2.vtf", 'f')
    symbols = ta.getSymbolArityDict()
    variables = [f"x" + f"{i+1}" for i in range(5)]
    xy = normalize(ta, symbols, variables)
    compressVariables(xy)
    

# End of file main.py
