# def find_anagram(filePath):
#     '''
#     :param filePath: Enter filepath to a txt file with a list of words to check for anagrams
#     :return: A continous print out of lists of words that are anagrams
#     '''
#     with open(filePath, 'r') as file:
#         words = list(file.read().splitlines()) #Split into proper words
#         dict_words = dict(enumerate(words))
#         k = 0
#         anagrammed_words = set() #Used to check words that have been associated with another word already
#         while k < len(words):
#             anagrams = []
#             prim = words[k] #This is the primary word to be compared against
#             if prim not in anagrammed_words:
#                 anagrams.append(prim) #Add to temporary list
#                 str_prim = list(prim) #Split string into letters
#                 str_prim.sort() #Sort the letters
#                 for sec in words[k+1:]:
#                     str_sec = list(sec)
#                     str_sec.sort()
#                     if str_prim == str_sec: #Compare target and primary words using sorted letters
#                         anagrams.append(sec) #If they match then add to temp anagram list
#                         anagrammed_words.add(prim)
#                         anagrammed_words.add(sec) #If they match add to exclude list
#             if len(anagrams) >= 6:
#                 print(anagrams)
#             k += 1

def find_anagram(filePath):
    with open(filePath, 'r') as file:
        word_list = list(file.read().splitlines())
        word_dict = dict(enumerate(word_list)) #Split into proper words
        word_dict = {v: k for k, v in word_dict.items()} #Make words the keys with ascending values
        done_words = set() #Set of values used to if a word is already in anagram list or been checked already
        position = 0 #To slice the word list later
        anagram_list = []
        for word, value in word_dict.items():
            position += 1 #Forward the counter
            if value not in done_words:
                done_words.add(value)
                anagrams = [word]
                for next_word in word_list[position:]:
                    str_prim = list(word)  # Split string into letters
                    str_prim.sort()  # Sort the letters
                    str_sec = list(next_word)
                    str_sec.sort()
                    if str_prim == str_sec:
                        anagrams.append(next_word)
                        done_words.add(word_dict[next_word])
            if len(anagrams) >= 6:
                anagram_list.append(anagrams)
                print(anagrams)
        anagram_list.sort(key=len) #Show largest anagram set first
        return anagram_list

find_anagram("C:/Users/Bruce/Google Drive/b-it/Programming Lab I/words.txt")


