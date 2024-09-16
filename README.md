# Passion Discovery App

This Streamlit-based app helps users explore their true passions by analyzing their responses to a set of personalized statements. The app integrates with OpenAI's GPT-3.5 to provide deep insights based on the user's answers.

## Features

- **Customizable Statements**: Users rate a series of statements related to their interests and motivations.
- **OpenAI Integration**: After all statements are rated, the app sends the results to GPT-3.5 for analysis, which provides personalized insights.
- **Streamlit Interface**: Simple, interactive UI built using Streamlit.
- **Debug Mode**: Option to save user results locally for debugging purposes.

## Requirements

- Python 3.7+
- Streamlit
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/DDecoene/selfquest.git
   cd selfquest
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your `secrets.toml` file for debug mode (optional):
   ```
   [general]
   debug = true  # Set to false to disable debug mode
   ```

4. Add your OpenAI API key. When running the app, you'll be prompted to enter it or you can hardcode it into the app for quicker access.

## Configuration

The app uses a `config.json` file to load customizable statements and choices. Here's an example `config.json` structure:

```
{
  "choices": [
    "Strongly agree",
    "Mostly agree",
    "Somewhat agree",
    "Neutral",
    "Somewhat disagree",
    "Mostly disagree",
    "Strongly disagree"
  ],
  "default_choice": "Neutral",
  "statements": [
    {
      "statement": "I enjoy working in a team where I can exchange ideas and collaborate on projects.",
      "explanation": "Teamwork can be motivating and stimulate new ideas."
    },
    {
      "statement": "I feel most fulfilled when I create something tangible, like art, crafts, or a physical product.",
      "explanation": "Some people find satisfaction in creating tangible products they can see and touch."
    }
  ],
  "custom_prompt": "You will now see a list of statements with an explanation and score. Analyze the information to determine the person's passion and what they truly enjoy. Give specific and actionable insights."
}
```

## Running the App

1. Start the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Enter your OpenAI API key when prompted.

3. Complete the series of statements by selecting your response for each one.

4. Once all statements are completed, the app will send the results to OpenAI for analysis. Insights will be displayed in the app.

## Debug Mode

If debug mode is enabled in the `secrets.toml` file, the app will save the user's responses and the text sent to ChatGPT in `results.json` after completion. **This text is saved only for debugging purposes and should not be used in production.** The file is useful for analysis or troubleshooting but should be handled with care to maintain user privacy.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributions

Feel free to submit pull requests or raise issues for improvements or bug fixes.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [OpenAI](https://openai.com/)
