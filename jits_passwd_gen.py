#Password Generator Project
import random
lettersu = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]
lettersl = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


greeting = "Thank you for using Jit's passwd generator🎲"
passlist = [lettersu, lettersl, numbers, symbols]
passwd = []
final_passwd = ""

print("Welcome to the Py Password Generator!  \n This password generator is running in two modes.\n")

while True:
    mode = input("Press 1 for auto mode: \n Press 2 for custom mode:")
    if mode == "1":
        digits = int(input("How many digits would you like? \n"))
        for char in range(digits):
            passwd.append(random.choice(random.choice(passlist)))

        for x in passwd:
            final_passwd += x
        print(f"Your final password is: {final_passwd}")
        print(greeting)
        break
   
    elif mode == "2":
        nr_lettersu = int(
            input(
                f"How many upper case letters would you like in your password?\n"))
        nr_lettersl = int(
            input(
                f"How many lower case letters would you like in your password?\n"))
        nr_symbols = int(input(f"How many symbols would you like?\n"))
        nr_numbers = int(input(f"How many numbers would you like?\n"))

        for letetru in range(nr_lettersu):
            passwd.append(random.choice(lettersu))

        for letetrl in range(nr_lettersl):
            passwd.append(random.choice(lettersl))

        for number in range(nr_numbers):
            passwd.append(random.choice(numbers))

        for symbol in range(nr_symbols):
            passwd.append(random.choice(symbols))

        random.shuffle(passwd)

        for x in passwd:
            final_passwd += x
        print(f"Your final password is: {final_passwd}")
        print(greeting)
        break
    
    elif mode == "q":
        print("***Good Bye***")
        break
    else:
        print("Your selection is invalid***. Please select correct input,")
