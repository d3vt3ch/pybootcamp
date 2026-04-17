# Hangman Game with CRUD operations and category selection with scoreboard system

# we try to recreate the execise
import random

word_list = ["banana", "apple", "grape", "orange", "strawberry"]

word = random.choice(word_list)

print(word)

#count how many times each letter appears in the word
letter_count = {}
for letter in word:
    if letter in letter_count:
        letter_count[letter] += 1
    else:
        letter_count[letter] = 1

total_letters = len(letter_count)
print(total_letters)

#create a blank list with the same length as the word
blank_list = '_' * len(word)
print(blank_list)

for i in range(total_letters):
    answer = input("Guess a letter: ")

    if answer in letter_count:
        print("Correct!")
        #replace the blank with the letter
        blank_list = list(blank_list) # we need to convert the string to a list to be able to replace the blank with the letter
        for i in range(len(word)):
            if word[i] == answer:
                blank_list[i] = answer
        blank_list = ''.join(blank_list)
        print(blank_list)


