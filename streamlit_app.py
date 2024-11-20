import streamlit as st

# Function to calculate hours
def calculate_time(data):
    try:
        # Parse input
        time_entries = list(map(int, data.split()))
        if len(time_entries) % 2 != 0:
            return "Error: Please ensure every hour has a corresponding minute."

        hours = time_entries[::2]
        minutes = time_entries[1::2]
        total_hours = sum(hours)
        total_minutes = sum(minutes)
        additional_hours, remaining_minutes = divmod(total_minutes, 60)
        total_hours += additional_hours
        days_of_work = len(hours)
        required_hours = days_of_work * 8

        worked_total_minutes = total_hours * 60 + remaining_minutes
        required_total_minutes = required_hours * 60
        difference = worked_total_minutes - required_total_minutes
        diff_hours, diff_minutes = divmod(abs(difference), 60)

        if difference < 0:
            extra_work = f"You have to work {diff_hours}:{diff_minutes:02d} hours extra/work overtime."
        elif difference > 0:
            extra_work = f"You have to work {diff_hours}:{diff_minutes:02d} hours less/leave work early."
        else:
            extra_work = "You have worked exactly the required hours."

        return total_hours, remaining_minutes, days_of_work, required_hours, extra_work
    except ValueError:
        return "Error: Invalid input format. Please enter hours and minutes as pairs."

# Streamlit App Layout
st.title("Work Hours Calculator")

# Increase font size using HTML for the instruction
st.markdown(
    "<h2 style='font-size: 36px;'>Enter all the hours and minutes worked</h2>", 
    unsafe_allow_html=True
)

st.write(
    "For example: `08 20 05 20 09 55`."
)

# Input field with a blank space above it
user_input = st.text_area(
    "",
    placeholder="E.g., 08 20 05 20 09 55",
    height=100  # Adjust the height of the input box
)

# Add a "SEND" button at the end
if st.button("SEND"):
    if user_input.strip():
        total_hours, remaining_minutes, days_of_work, required_hours, extra_work = calculate_time(user_input.strip())
        
        # Display each result on a separate line with a larger font size
        st.markdown(f"<h3 style='font-size: 36px;'>You have worked for {total_hours}:{remaining_minutes:02d} hours.</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='font-size: 36px;'>There have been {days_of_work} days of work.</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='font-size: 36px;'>You had to work for {required_hours}:00 hours.</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='font-size: 36px;'>{extra_work}</h3>", unsafe_allow_html=True)
    else:
        st.error("Please enter some data before pressing SEND.")
