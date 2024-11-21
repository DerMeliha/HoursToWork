import streamlit as st

# Function to validate and preprocess the input data
def preprocess_input(data):
    # Handle different formats
    try:
        # Remove colons if present and replace with space
        cleaned_data = data.replace(":", " ")
        
        # If the input is in `0800` format, add spaces between hours and minutes
        cleaned_data = " ".join(cleaned_data[i:i+2] for i in range(0, len(cleaned_data), 2)) if len(cleaned_data.split()) == 1 else cleaned_data
        
        # Split the cleaned input and convert to integers
        time_entries = list(map(int, cleaned_data.split()))
        
        # Ensure even entries are valid hours (0-24) and odd entries are valid minutes (0-59)
        for i, value in enumerate(time_entries):
            if i % 2 == 0 and not (0 <= value <= 24):  # Hours validation
                return None, "Wrong hour input. Please ensure hours are between 0 and 24."
            if i % 2 != 0 and not (0 <= value <= 59):  # Minutes validation
                return None, "Wrong minute input. Please ensure minutes are between 0 and 59."
        
        return time_entries, None
    except ValueError:
        return None, "Wrong input, try again."

# Function to calculate hours worked and required work hours
def calculate_time(time_entries):
    # Split hours and minutes from time entries
    hours = time_entries[::2]
    minutes = time_entries[1::2]

    # Calculate total hours and minutes worked
    total_hours = sum(hours)
    total_minutes = sum(minutes)
    additional_hours, remaining_minutes = divmod(total_minutes, 60)
    total_hours += additional_hours

    # Calculate days worked and required hours
    days_of_work = len(hours)
    required_hours = days_of_work * 8

    # Convert total worked time and required time to minutes
    worked_total_minutes = total_hours * 60 + remaining_minutes
    required_total_minutes = required_hours * 60
    difference = worked_total_minutes - required_total_minutes
    diff_hours, diff_minutes = divmod(abs(difference), 60)

    # Determine if extra work is needed or if there's overtime/early leave
    if difference < 0:
        extra_work = f"You have to work <span style='font-size: 36px; font-weight: bold; color: lightblue;'>{diff_hours}:{diff_minutes:02d}</span> hours extra"
        extra_message = "<span style='color: lightblue;'>Oh no you gotta work overtime... 🥹</span>"
    elif difference > 0:
        extra_work = f"You have to work <span style='font-size: 36px; font-weight: bold; color: lightblue;'>{diff_hours}:{diff_minutes:02d}</span> hours less"
        extra_message = "<span style='color: lightblue;'>Yay!!! Leave work early. 💜</span>"
    else:
        extra_work = "You have worked exactly the required hours."
        extra_message = ""

    return total_hours, remaining_minutes, days_of_work, required_hours, extra_work, extra_message

# Streamlit App Layout
st.title("Work Hours Calculator")

# Large text for instructions using HTML styling
st.markdown(
    "<h2 style='font-size: 36px; font-weight: bold;'>Enter all the hours and minutes worked</h2>", 
    unsafe_allow_html=True
)

# Multi-line placeholder for user input with increased height
user_input = st.text_area(
    "",
    placeholder="E.g.,\n08 20\n05 20\n09 55\nOR\n0800 0520\nOR\n08:00 05:20",  # Updated placeholder
    height=200  # Adjust height to show more lines in the input box
)

# Action when user clicks "SEND" button
if st.button("SEND"):
    if user_input.strip():  # Check if input is not empty
        # Preprocess input data
        preprocessed_data, error_message = preprocess_input(user_input.strip())
        
        if error_message:  # If there's an error, display it
            st.error(error_message)
        else:
            # Calculate time based on preprocessed data
            total_hours, remaining_minutes, days_of_work, required_hours, extra_work, extra_message = calculate_time(preprocessed_data)
            
            # Display the results with numbers in larger font and smaller font for text
            st.markdown(f"<h3 style='font-size: 24px;'>Total hours worked: <span style='font-size: 32px; font-weight: bold;'>{total_hours}:{remaining_minutes:02d}</span></h3>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='font-size: 24px;'>Total days worked: <span style='font-size: 32px; font-weight: bold;'>{days_of_work}</span></h3>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='font-size: 24px;'>Required hours to work: <span style='font-size: 32px; font-weight: bold;'>{required_hours}:00</span></h3>", unsafe_allow_html=True)
            
            # If there is a difference, display two separate lines
            if extra_message:
                st.markdown(f"<h3 style='font-size: 24px;'>{extra_work}</h3>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='font-size: 24px;'>{extra_message}</h3>", unsafe_allow_html=True)
            else:
                # No extra work or overtime, just a single message
                st.markdown(f"<h3 style='font-size: 24px;'>{extra_work}</h3>", unsafe_allow_html=True)
    else:
        st.error("Please enter some data before pressing SEND.")
