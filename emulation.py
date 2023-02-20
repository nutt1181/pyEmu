from javax.swing import *
from java.lang import *
from javax.swing.table import DefaultTableModel
from java.awt import Dimension
from javax.swing import JButton, JFrame,JPanel,BoxLayout,Box,SwingConstants,WindowConstants
from ghidra.app.emulator import EmulatorHelper
from ghidra.program.model.symbol import SymbolUtilities
from ghidra.util.task import ConsoleTaskMonitor

from __main__ import *
import ctypes

from registers import getRegValue

def setAllRegisters(currentProgram, emuHelper, registers):
    pc = currentProgram.getProgramContext()
    intreg = 0
    for i in pc.registers:
        if i:
            reg = getRegValue(currentProgram, i)
            if reg == 0:
                emuHelper.writeRegister(i, 0)
            else:
                intreg = int(reg, 16)
                emuHelper.writeRegister(i, intreg)

            if str(i) == "cr15":
                break
        else:
            break
    return

def updateRegisters(currentProgram, emuHelper, registers):
    pc = currentProgram.getProgramContext()
    for i in pc.registers:
        reg = emuHelper.readRegister(i)
        registers.setRegValue(currentProgram, i, reg)
    return


class Emulation:
    def stepAction(self,event):
        currentProgram = self.currentProgram
        registers = self.registers
        emuHelper = EmulatorHelper(currentProgram)
        listing = currentProgram.getListing()
        pc = int(getRegValue(currentProgram, "pc"), 16)
        stackPointer = int(getRegValue(currentProgram, "sp"), 16)

        if pc > 0 and stackPointer > 0:

            setAllRegisters(currentProgram, emuHelper, registers)
            
            if self.monitor.isCancelled() is False:
                executionAddress = emuHelper.getExecutionAddress()  
                success = emuHelper.step(self.monitor)
                instr = getInstructionAt(executionAddress)
                if (success == False):
                    #print instruction and skip over it
                    print("%s: %s %s" % (executionAddress, instr, "emulation error, skipping instruction"))
                    instr = getInstructionAfter(executionAddress)
                    newAddr = instr.getAddress().getAddressableWordOffset()
                    registers.setRegValue(currentProgram, "pc", newAddr)
                else:
                    print("%s: %s %s" % (executionAddress, instr, "emulation success"))
                    
                    updateRegisters(currentProgram, emuHelper, registers)

        elif pc == 0 and stackPointer > 0:
            print("check if pc is valid instruction")
        else:
            print("no gud")
        return

    def stepOverAction(self,event):
        return

    def resetAction(self,event):
        return

    def __init__(self, currentProgram, registers):
        # These lines setup the basic frame, size.
        # the setDefaultCloseOperation is required to completely exit the app
        # when you click the close button
        frame = JFrame()
        frame.setTitle("PyEmu Emulation")
        frame.setSize(400, 100)
        
        panel = JPanel()
        panel.setLayout(BoxLayout(panel, BoxLayout.Y_AXIS))
        frame.add(panel)

        top = JPanel()
        top.setLayout(BoxLayout(top, BoxLayout.X_AXIS))
        textfield1 = JTextField(10)
        textfield1.setMaximumSize(Dimension(Integer.MAX_VALUE, textfield1.getPreferredSize().height))
        textfield2 = JTextField(10)
        textfield2.setMaximumSize(Dimension(Integer.MAX_VALUE, textfield2.getPreferredSize().height))
        
        top.add(Box.createVerticalGlue())
        top.add(JLabel("start addr:"))
        top.add(textfield1)
        top.add(Box.createRigidArea(Dimension(25,0)))
        top.add(JLabel("end addr:"))
        top.add(textfield2)

        bottom = JPanel()
        bottom.setLayout(BoxLayout(bottom, BoxLayout.X_AXIS))
        stepButton = JButton('Step', actionPerformed = self.stepAction)
        stepOverButton = JButton('Step Over', actionPerformed = self.stepOverAction)
        resetButton = JButton('Reset', actionPerformed = self.resetAction)
        bottom.add(stepButton)
        bottom.add(Box.createRigidArea(Dimension(25,0)))
        bottom.add(stepOverButton)
        bottom.add(Box.createRigidArea(Dimension(25,0)))
        bottom.add(resetButton)
        bottom.add(Box.createVerticalGlue())
        
        panel.add(top)
        panel.add(bottom)
        
        frame.setVisible(True)
        self.currentProgram = currentProgram
        self.monitor = ConsoleTaskMonitor()
        self.registers = registers
        emuHelper = EmulatorHelper(currentProgram)