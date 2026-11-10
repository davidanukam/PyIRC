import random
import sys

# Clear screen and move cursor home
print("\033[2J\033[H", end="")

messages = [
    "Hello, World!!!",
    "who r u?",
    "bobby?",
    "can I have my badge?",
    "its been great talking to you",
]

# Set scrolling region from line 1 to 23
print("\033[1;23r", end="")


def send(message: str):
    # Save cursor position
    print("\x1b7", end="")

    # Jump to the bottom of the scroll region (Line 23, Column 1)
    print("\033[23;1H", end="")

    # Print the message inside the scrolling region
    print(f"\n<< {message}", end="")

    # Restore cursor position
    print("\x1b8", end="")


try:
    while True:
        message = random.choice(messages)

        send(message)

        # Move cursor to Line 24, clear the line, and flush output
        print("\033[24;1H\033[K", end="")
        sys.stdout.flush()

        # Get user input at the bottom
        next_text = input(">> ")
        send(next_text)

except KeyboardInterrupt:
    # Reset scrolling region to full screen upon exit before quitting
    # print("\033[r\033[2J\033[H", end="")
    print("Goodbye!")
