from ROOT import TTree, TFile
from array import array
class GetResult:
    def __init__(self,log="log0000"):
        self._log = log
    def SetLog(self, log):
        self._log = log
    def FCN(self):
        for line in open(self._log):
            if not "RooFitResult:" in line :
                continue
            ll = line.split()
            ii  = ll.index("value:")
            return float(ll[ii+1].split(",")[0])
    def GetVal(self, var="sigma"):
        ll = []
        ll2=[]
        for line in open(self._log):
            if len(line.split())==0:
                continue
            if line.split()[0] == var and r"+/-" in line:
                #print line
                ll = line.split()
            if line.split()[0]==var and len(line.split())==2:
                ll2 = line.split()
                #break
        if len(ll) !=0:
            ii = ll.index(r"+/-")
            return float( ll[ii-1])
        if len(ll2) !=0:
            return float(ll2[-1])
        return self.FF(var)
        return 0.0
    def GetError(self, var="sigma"):
        ll = []
        ll2=[]
        for line in open(self._log):
            if len(line.split())==0:
                continue
            if line.split()[0] == var and r"+/-" in line:
                #print line
                ll = line.split()
            if line.split()[0]==var and len(line.split())==2:
                ll2 = line.split()
                #break
        if len(ll) !=0:
            ii = ll.index(r"+/-")
            return float( ll[ii+1])
        if len(ll2) !=0:
            return float(ll2[-1])
        return self.FF(var)
        return 0.0
    def FF(self, var="a0"):
        ll=[]
        for line in open(self._log):
            if not "Fraction::" in line:
                continue
            if var in line:
                ll = line.split()
        if len(ll) >0 :
            return float(ll[-1])
        else:
            return 0.0
    def WriteToFile(self, inputval = [], output = "out.root"):
        fout= TFile(output , "recreate")
        tout=TTree("sig", "")
        val = array("d",[0.0])
        tout.Branch("val", val, "val/D")
        for i in inputval:
            val[0] = i
            tout.Fill()
        tout.Write()
        fout.Close()


