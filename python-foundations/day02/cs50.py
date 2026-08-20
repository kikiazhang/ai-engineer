def main():

    # Output using our own function
    name = input("What's your name? ").strip().title()
    hello(name)

    # Output without passing the expected arguments
    hello()


# Create our own function
def hello(to="world"):
    print("hello,", to)


main()