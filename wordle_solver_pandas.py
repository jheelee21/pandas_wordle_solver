import pandas as pd
import string

word_dict = {0: [], 1: [], 2: [], 3: [], 4: []}
listfile = open('valid_words.csv')
word = listfile.readline().strip()
while word != '':
    for i in range(5):
        word_dict[i].append(word[i])
    word = listfile.readline().strip()
df = pd.DataFrame(word_dict)

# A dictionary with alphabet as key and list of occurance in 
# each index of the word in wordlist as a value. 
alphabet_list = list(string.ascii_lowercase)
alphabet_dict = {}
for alphabet in alphabet_list:
    alphabet_dict[alphabet] = [0, 0, 0, 0, 0]

guess = ''
feedback = ''


def calculate_frequency():
    for alphabet in alphabet_list:
        for i in range(5):
            alphabet_dict[alphabet][i] = df[i].eq(alphabet).astype(int).sum()


def update_dataframe(df):
    for i in range(5):
        letter = guess[i]
        colour = feedback[i]
        if colour == 'g':
            df = df[df[i] == letter]
        elif colour == 'y':
            df = df[df[i] != letter]
            df = df[(df.iloc[:, 0:] == letter).any(axis=1)]
        elif colour == 'w':
            df = df[(df.iloc[:, 0:] != letter).all(axis=1)]
    return df


def best_word(guess, feedback) -> str:
    calculate_frequency()

    score_dict = {}
    max_freq = [0, 0, 0, 0, 0]

    for letter in alphabet_dict:
        for i in range(5):
            if max_freq[i] < alphabet_dict[letter][i]:
                max_freq[i] = alphabet_dict[letter][i]

    for ind in df.index:
        word = ''
        score = 1
        for i in range(5):
            letter = df[i][ind]
            score *= + (alphabet_dict[letter][i] - max_freq[i]) ** 2
            word += letter
        score_dict[word] = score

    best_word = ''
    best_score = 10**100
    for word in score_dict:
        if best_score > score_dict[word]:
            best_word = word
            best_score = score_dict[word]
    return best_word


for i in range(6):
    guess = input('Enter your guess: ')
    print('g - green, y - yellow, w - wrong/grey')
    feedback = input('Feedback: ')
    if feedback == 'ggggg':
        print(f'Congratulations! You got the word in {i + 1} guesse(s).')
        break
    else:
        df = update_dataframe(df)
        print(f'I suggest trying: {best_word(guess, feedback)}')

if feedback != 'ggggg':
    print('Sorry, end of your wordle streak.')
