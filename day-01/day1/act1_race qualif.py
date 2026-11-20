

total_athletes = 0
qualified_count = 0
winner_name = ""
winner_time_str = ""
lowest_seconds = -1

while True:
    name = input("Enter athlete's name (x to end): ").strip()
    
    if name.lower() == "x":
        break
        
    time_str = input("Enter time (mm:ss): ").strip()
    
    # Validate format: must contain ':' and split into 2 parts
    parts = time_str.split(":")
    if len(parts) != 2:
        print("Invalid time format ignored.")
        continue
        
    min_part = parts[0]
    sec_part = parts[1]
    
    # Validate that both parts are positive digits
    if not (min_part.isdigit() and sec_part.isdigit()):
        print("Invalid numbers ignored.")
        continue
        
    minutes = int(min_part)
    seconds = int(sec_part)
    
    # Validate seconds are between 0 and 59
    if seconds < 0 or seconds > 59:
        print("Invalid seconds ignored.")
        continue
        
    # Valid entry confirmed
    total_seconds = minutes * 60 + seconds
    total_athletes += 1
    
    # Check qualifier (25:00 = 1500 seconds or less)
    if total_seconds <= 1500:
        qualified_count += 1
        
    # Check winner (strict '<' ensures first athlete wins on a tie)
    if lowest_seconds == -1 or total_seconds < lowest_seconds:
        lowest_seconds = total_seconds
        winner_name = name
        winner_time_str = f"{minutes}:{seconds:02d}"

# Display final output
print()
if total_athletes == 0:
    print("No valid athletes were entered.")
else:
    print(f"Winner: {winner_name} ({winner_time_str})")
    print(f"Qualified: {qualified_count} of {total_athletes}")

