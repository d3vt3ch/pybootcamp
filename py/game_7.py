# we try to recreate the execise
import random

lives = 6
word_list = ["banana", "apple", "grape", "orange", "strawberry"]

stages = [  # final state: head, torso, both arms, and both legs
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # head, torso, both arms, and one leg
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                # head, torso, and both arms
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                # head, torso, and one arm
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                # head and torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                # head only
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                # initial empty state
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    ]


# Choose a random word from the list
chosen_word = random.choice(word_list)
print(chosen_word)


# different way to create a placeholder using list comprehension

placeholder = '_' * len(chosen_word)
print(placeholder)

game_over = False
correct = []

while not game_over:
    guess = input("Guess a letter: ").lower()
    
    

    display = ''

    for letter in chosen_word:
        if letter == guess:
            display += guess
            correct.append(guess)
        

        elif letter in correct:
            display += letter
            

        else:
            display += '_'

    if guess not in chosen_word:
        lives -= 1
        

    print(stages[lives])
    print(f"Your have {lives} lives left.")
    if lives == 0:
            game_over = True
            print("You lose!")
    print(display)
    
    

    
    if "_" not in display:
        game_over = True
        print("You win!")

    # if display == chosen_word:
    #     game_over = True
    #     print("You win!")  
    
