# we try to recreate the execise
import random

word_list = ["banana", "apple", "grape", "orange", "strawberry"]

# Choose a random word from the list
chosen_word = random.choice(word_list)
print(chosen_word)


# different way to create a placeholder using list comprehension

placeholder = '_' * len(chosen_word)
print(placeholder)

# different way to create a placeholder using a for loop

placeholder2 = ''
for i in chosen_word:
    placeholder2 += '_'
print(placeholder2) 

# Ask user to guess a letter and make it lowercase
guess = input("Guess a letter: ").lower()
print(guess+"\n")

# Check if the guessed letter is in the chosen word print "Correct!" if it is and "Wrong!" if it isn't for each letter in the chosen word
for letter in (chosen_word):
    if letter == guess:
        print(letter)
    else:
        print('_')

print("\n")

display = ''
for letter in chosen_word:
    if letter == guess:
        display += guess
    else:
        display += '_'

print(display)  
