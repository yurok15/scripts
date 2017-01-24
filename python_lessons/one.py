#!/usr/bin/python3
'''http://www.practicepython.org/exercise/2014/01/29/01-character-input.html'''

from datetime import date


def year(age):
    return(date.today().year + (100 - age))


def main():
    name = input("Give your name\n")
    age = int(input("Give your age\n"))
    print_number = int(input("Give print number\n"))
    year100 = year(age)

    while print_number != 0:
        print("In " + str(year100) + " you will celebrate 100 years")
        print_number = print_number - 1


if __name__ == "__main__":
    main()
