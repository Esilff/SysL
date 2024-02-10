import ctypes

class SysL:

    def __init__(self):
        self.sysl = ctypes.CDLL(r"C:\Users\Esilff\Git\SysL\SysL\cmake-build-release-visual-studio\SysL.dll")
        self.load_functions()

    def get_tortoise(self):
        return self.sysl.getTortoiseSystem()

    def add_rule(self, tortoise, expression: str):
        self.sysl.addRule(tortoise, expression.encode('utf-8'))

    def generate_axiom(self, tortoise, axiom: str, iterations):
        return self.sysl.generateAxiom(tortoise, axiom.encode('utf-8'), iterations).decode('utf-8')

    def load_functions(self):
        try:
            self.sysl.getTortoiseSystem.restype = ctypes.c_void_p

            self.sysl.addRule.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
            self.sysl.removeRule.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
            self.sysl.addRule.argtypes = [ctypes.c_void_p]
            self.sysl.generateAxiom.restype = ctypes.c_char_p
            self.sysl.generateAxiom.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint]
        except Exception as e:
            print("[SysL:DLL] : An exception occured while loading the functions: " + str(e))