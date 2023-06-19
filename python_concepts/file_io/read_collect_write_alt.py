from subprocess import call

# path to file
f = './data/example.txt'

# use subprocess call to execute a shell command instead

command = """grep 'energy' %s | awk '{print ($NF)}' > energy_only2.txt""" % f

call(command, shell = True)



