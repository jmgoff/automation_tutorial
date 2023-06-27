from subprocess import call

call('python subrun_qe_calcs.py &> outrunall.txt &',shell = True)
