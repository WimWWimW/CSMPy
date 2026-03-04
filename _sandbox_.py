from functions import *
from keywords  import *
from csmp import CSMP_Model

        

class SimulationModel(CSMP_Model):

    def defineConstants(self):
        """ -/- """
        return locals()

    def defineParameters(self):
        """ -/- """
        CVF = PARAM(0.7)
        GPHST = PARAM(400.0)
        return locals()

    def setUp(self):
        globals().update(self.defineConstants())
        globals().update(self.defineParameters())
        globals().update(self.initial())
        
        ':initStates:'
        self.createStateVariable(0, 'WSH', WSHI)
        self.createStateVariable(1, 'WRT', WRTI)
        ':systemParams:'
        self.setTitle('DRY MATTER PRODUCTION')
        self.setTimer(FINTIM=100.0, DELT=1.0, PRDEL=5.0, OUTDEL=5.0)
        self.setMethod('RECT')
        self.setPrint('TWT', 'WSH', 'WRT', 'GTW')
        self.setOutput('TWT')

    def initial(self):
        """
        Initialization-block called before the loop is started.
        All variables created here will persist in the global scope,
        unless explicitly deleted.
        note: parameters and constants have been created above
              and may be used here.
        """
        ':incons:'
        WSHI = INCON(50.0)
        WRTI = INCON(50.0)
        ':initial:'
        return locals()

    def loop(self, time):
        """
        Called each time step and also in between,
        if the integration method requires so.
        """
        ':commonBlock:'
        ':restoreValues:'
        WSH = self.getState(0)
        WRT = self.getState(1)
        ':dynamic:'
        TWT = WSH + WRT
        MAINT = (WSH + WRT) * 0.015
        LAI = AMIN1(WSH / 500.0, 5.0)
        GPHOT = GPHST * (1.0 - EXP(-0.7 * LAI))
        GTW = (GPHOT - MAINT) * CVF
        GSH = 0.7 * GTW
        GRT = 0.3 * GTW
        ':update:'
        self.setCurrentRate(0, GSH)
        self.setCurrentRate(1, GRT)
        
        return locals() # ??
        

    def final(self):
        """ 
        End condition has been met. 
        Final actions to take.
        """

    def run(self):
        def printVar(x):
            print("%12g" % x, end = "")
        
        self.timer.start()
        
        while True:
            v = self.loop(self.timer.time)
            
            if self.timer.printRequired():
                print("%.8E" % self.timer.time, end = "")
                printVar(v.get("TWT", -99999))
                printVar(self.stateNames["WSH"].value)
                printVar(self.stateNames["WRT"].value)
                printVar(v.get("GTW", -99999))
                print()
            
            self.integrator.run(self.stateVariables.values())
            if not self.timer.setTimeStep():
                break
            
            
m = SimulationModel()
m.setUp()
m.run()