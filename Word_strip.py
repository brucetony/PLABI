from collections import defaultdict

def longest_word(filePath):
    #Read list of words and assemble into list
    with open(filePath, 'r') as file:
        word_list = list(file.read().splitlines())

    #Create dictionary with keys beings the length of a word
    word_dict = defaultdict(list)
    for word in word_list:
        word_dict[len(word)].append(word)
    word_dict[0].append('')

    reducable_words = set()

    #Go through each word and ieratively remove a letter and check if still a word
    for key in list(word_dict.keys())[2:]:
        for word in word_dict[key]:
            i = 0
            while i < len(word):
                letters = list(word)
                del letters[i]
                new_word = ''.join(letters)
                if new_word in word_dict[key-1]:
                    reducable_words.add(word)
                    break
                i += 1
    return reducable_words

#longest_word('words.txt')
