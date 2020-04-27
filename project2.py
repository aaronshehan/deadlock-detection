from sys import argv
import re
try: 
    import queue
except ImportError:
    import Queue as queue

def readFile(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            if not line.strip():
                continue
            else:
                lines.append(line.strip())
    return lines

def parseLines(lines):
    num_processes = None
    num_resources = None
    units = None
    matrix = []

    for line in lines:
        if re.search('^%.*$', line):
            continue
        elif re.search('num_processes=', line):
            num_processes = int(line.split('=')[1])
        elif re.search('num_resources=', line):
             num_resources = int(line.split('=')[1])
        elif re.search('^[0-9]+,[0-9]+,[0-9]+$', line):
            units = [int(i) for i in line.split(',')]
        elif re.search('^([01]+,)*[01]$', line):
            matrix.append([int(i) for i in line.split(',')])

    return (num_processes, num_resources, units, matrix)


def bfs(matrix, start):
    q = queue.Queue()
    q.put(start)
    visited = {start: True}
    
    while not q.empty():
        current_node = q.get()
        
        for i, j in enumerate(matrix):
            if matrix[current_node][i] != 0 and i not in visited:
                q.put(i)
                visited[i] = True

    return visited


def main(filename):
    parsedInfo = parseLines(readFile(filename))
    num_processes = parsedInfo[0]
    num_resources = parsedInfo[1]
    units = parsedInfo[2]
    matrix = parsedInfo[3]

    count = 0
    for i in range(len(matrix)):
        visited = bfs(matrix, i)

        if len(visited) == len(matrix):
            count += 1

    if count == len(matrix):
        print('Deadlocks exists.')
    else:
        print('Deadlock does not exist.')


if __name__ == '__main__':
    main(argv[1])
