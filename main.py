import random
import sys
import time
import threading

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

# Create a lock to prevent threads from clashing when writing to stdout
print_lock = threading.Lock()


def send(message: str, prefix: str = "<< "):
    with print_lock:
        # Save cursor position
        print("\x1b7", end="")

        # Jump to the bottom of the scroll region (Line 23, Column 1)
        print("\033[23;1H", end="")

        # Print the message inside the scrolling region
        print(f"\n{prefix}{message}", end="")

        # Restore cursor position (puts cursor back to Line 24 input prompt)
        print("\x1b8", end="")
        sys.stdout.flush()


def background_bot():
    """Background thread that sends random messages every few seconds."""
    while True:
        # Wait a random amount of time between messages (e.g., 3 to 6 seconds)
        time.sleep(random.randint(3, 6))
        message = random.choice(messages)
        send(message, prefix="<< ")


# Start the background bot thread (daemon=True means it exits when the main program exits)
bot_thread = threading.Thread(target=background_bot, daemon=True)
bot_thread.start()


def main():
    try:
        while True:
            # Move cursor to Line 24, clear the line, and flush output
            with print_lock:
                print("\033[24;1H\033[K", end="")
                sys.stdout.flush()

            # Get user input at the bottom (blocking, but background thread can still run!)
            next_text = input(">> ")

            if next_text.strip():
                # Echo user's message into the chat scroll region
                send(next_text, prefix="You: ")

    except KeyboardInterrupt:
        # Reset scrolling region to full screen upon exit before quitting
        # print("\033[r\033[2J\033[H", end="")
        print("\n>> Goodbye!")


if __name__ == "__main__":
    main()
