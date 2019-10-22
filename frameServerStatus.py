'''
FrameServerStatus v1.1

Written by Jeang Jenq Loh
Last updated 05 May 2019

Panel to display currently running frame server slaves
'''

import nuke
import nukescripts
from socket import gethostname
# import PySide for modifying clipboard
try:
    from PySide2 import QtWidgets
except:
    from PySide import QtGui as QtWidgets

def frameServerCommand():
    from hiero.ui.nuke_bridge.FnNsFrameServer import frameServer
    return [worker.address for worker in frameServer.getStatus(1).workerStatus]

# get a list of workers as multiline string
def frameServerWorkers():
    # convert list of workers into a list that can be index
    frameServerOutput = []
    [frameServerOutput.append(worker) for worker in frameServerCommand()]

    # convert list of slaves into multiline string
    AllworkersList = frameServerOutput[0:]
    each = "\n".join(AllworkersList)

    slaves = []
    slavesWorkers = []
    hostWorkers = []
    # Working on sorting out slaves and reorganizing them
    for worker in frameServerOutput:
        slave = worker.rsplit(" ").__getitem__(3)
        if not slave == gethostname():
            slavesWorkers.append(worker)
            if slave not in slaves:
                slaves.append(slave)
        else:
            if slave in worker:
                hostWorkers.append(worker)
    return [hostWorkers, slavesWorkers, AllworkersList, slaves]


class FrameServerStatus(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, 'Frame Server Status', 'FSPanel')
        # multiline text field to display workers
        self.host = nuke.Text_Knob('host', 'Host:', gethostname())
        self.hostWorkers = nuke.Multiline_Eval_String_Knob('hostWorkers', 'Workers on host', '')
        self.hostRunning = nuke.Int_Knob('hostRunning', 'Workers on host')
        self.div1 = nuke.Text_Knob('div1', '')
        self.slavesWorkers = nuke.Multiline_Eval_String_Knob('slavesWorkers', 'Workers on slaves', '')
        # data data data
        self.slavesRunning = nuke.String_Knob('slavesRunning', 'Slaves running')
        self.numOfSlaves = nuke.Int_Knob('numOfSlaves', 'Total Slaves')
        self.numOfWorkers = nuke.Int_Knob('numOfWorkers', 'Total Workers')
        self.workersPerSlave = nuke.Int_Knob('workersPerSlave', 'Workers per Slaves')
        # buttons to refresh/copy
        self.refresh = nuke.PyScript_Knob('refresh', 'Refresh')
        self.showCommand = nuke.PyScript_Knob('showCommand', 'Copy workers\' list command')

        # add knobs
        for knob in [self.refresh, self.slavesRunning, self.numOfSlaves, self.workersPerSlave, self.div1]:
            knob.setFlag(0x1000)
        for knob in [self.host, self.hostWorkers, self.hostRunning, self.div1, self.slavesWorkers, self.slavesRunning, self.numOfSlaves, self.numOfWorkers, self.workersPerSlave, self.refresh, self.showCommand]:
            self.addKnob(knob)

    def knobChanged(self, knob):
        if knob is self.refresh:
            print knob.name()
            slavesWorkers = '\n'.join(frameServerWorkers()[1])
            hostWorkers = '\n'.join(frameServerWorkers()[0])
            slavesRunning = ', '.join(frameServerWorkers()[3])
            numSlaves = len(frameServerWorkers()[3])
            numSlavesWorkers = len(frameServerWorkers()[1])
            if numSlaves == 0:
                workersPerSlave = 0
            else:
                workersPerSlave = int(int(numSlavesWorkers)/int(numSlaves))
            numHostWorkers = len(frameServerWorkers()[0])

            self.slavesWorkers.setValue(slavesWorkers)
            self.hostWorkers.setValue(hostWorkers)
            self.slavesRunning.setValue(slavesRunning)
            self.numOfSlaves.setValue(numSlaves)
            self.numOfWorkers.setValue(numSlavesWorkers)
            self.workersPerSlave.setValue(workersPerSlave)
            self.hostRunning.setValue(numHostWorkers)

        elif knob is self.showCommand:
            # copyFScommand()
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText('from hiero.ui.nuke_bridge.FnNsFrameServer import frameServer\nprint [worker.address for worker in frameServer.getStatus(1).workerStatus]')


# register panel
def addFSpanel():
    global FSpanel
    FSpanel = FrameServerStatus()
    return FSpanel.addToPane()

paneMenu = nuke.menu('Pane')
paneMenu.addCommand('Frame Server Status', addFSpanel)
nukescripts.registerPanel('FSPanel', addFSpanel)