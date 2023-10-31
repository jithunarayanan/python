import random
import hangman_words
import hangman_art

word = random.choice(hangman_words.word_list)
length = len(word)
end_of_game = False
lives = 6

print(hangman_art.logo)
display = []
for _ in range(length):
    display += "_"

while not end_of_game:
    guess = input("Guess a letter: ").lower()
    if guess in display:
        print(f"You've already guessed {guess}")
    for position in range(length):
        letter = word[position]
        if letter == guess:
            display[position] = letter
    if guess not in word:
        print(f"You guessed {guess}, that's not in the word. You lose a life.")
        lives -= 1
        if lives == 0:
            end_of_game = True
            print("You lose.")
            print(f"Selected word is {word}")

    print(f"{' '.join(display)}")

    if "_" not in display:
        end_of_game = True
        print("You win!!!👍")
    from hangman_art import stages
    print(stages[lives])
