class PrincessGame:
    def __init__(self):
        self.game_logic()

    def clear_screen(self):
        import os
        # 'nt' means Windows, 'posix' means Max or Linux
        if (os.name == "posix"):
            os.system("clear")
        else:
            os.system("cls")

    def game_logic(self):
        self.clear_screen()
        print("Welcome to you own adventure!")
        print("The goal is to find your Python princess...")
        name = input("Enter your name: ")
        name = name.lower()
        self.clear_screen()
        print("You are standing in front of two doors...")
        print("Do you open the door on your left or right?")
        question = input().lower()
        if question == "left":
            self.clear_screen()
            print("You fell into a pit and died. GAME OVER.")
        elif question == "right":
            self.clear_screen()
            print(f"Congratulations {name.capitalize()}! You found the Python princess. YOU WIN!")
        else:
            self.clear_screen()
            print("Sorry I dont recognize this input. Please enter left or right. GAME OVER")


if __name__ == "__main__":
    pg = PrincessGame()

