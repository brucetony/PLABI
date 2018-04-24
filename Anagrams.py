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