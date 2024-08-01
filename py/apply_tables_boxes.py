from apply_testing import BooleanOperation

# TODO: Figure out what kind of information should be stored wrt. to ports
# TODO: Find out an efficient way to store and use this info
class PortConnectionInfo:
    def __init__(self, recursive: bool, op: BooleanOperation, negation: bool):
        self.operation = op
        self.negation = negation
        self.attach = (None, None)
    def __repr__(self):
        pass


AND_table = {
    'X': {
        'X': (),
        'L0': (),
        'L1': (),
        'H0': (),
        'H1': (),
        },
    'L0': {},
    'L1': {},
    'H0': {},
    'H1': {},
}
