# %matplotlib inline #For jupyter notebook
import numpy as np
import matplotlib.pylab as plt

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
    '''
    Creates ASCII art using a numpy matrix as input and writes the compared strings on the axes
    :param dp: Numpy dotplot made of 1's and 0's
    :param seqA: String
    :param seqB: String
    :param heading: Title to be posted at the top of file
    :param filename: output file name (including the extension)
    :return:
    '''
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

def dotplot2Graphics(dp, hdA, hdB, heading):
    '''
    Uses a numpy dotplot used for comparing two strings and saves it as a figure (.png, .pdf, etc)
    :param dp: Numpy dotplot
    :param hdA: String A
    :param hdB: String B
    :param heading: Title
    :param filename: output filepath
    :return: Figure
    '''

    #Collect list of points
    points = []

    #Add points to a list if point in array == 1
    for i in range(len(dp)):
        for j in range(len(dp[i])):
            if dp[i][j] == 1:
                points.append((j, i))

    fig, ax = plt.subplots()
    dotplot = ax.scatter(*zip(*points), marker="+", s=2)

    # Unzip points and plot them
    plt.gca().invert_yaxis()
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    plt.xlabel(hdB)
    plt.ylabel(hdA, rotation=0)

    plt.title(heading, y=1.15)
    plt.show()


seqA = "peter piper picked a peck of pickled peppers"
seqB = "a peck of pickled peppers peter piper picked"
dp = dotplot(seqA, seqB, 5, 4)
dotplot2Graphics(dp, seqA, seqB, "Peter Piper")