# ------------------------------------ imports --------------------------- #
import math


# ------------------------------------ functions --------------------------- #

# this is our welcome message for the app
def welcome():
    welcome = "Welcome to the Right Triangle Solver App"
    return welcome


# user input for the first leg of the right triangle
def input_height():
    height = ""
    while height.replace(".", "").isnumeric() == False:
        height = input("What is the height of the triangle: ")
        if height.replace(".", "").isnumeric() == False:
            print()
            print("Input must only contain numeric values!")
            print()
    height = float(height)
    return height 


# user input for the second leg of the right triangle
def input_base():
    base = ""
    while base.replace(".", "").isnumeric() == False:
        base = input("What is the base of the triangle: ")
        if base.replace(".", "").isnumeric() == False:
            print()
            print("Input must only contain numeric values!")
            print()
    base = float(base)
    return base 


# this function will calculate hypotenuse
def calc_hypotenuse(height, base):
    hypotenuse = math.hypot(height, base)
    return hypotenuse


# this function will calculate area
def calc_area(height, base):
    area = (height*base)/2
    return area


# this is the output message of the program
def print_output(hypotenuse, area):
    hypotenuse = round(hypotenuse, 3)
    area = round(area, 3)

    hypotenuse_output = (
        f"For a triangle with height of 20 and base of 40.5 the hypotenuse"
        f" is {hypotenuse}"
    )
    area_output = (
        f"For a triangle with height of 20 and base of 40.5 the area"
        f" is {area}"
    )
    print(hypotenuse_output)
    print(area_output)


# ------------------------------------ main --------------------------------- #
# this the main app function
def main():
    
    # welcome message for our app
    print()
    print(welcome())
    print()

    # we'll ask the user to input height of the right triangle
    height = input_height()

    # we'll ask the user to input base of the right triangle
    base = input_base()

    # we'll calculate hypotenuse
    hypotenuse = calc_hypotenuse(height, base)

    # we'll calculate area
    area = calc_area(height, base)

    # final output
    print()
    print_output(hypotenuse, area)
    print()


# ------------------------------------ run program ---------------------------#
if __name__ == "__main__":
    main()
