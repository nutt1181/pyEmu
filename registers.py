from javax.swing import *
from java.lang import *
from javax.swing.table import DefaultTableModel
from java.awt import *
from javax.swing import *

from ghidra.program.model.lang import Register
from ghidra.program.model.listing import Program

from ghidra.program.model.symbol import SymbolUtilities
from ghidra.app.emulator import EmulatorHelper
from javax.swing.event import TableModelListener


columnNames = {"Register", "Value"}
regData = []
globalDataModel = lambda:None

def getProgramRegisterList(currentProgram):
    emuHelper = EmulatorHelper(currentProgram)
    pc = currentProgram.getProgramContext()
    for i in pc.registers:
        
        regData.append([i,0])
    return regData

def getRegValue(currentProgram, register):
    emuHelper = EmulatorHelper(currentProgram)
    pc = currentProgram.getProgramContext()
    
    reg = 0
    for i in pc.registers:
        if str(i) == str(register):
            break
        else:
            reg = reg + 1
    return regData[reg][1]



class Registers:
    def copyText(self,event):
        self.textfield2.text = self.textfield1.text
    
    def setRegValue(self, currentProgram, register, value):
        emuHelper = EmulatorHelper(currentProgram)
        pc = currentProgram.getProgramContext()
        
        reg = 0
        for i in pc.registers:
            if str(i) == str(register):
                break
            else:
                reg = reg + 1
        stringVal = hex(value)
        stringVal = stringVal[2:]
        stringVal = stringVal[:-1]
        self.dataModel.setValueAt(stringVal, reg, 1)

    def __init__(self, currentProgram):
        # These lines setup the basic frame, size.
        # the setDefaultCloseOperation is required to completely exit the app
        # when you click the close button
        print("registers")
        self.currentProgram = currentProgram
        regs = getProgramRegisterList(currentProgram)
        
        frame = JFrame("PyEmu Registers")
        frame.setSize(400, 700)
        frame.setLayout(BorderLayout())
        
        colNames = ('Register','Value')
        dataModel = DefaultTableModel(regs, colNames)
        self.table = JTable(dataModel)
        dataModel.addTableModelListener(MyTableModelListener())

        scrollPane = JScrollPane()
        scrollPane.setPreferredSize(Dimension(390,690))
        scrollPane.getViewport().setView((self.table))
        panel = JPanel()
        panel.add(scrollPane)
        
        frame.add(panel, BorderLayout.CENTER)
        frame.setVisible(True)
        self.dataModel = dataModel
        globalDataModel = dataModel

class MyTableModelListener(TableModelListener):
    def tableChanged(self, e):
        row = e.getFirstRow()
        col = e.getColumn()
        model = e.getSource()
        data = model.getValueAt(row, col)
        regData[row][col] = data

