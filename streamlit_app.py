import streamlit as st
import json
from openai import OpenAI

# Ask the user to enter their own API key
api_key = st.text_input("Enter your OpenAI API key:", type="password")

# Check if debug mode is enabled
debug = False
if "debug" in st.secrets["general"]:
    debug = st.secrets["general"]["debug"]

if api_key:
    client = OpenAI(api_key=api_key)

    # Load statements and prompt from JSON file
    with open('config.json') as f:
        config = json.load(f)

    statements = config["statements"]
    custom_prompt = config["custom_prompt"]
    choices = config["choices"]
    default_choice = config["default_choice"]

    def send_to_chatgpt(data, prompt):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": data
                    }
                ],
                temperature=0.8,
                max_tokens=64,
                top_p=1
            )
            return response.choices[0].text.strip()
        except Exception as e:
            st.error(f"Error occurred: {e}")
            return "ChatGPT communication failed"

    def main():
        # Session state initialization
        if 'current_index' not in st.session_state:
            st.session_state.current_index = 0
        if 'scores' not in st.session_state:
            st.session_state.scores = {}

        # Function to display the current statement
        def display_current_statement(index):
            if index < len(statements):
                st.write(
                    f"**Statement {index + 1} of {len(statements)}:** {statements[index]['statement']}")
                st.write(f"*{statements[index]['explanation']}*")
                score = st.select_slider(
                    f"Rate statement {index + 1}", options=choices, value=default_choice)
                if st.button("Submit answer"):
                    st.session_state.scores[index] = score
                    st.session_state.current_index += 1
            else:
                st.write("All statements are completed. Thank you for your participation!")

                # Create the JSON file for ChatGPT
                results_for_chatgpt = [
                    {
                        "statement": statements[i]["statement"],
                        "explanation": statements[i]["explanation"],
                        "score": st.session_state.scores[i]
                    }
                    for i in range(len(statements))
                ]

                # Send results to ChatGPT with a custom prompt
                response_text = send_to_chatgpt(results_for_chatgpt, custom_prompt)
                st.write("Insight from ChatGPT:")
                st.write(response_text)

                # Save scores only if debug mode is enabled
                if debug:
                    with open('results.json', 'w') as f:
                        json.dump(results_for_chatgpt, f, indent=2)

        # Display the current statement
        display_current_statement(st.session_state.current_index)

    if __name__ == "__main__":
        main()
else:
    st.warning("Please enter your OpenAI API key to continue.")
