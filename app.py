import openai
import streamlit as st

# Set up OpenAI API key
  # Ensure your secrets.toml has this key

openai.api_key = "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"

# Custom CSS to set colors

st.markdown(
    """
    <style>
    .stApp {
        background-color: #c4ae78; /* Cream color */
    }
    /* Sidebar styling */
    .css-1d391kg { /* This class might change in different Streamlit versions */
        background-color: #171515; /* Brown color */
        color: white; /* White text */
    }
    /* Change color of text in the sidebar */
    .css-1d391kg p, .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #c4ae78; /* Text color for headings and paragraphs */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("ChatGPT-like Bot")

# Initialize session state variables
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for previous chats
with st.sidebar:
    st.header("Previous Chats")
    if st.session_state.chat_history:
        for i, chat in enumerate(st.session_state.chat_history):
            st.write(f"Chat {i + 1}:")
            for message in chat:
                st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")
            st.write("---")  # Separator between chats
    else:
        st.write("No previous chats.")

    if st.button("Start New Chat"):
        st.session_state.messages = []
        st.session_state.chat_history.append(st.session_state.messages)

# Display current chat messages with icons
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.markdown(f"**👤 User:** {message['content']}")  # User icon
    else:
        st.markdown(f"**🤖 Assistant:** {message['content']}")  # Assistant icon

# Text input for user to send messages
prompt = st.text_input("What's up?", placeholder="Type your message here...")
if prompt:
    # Few-shot examples added before user input
    few_shot_prompt = """
    You are a helpful assistant. Answer the following questions based on the examples below:

    Q: What is Ananya's full name?
    A: Ananya Shashidhara Bangalore

    Q: How many members in the family
    A: Four members 

    Q: Whats the mother name
    A: LakshmiSuchetha

    Q: What's the father's name
    A:Shashi

    Q: Brother's name 
    A:Samart

    Now, answer this question:
    """

    # Combine the few-shot examples with the user input
    full_prompt = few_shot_prompt + prompt

    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user's message with icon
    st.markdown(f"**👤 User:** {prompt}")  # User icon

    # Call the OpenAI API to get a response with few-shot learning prompt
    response = openai.ChatCompletion.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": "system", "content": few_shot_prompt},  # Few-shot examples
            {"role": "user", "content": prompt}  # User's question
        ],
        max_tokens=150
    )

    # Extract and display assistant's response
    assistant_response = response['choices'][0]['message']['content']
    st.markdown(f"**🤖 Assistant:** {assistant_response}")  # Assistant icon

    # Store assistant's response
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
