from typing import TextIO
import string

wordlist = []
listfile = open('valid_words.csv')
word = listfile.readline().strip()
while word != '':
    wordlist.append(word)
    word = listfile.readline().strip()

alphabet_list = list(string.ascii_lowercase)
# A dictionary with alphabet as key and list of occurance 
# in each index of the word in wordlist as a value. 
# The value of each alphabet is initially [0, 0, 0, 0, 0]
alphabet_dict = {}
for alphabet in alphabet_list:
    alphabet_dict[alphabet] = [0, 0, 0, 0, 0]

guess = ''
feedback = ''


def suggest() -> str:
    update_wordlist(guess, feedback)
    calculate_frequency()
    
    score_dict = {}
    max_freq = [0, 0, 0, 0, 0]

    for letter in alphabet_dict:
        for i in range(5):
            if max_freq[i] < alphabet_dict[letter][i]:
                max_freq[i] = alphabet_dict[letter][i]

    for word in wordlist:
        score = 1
        for i in range(5):
            score *= 1 + (alphabet_dict[word[i]][i] - max_freq[i]) ** 2
        score_dict[word] = score

    best_word = ''
    best_score = 10**100
    for word in score_dict:
        if best_score > score_dict[word]:
            best_word = word
            best_score = score_dict[word]
            print(best_score, best_word)
    return best_word


def calculate_frequency():
    for alphabet in alphabet_dict:
        alphabet_dict[alphabet] = [0, 0, 0, 0, 0]
    for word in wordlist:
        for i in range(5):
            alphabet_dict[word[i]][i] += 1


def update_wordlist(guess: str, feedback: str):
    for i in range(5):
        colour = feedback[i]
        letter = guess[i]
        for word in wordlist:
            if feedback[i] == 'g' and word[i] != guess[i]:
                wordlist.remove(word)
            elif feedback[i] == 'y' and ((guess[i] not in word) or (word[i] == guess[i])):
                wordlist.remove(word)
            elif feedback[i] == 'w' and guess[i] in word:
                wordlist.remove(word)
    for word in wordlist:
        for i in range(5):
            if feedback[i] == 'w':
                if guess[i] in word:
                    print('Bug here, in ', word)


# for i in range(6):
#     guess = input('Enter your guess: ')
#     print('g - green, y - yellow, w - wrong / grey')
#     feedback = input('Feedback: ')
#     if feedback == 'ggggg':
#         print(f'Congratulations! You got the word in {i + 1} guesses.')
#         break
#     else:
#         suggestion = suggest()
#         print(f'I suggest trying: {suggestion}')
#         print(len(wordlist), 'words')

# if feedback != 'ggggg':
#     print('Sorry, end of your wordle streak.')