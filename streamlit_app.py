import streamlit as st
import json
import openai

# Haal de API-sleutel uit de Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Laad stellingen en prompt uit JSON-bestand
with open('config.json') as f:
    config = json.load(f)

stellingen = config["stellingen"]
custom_prompt = config["custom_prompt"]

def send_to_chatgpt(data, prompt):
    response = openai.Completion.create(
        model="gpt-4",
        prompt=f"{prompt}\n\nHier zijn de resultaten van de persoonlijkheidsquiz:\n{json.dumps(data, indent=2)}\n\nKun je een inzicht geven in deze resultaten?",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def main():
    # Session state initialisatie
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'scores' not in st.session_state:
        st.session_state.scores = {}

    # Functie om de huidige stelling weer te geven
    def display_current_stelling(index):
        if index < len(stellingen):
            st.write(f"**Stelling {index + 1}:** {stellingen[index]['stelling']}")
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
            st.write("De resultaten zijn opgeslagen en verzonden naar ChatGPT.")

    # Weergeven van de huidige stelling
    display_current_stelling(st.session_state.current_index)

if __name__ == "__main__":
    main()
