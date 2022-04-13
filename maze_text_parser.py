#converts text file to 2D array
def parseTextFile(filename):
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    template = []
    for line in lines:
        line = line.strip("\n")
        row = list(line)
        template.append(row)

    return template