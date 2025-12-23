from supplemental import *
import os

def main():
    print("How to play: It is wordle. otherwise type 'saved_game' to save your game to come back to\nCharacter is in word, incorrect place: 0\nCharater is in correct place: ✓")
    try:
        with open("./saved_game.pkl", "rb") as file:
            wordle = pickle.load(file)
            wordle.dump_history()
            print("game loaded")
    except:
        wordle = Game()

    for i in range(wordle.guess_number, 7):
        if wordle.guess_word():
            print("correct")
            try:
                os.remove("./saved_game.pkl")
            except:
                pass
            break
        elif i == 6:
            print("\nToo many guesses!")
            print(f"correct word: {wordle.word}")
            break
    wordle.dump_history()

main()
