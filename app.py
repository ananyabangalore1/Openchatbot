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
    .css-1d391kg {
        background-color: #171515; /* Brown color */
        color: white;
    }
    .css-1d391kg p, .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #c4ae78;
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

    # Button to start a new chat
    if st.button("Start New Chat"):
        if st.session_state.messages:
            # Append the current conversation to chat history
            st.session_state.chat_history.append(st.session_state.messages.copy())
        # Reset messages for a new conversation
        st.session_state.messages = []

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

    Q: How many members are in the family?
    A: Four members

    Q: What's the mother's name?
    A: LakshmiSuchetha

    Q: What's the father's name?
    A: Shashi

    Q: Brother's name?
    A: Samart

    Now, answer this question:
    """

    # Combine the few-shot examples with the user input
    full_prompt = few_shot_prompt + "\n" + prompt

    # Store user message in session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user's message with an icon
    st.markdown(f"**👤 User:** {prompt}")

    try:
        # Call the OpenAI API to get a response with few-shot learning prompt
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "system", "content": few_shot_prompt},  # Few-shot examples
                {"role": "user", "content": prompt}  # User's question
            ],
            max_tokens=150
        )

        # Extract assistant's response
        assistant_response = response['choices'][0]['message']['content']

        # Display assistant's response with an icon
        st.markdown(f"**🤖 Assistant:** {assistant_response}")

        # Store assistant's response in session state
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Button to clear chat history
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.session_state.messages = []

