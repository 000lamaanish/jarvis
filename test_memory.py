
from app.database import (
    initialize_database,
    save_message,
    get_recent_messages
)

initialize_database()

save_message("user", "My name is Anish.")
save_message("assistant", "Hello, Anish!")

messages = get_recent_messages(10)

for message in messages:
    print(message)
