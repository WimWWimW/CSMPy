from csmp import CSMPy



        
        
if __name__ == '__main__':
    import sys
    
    csmp = CSMPy()        
    csmp.compile("./models/test.csm.py")
    
    print("\n", '-'*80, '\n')
    if csmp.compiled:
        csmp.model.writeTemplate()
    else:
        csmp.model.writeListFile(sys.stdout)
