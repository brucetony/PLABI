from collections import defaultdict

#Use defaultdict as it easily allows for lists to be created in dict
def find_anagrams(filePath):
    six_plus_anagrams = []
    eight_letter_anagrams = []
    with open(filePath, 'r') as file:
        word_list = list(file.read().splitlines())
    screener = defaultdict(list)
    for word in word_list:
        key = ''.join(sorted(word))
        screener[key].append(word)
    for key, anagrams in screener.items():
        if len(anagrams) >= 6:
            six_plus_anagrams.append(anagrams)
            if len(key) >= 8:
                eight_letter_anagrams.append(anagrams)
    six_plus_anagrams.sort(key=len) #Sort smallest lists first
    eight_letter_anagrams.sort(key=len) #Sort
    for anagram_list in six_plus_anagrams[::-1]: #Slice it so largest is first
        print(anagram_list)
    print(eight_letter_anagrams[-1]) #Returns last element in list (largest)

find_anagrams("words.txt")

# def find_anagram(filePath):
#     '''
#     :param filePath: Enter filepath to a txt file with a list of words to check for anagrams
#     :return: A continous print out of lists of words that are anagrams
#     '''
#     with open(filePath, 'r') as file:
#         words = list(file.read().splitlines())  # Split into proper words
#         k = 0
#         anagrammed_words = set()  # Used to check words that have been associated with another word already
#         while k < len(words):
#             anagrams = []
#             prim = words[k]  # This is the primary word to be compared against
#             if prim not in anagrammed_words:
#                 anagrams.append(prim)  # Add to temporary list
#                 str_prim = list(prim)  # Split string into letters
#                 str_prim.sort()  # Sort the letters
#                 for sec in words[k + 1:]:
#                     str_sec = list(sec)
#                     str_sec.sort()
#                     if str_prim == str_sec:  # Compare target and primary words using sorted letters
#                         anagrams.append(sec)  # If they match then add to temp anagram list
#                         anagrammed_words.add(prim)
#                         anagrammed_words.add(sec)  # If they match add to exclude list
#             if len(anagrams) >= 6:
#                 print(anagrams)
#             k += 1