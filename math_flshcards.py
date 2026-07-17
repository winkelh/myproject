from os import system
import random
# function to start the game and pick cards

# Start addition flashcard function
def add_flashcards() -> None:
    system("cls")
    card_one = random.randint(1, 10)
    card_two = random.randint(1, 10)
    correct = card_one + card_two
    answer = input(f"{card_one} + {card_two} = ")

    if int(answer) == correct:
        print(f"Correct! {card_one} + {card_two} = {answer}")
    else:
        print(f"Incorrect, {card_one} + {card_two} = {answer}")
    play_again = input("Would you like to play again? (a/s/m/d/n): ").lower()
    handle_input(key=play_again)
    # End addition flashcard function

# Start multiplication flashcard function
def multiply_flashcards() -> None:
    system("cls")
    card_one = random.randint(1, 10)
    card_two = random.randint(1, 10)
    correct = card_one * card_two
    answer = input(f"{card_one} * {card_two} = ")

    if int(answer) == correct:
        print(f"Correct! {card_one} * {card_two} = {answer}")
    else:
        print(f"Incorrect, {card_one} * {card_two} = {answer}")

    play_again = input("Would you like to play again? (a/s/m/d/n): ").lower()
    handle_input(key=play_again)
    # End multiplication flashcard function

# Start division flashcard function
def divide_flashcards() -> None:
    system("cls")
    card_one = random.randint(1, 10)
    card_two = random.randint(1, 10)
    correct = card_one / card_two
    answer = input(f"{card_one} / {card_two} = ")

    if float(answer) == correct:
        print(f"Correct! {card_one} / {card_two} = {answer}")
    else:
        print(f"Incorrect, {card_one} / {card_two} = {answer}")

    play_again = input("Would you like to play again? (a/s/m/d/n): ").lower()
    handle_input(key=play_again)
    # End division flashcard function

# Start subtraction flashcard function
def substraction_flashcards() -> None:
    system("cls")
    card_one = random.randint(1, 10)
    card_two = random.randint(1, 10)
    correct = card_one - card_two
    answer = input(f"{card_one} - {card_two} = ")

    if int(answer) == correct:
        print(f"Correct! {card_one} - {card_two} = {answer}")
    else:
        print(f"Incorrect, {card_one} - {card_two} = {answer}")

    play_again = input("Would you like to play again? (y/n/r): ").lower()
    handle_input(key=play_again)
    # End subtraction flashcard function

# Start Helper function to handle the followup input
def handle_input(*, key :str) -> None:
    play_again = input("Would you like to play again? (a/s/m/d/n): ").lower()
    if play_again == "a":
        add_flashcards()
    elif play_again == "s":
        substraction_flashcards()
    elif play_again == "m":
        multiply_flashcards()
    elif play_again == "d":
        divide_flashcards()
    elif play_again == "n":
        print("Thank you for playing. Goodbye!")
    else:
        print("Invalid choice. Please try again.")
        input("Hit enter to try again.")
        play_again = input("Would you like to play again? (a/s/m/d/n): ").lower()
        handle_input(key = play_again)
# End Helper function to handle the followup input


def start_game() -> None:
    system("cls")
    print("Welcome to Math Flashcards!")
    pick = input("Choose your flashcards (add|subtract|multiply|divide): ").lower()
    handle_input(key=pick)

start_game()

