import streamlit as st
import json
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Haal de API-sleutel uit de Streamlit secrets

# Laad stellingen en prompt uit JSON-bestand
with open('config.json') as f:
    config = json.load(f)

stellingen = config["stellingen"]
custom_prompt = config["custom_prompt"]


def send_to_chatgpt(data, prompt):
    try:
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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
        return "Chatgpt communication failed"


def main():
    # Session state initialisatie
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'scores' not in st.session_state:
        st.session_state.scores = {}

    # Functie om de huidige stelling weer te geven
    def display_current_stelling(index):
        if index < len(stellingen):
            st.write(
                f"**Stelling {index + 1}:** {stellingen[index]['stelling']}")
            st.write(f"*{stellingen[index]['uitleg']}*")
            score = st.slider(f"Beoordeel stelling {index + 1}", 1, 9, 5)
            if st.button("Verzend antwoord"):
                st.session_state.scores[index] = score
                st.session_state.current_index += 1
        else:
            st.write("Alle stellingen zijn voltooid. Bedankt voor je deelname!")

            # Maak het JSON-bestand voor ChatGPT
            results_for_chatgpt = [
                {
                    "stelling": stellingen[i]["stelling"],
                    "uitleg": stellingen[i]["uitleg"],
                    "score": st.session_state.scores[i]
                }
                for i in range(len(stellingen))
            ]

            # Verstuur resultaten naar ChatGPT met een aangepaste prompt
            response_text = send_to_chatgpt(results_for_chatgpt, custom_prompt)
            st.write("Inzicht van ChatGPT:")
            st.write(response_text)

            # Sla de scores op als JSON bestand
            with open('results.json', 'w') as f:
                json.dump(results_for_chatgpt, f, indent=2)
            st.write("Hopelijk heb je hier wat aan.")

    # Weergeven van de huidige stelling
    display_current_stelling(st.session_state.current_index)


if __name__ == "__main__":
    main()
