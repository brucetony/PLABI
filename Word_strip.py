from collections import defaultdict


def word_reduction(some_word, word_dictionary):
    i = 0
    result = some_word
    while i < len(some_word):
        letters = list(some_word)
        del letters[i]
        new_word = ''.join(letters)
        if new_word is '':
            print('Yay')
            return True
        elif new_word in word_dictionary[len(new_word)]:
            result = word_reduction(new_word, word_dictionary)
            break
        else:
            i += 1
    if result is True:
        return True
    else:
        return some_word

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
    nonreducable_words = set()

    #Go through each word and ieratively remove a letter and check if still a word
    for key in list(word_dict.keys())[:2:-1]:
        for word in word_dict[key]:
            if word not in nonreducable_words or reducable_words:
                attempt = word_reduction(word, word_dict)
                reducable_words.add(word) if attempt is True else nonreducable_words.add(attempt)
    return reducable_words

longest_word('words.txt')