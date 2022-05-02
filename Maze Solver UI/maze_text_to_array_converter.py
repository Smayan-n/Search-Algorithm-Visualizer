#converts text file and strings to 2D array
def convertTextFile(filename):
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    template = []
    for line in lines:
        line = line.strip("\n")
        row = list(line)
        template.append(row)

    return template

def ConvertString(string):
    lines = string.splitlines()

    template = []
    for line in lines:
        line = line.strip("\n")
        row = list(line)
        template.append(row)
    return template