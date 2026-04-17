# we try to recreate the execise
import random

word_list = ["banana", "apple", "grape", "orange", "strawberry"]

# Choose a random word from the list
chosen_word = random.choice(word_list)
print(chosen_word)

# Ask user to guess a letter and make it lowercase
guess = input("Guess a letter: ").lower()

# Check if the guessed letter is in the chosen word print "Correct!" if it is and "Wrong!" if it isn't for each letter in the chosen word
for letter in chosen_word:
    if letter == guess:
        print("Correct!")
    else:
        print("Wrong!")