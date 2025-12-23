import random
import pickle
import os

class Game:
    def __init__(self):
        self.guess_number = 1
        # grab word from list
        with open("./words.txt","r") as file:
            number_words = 0
            all_words = []
            for x in file:
                number_words += 1
                all_words.append(x)
            all_words = [i.rstrip() for i in all_words]
            word_index = random.randint(0, number_words - 1)
        self.word = all_words[word_index]

        # init word character checker
        self.word_dict = {}
        list_a = list(map(chr, range(97, 123)))
        for i in list_a:
            self.word_dict[i] = False

        for i in range(len(self.word)):
            self.word_dict[self.word[i]] = True

        # init history containers
        self.guess_history = []
        self.correct_history = []




    def guess_word(self):
        # Stays with user until a valid guess is passed.
        while True:
            guess = input(f"Guess {self.guess_number}:\n").lower()
            if len(guess) == 5 and guess.isalpha():
                self.guess_number += 1
                self.guess_history.append(guess)
                guess_array = ["_","_","_","_","_"]
                for i in range(5):
                    if self.word_dict[guess[i]]:
                        guess_array[i] = "0"
                    if guess[i] == self.word[i]:
                        guess_array[i] = "✓"
                print("".join(guess_array))
                self.correct_history.append("".join(guess_array))
                if guess == self.word:
                    return True
                else:
                    return False
            elif guess == "save_game":
                self.save_game()
                quit()
            elif len(guess) != 5:
                print("Guess does not contain 5 letters")
            elif not guess.isalpha():
                print("Guess contains a non-alphabetical character")


    def dump_history(self):
        print("\nWordle history:")
        for i, (guess_h, correct_h) in enumerate(zip(self.guess_history, self.correct_history)):
            print(f"Guess {i+1}:")
            print(guess_h)
            print(correct_h + "\n")

    def save_game(self):
        with open("saved_game.pkl", "wb") as file:
            pickle.dump(self, file, -1)

    def del_save(self):
        try:
            os.remove("./saved_game.pkl")
            print("Save deleted")
        except:
            pass
