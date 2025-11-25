from datetime import datetime, timedelta



'''
event_start_time = datetime.now()
timestamp_string = event_start_time.isoformat()

with open('game_save.txt', 'w') as f:
    f.write(timestamp_string)

'''


try:
    with open('game_save.txt', 'r') as f:
        saved_timestamp_string = f.read()
    
    # Convert the saved string back into a datetime object
    saved_time = datetime.fromisoformat(saved_timestamp_string)
    
except FileNotFoundError:
    # Handle case where the save file doesn't exist yet
    print("No saved time found.")
    saved_time = None



current_time = datetime.now()

if saved_time:
    # Calculate the difference, which is a timedelta object
    time_elapsed = current_time - saved_time 
    
    # You now have the elapsed time!
    # time_elapsed.total_seconds() gives the time in seconds
    print(f"Total time elapsed: {time_elapsed}")
    
    # Define your required duration (e.g., 5 minutes)
    REQUIRED_DURATION = timedelta(hours=.5)
    
    # Check if the required time has passed
    if time_elapsed >= REQUIRED_DURATION:
        print("✅ Success! 5 minutes have passed in real-world time.")
        # Apply rewards, complete crafting, etc.
    else:
        time_remaining = REQUIRED_DURATION - time_elapsed
        print(f"⏳ Still waiting. Time remaining: {time_remaining}")