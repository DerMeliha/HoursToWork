import streamlit as st

# Function to calculate hours worked and required work hours
def calculate_time(data):
    try:
        # Parse input data (split into hour and minute pairs)
        time_entries = list(map(int, data.split()))
        if len(time_entries) % 2 != 0:
            return "Error: Please ensure every hour has a corresponding minute."

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
            extra_work = f"You have to work <span style='font-size: 36px; font-weight: bold;'>{diff_hours}:{diff_minutes:02d}</span> hours extra"
            extra_message = "<span style='color: blue;'>Oh no you gotta work overtime. :(</span>"
            heart_message = "<span style='color: blue;'>❤️</span>"
        elif difference > 0:
            extra_work = f"You have to work <span style='font-size: 36px; font-weight: bold;'>{diff_hours}:{diff_minutes:02d}</span> hours less"
            extra_message = "<span style='color: blue;'>Yay!!! Leave work early. ❤️</span>"
            heart_message = ""
        else:
            extra_work = "You have worked exactly the required hours."
            extra_message = ""
            heart_message = ""

        return total_hours, remaining_minutes, days_of_work, required_hours, extra_work, extra_message, heart_message
    except ValueError:
        return "Error: Invalid input format. Please enter hours and minutes as pairs."

# Streamlit App Layout
st.title("Work Hours Calculator")

# Large text for instructions using HTML styling
st.markdown(
    "<h2 style='font-size: 36px; font-weight: bold;'>Enter all the hours and minutes worked</h2>", 
    unsafe_allow_html=True
)

# Text area for user input (allow multiple lines for convenience)
user_input = st.text_area(
    "",
    placeholder="E.g., 08 20 05 20 09 55",
    height=100  # Adjust the height of the input box for better visibility
)

# Action when user clicks "SEND" button
if st.button("SEND"):
    if user_input.strip():  # Check if input is not empty
        total_hours, remaining_minutes, days_of_work, required_hours, extra_work, extra_message, heart_message = calculate_time(user_input.strip())
        
        # Display the results with numbers in larger font and smaller font for text
        st.markdown(f"<h3 style='font-size: 28px;'>Total hours worked: <span style='font-size: 32px; font-weight: bold;'>{total_hours}:{remaining_minutes:02d}</span></h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='font-size: 28px;'>Total days worked: <span style='font-size: 32px; font-weight: bold;'>{days_of_work}</span></h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='font-size: 28px;'>Required hours to work: <span style='font-size: 32px; font-weight: bold;'>{required_hours}:00</span></h3>", unsafe_allow_html=True)
        
        # If there is a difference, display two separate lines
        if extra_message:
            st.markdown(f"<h3 style='font-size: 24px;'>{extra_work}</h3>", unsafe_allow_html=True)  # Keep numbers big and bold
            st.markdown(f"<h3 style='font-size: 24px;'>{heart_message}{extra_message}</h3>", unsafe_allow_html=True)  # Smaller message with heart emoji
        else:
            # No extra work or overtime, just a single message
            st.markdown(f"<h3 style='font-size: 24px;'>{extra_work}</h3>", unsafe_allow_html=True)  # Keep numbers big and bold
    else:
        st.error("Please enter some data before pressing SEND.")
