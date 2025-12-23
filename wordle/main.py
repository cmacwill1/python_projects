from supplemental import *

def main():
    print("How to play:\nIt is wordle. otherwise type 'save_game' to save your game to come back to\nCharacter is in word, incorrect place: 0\nCharacter is in correct place: ✓\n")
    print("1: Load game from save")
    print("2: New game")
    while True:
        user_input = input()
        try:
            user_input = int(user_input)
            if user_input > 2:
                raise ValueError("Number not a valid selection")
            else:
                break
        except:
            print("please select valid option (integer)")

    if user_input == 1:
        try:
            with open("./saved_game.pkl", "rb") as file:
                wordle = pickle.load(file)
                wordle.dump_history()
            print("Game loaded")
        except:
            print("No file to restore! Creating new game.")
            wordle = Game()
            pass
    else:
        wordle = Game()
        wordle.del_save()

    for i in range(wordle.guess_number, 7):
        if wordle.guess_word():
            print("correct")
            wordle.del_save()
            break
        elif i == 6:
            print("\nToo many guesses!")
            print(f"correct word: {wordle.word}")
            wordle.del_save()
            break
    wordle.dump_history()

main()
