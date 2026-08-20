# Ask the user for their name
name = input('What\'s your "name"?')
# Remove whitespace from the str
name = name.strip()
# Capitalize the first letter of each word
name = name.title()
# name = input("What's your name? ").strip().title()

first, last = name.split(" ")

# print hello, end without a newline
print("hello, " + name, end=". ")

david = "David"
print("hello, ", name, ", ", david)
print(f"hello, {name}, {david}")

x = 1
y = 2

z = x + y

print(z)  # 3

x = input("What's x? ")
y = input("What's y? ")

z = x + y

print(z)  # 12 if x=1 and y=2, because input() returns str

z = int(x) + int(y)

print(z)  # 3 if x=1 and y=2, because we convert str to int
