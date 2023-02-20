# Use p-code emulation and emulate some codes
#@author jjnutte
#@category EMU
#@menupath EMU.pyemu

from registers import Registers
from emulation import Emulation
from maps import Maps
from __main__ import currentProgram

def main():
    #Msg.showError(None, None, "Error", "Error doing whatever")
    
    registers = Registers(currentProgram)
    Emulation(currentProgram, registers)


if __name__ == "__main__":
    main()