from csmp.precompiler import Precompiler



if __name__ == '__main__':
            
    mdl = Precompiler("./models/test.csm.py")
    print("\n", '-'*80, '\n')
    mdl.saveListFile(True)
    print("\n", '-'*80, '\n')
    mdl.debugSegmentation()
    mdl.printSummary()