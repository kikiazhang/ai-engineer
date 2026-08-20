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


# Get the user's input
x = float(input("What's x? "))
y = float(input("What's y? "))

# Calculate the result
z = x / y

# Print the result
print(f"{z:.2f}")
# Calculate the result and round, same result as above
# z = round(x / y, 2)
# Print the formatted result, eg: 1,000
# print(f"{z:,}")