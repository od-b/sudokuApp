
def addCommas(path):
    npath = path.rstrip('.csv') + '_fix.csv'
    with open(path, 'r') as istr:
        with open(npath, 'w') as ostr:
            for line in istr:
                line = line.rstrip('\n') + ','
                print(line, file=ostr)


if __name__ == '__main__':
    fp = './sudoku_expert_5000.csv'
    addCommas(fp)
    fp2 = './sudoku_intermediate_5000.csv'
    addCommas(fp2)
