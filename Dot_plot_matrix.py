import numpy as np
np.set_printoptions(threshold=np.inf)

def dotplot(seqA, seqB, w, s):
    '''
    Function that takes 2 strings and compares each letter to every other letter in sequence.
    If there are at least s matches in a width w, then a 1 will be printed in the matrix at that position.
    :param seqA: Some string possibly a DNA sequence or sentence
    :param seqB: A second string to be compared
    :param w: Width of the compared strings (position i +- (w-1)/2
    :param s: Required number of matches within compared substrings to designate a a "positive" result
    :return: A numpy matrix with 1 at positions where substrings of length w "match"
    '''
    M = len(seqA)
    N = len(seqB)
    dotplot = np.zeros((M, N), dtype=int)
    dis = (w-1)/2
    for i in range(M):
        for j in range(N):
            #Create assignments for substring slicing
            startA = int(i-dis)
            endA = int(i+dis)
            startB = int(j-dis)
            endB = int(j+dis)

            #In case the window is at the beginning or end
            if startA < 0:
                startA = 0
            if startB < 0:
                startB = 0
            if endA > M:
                endA = M
            if endB > N:
                endB = N

            #Create the substrings
            subA = seqA[startA:endA]
            subB = seqB[startB:endB]

            #Can only compare using smaller length
            sub_length = min(len(subA), len(subB))

            num_matches = 0
            for k in range(sub_length):
                if list(subA)[k] == list(subB)[k]:
                    num_matches += 1

            #Change position to 1 if a match
            if num_matches >= s:
                dotplot[i, j] = 1

    return dotplot


def dotplt2Ascii(dp, seqA, seqB, heading, filename):
    M = len(seqA)
    N = len(seqB)

    with open(filename, 'w') as outputFile:
        outputFile.write('{}\n\n |{}\n'.format(heading, seqB))
        outputFile.write('-+{}\n'.format('-'*N))
        for i in range(M):
            outputFile.write('{}|'.format(list(seqA)[i]))
            for num in dp[i]:
                if num == 0:
                    outputFile.write(' ')
                else:
                    outputFile.write('*')
            outputFile.write('\n')


seqA = "peter piper picked a peck of pickled peppers"
seqB = "a peck of pickled peppers peter piper picked"
peter_plot = dotplot(seqA, seqB, 5, 4)

dotplt2Ascii(peter_plot, seqA, seqB, 'Peter Piper Bruce Plot', 'BSpeter.txt')
