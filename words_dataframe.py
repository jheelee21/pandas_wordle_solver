import pandas as pd

word_dict = {0: [], 1: [], 2: [], 3: [], 4: []}
listfile = open('valid_guesses.csv')
word = listfile.readline().strip()
while word != '':
    for i in range(5):
        word_dict[i].append(word[i])
    word = listfile.readline().strip()

df = pd.DataFrame(word_dict)

print(df)
