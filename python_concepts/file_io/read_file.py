
# path to file
f = './data/example.txt'
# use the open function in read 'r' mode
with open(f, 'r') as readin:
    # read in line per line
    lines = readin.readlines()
    for line in lines:
        print (line)
