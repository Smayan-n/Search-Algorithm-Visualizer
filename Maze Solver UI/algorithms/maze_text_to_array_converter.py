
def convertTextFile(filename):
    '''converts text file and strings to 2D array'''
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    template = []
    for line in lines:
        line = line.strip("\n")
        row = list(line)
        template.append(row)

    return template


def ConvertString(string):
    '''converts string to 2D array'''
    lines = string.splitlines()

    template = []
    for line in lines:
        line = line.strip("\n")
        row = list(line)
        template.append(row)
    return template