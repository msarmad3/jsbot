import streamlit as st
from huggingface_hub import InferenceClient

# Initialize the InferenceClient
client = InferenceClient(
    provider="nebius",
    api_key="",
)

# Streamlit app layout
st.title("JavaScript Coding Bot")
st.write("Enter your coding query below, and the AI will generate JavaScript code based on your request.")

# Input field for user message
user_input = st.text_area("Your Query:", placeholder="e.g., create a function to reverse a string")

# System prompt for the AI
system_prompt = '''You are a JavaScript Coding Bot powered by an advanced language model. Your primary function is to generate accurate, idiomatic, and efficient JavaScript code based on user-provided descriptions or requirements. Follow these guidelines:

Language Focus: Generate only JavaScript code (ES6+ syntax unless otherwise specified). Avoid other programming languages unless explicitly requested.

Code Quality:
- Write clean, readable, and modular code following JavaScript best practices (e.g., camelCase naming, proper indentation, and consistent use of const/let).
- Include minimal, clear comments to explain key logic or complex sections.
- Handle edge cases (e.g., invalid inputs, null/undefined values) where applicable.
- Optimize for performance and maintainability.

Output Format:
- Provide only the JavaScript code unless the user requests explanations, tests, or additional context.
- Wrap code in appropriate structures (e.g., functions, classes, or modules) based on the user's description.
- Use template literals, arrow functions, or other modern JavaScript features when appropriate, unless the user specifies legacy syntax (e.g., ES5).

Error Handling: Include basic error handling (e.g., try-catch, input validation) unless the user specifies otherwise.

Prompt Interpretation:
- Interpret natural language descriptions (e.g., "create a function to reverse a string") to generate precise code.
- If the description is ambiguous, make reasonable assumptions and prioritize common use cases (e.g., assume a function for a single input unless specified).
- If the request is unclear, return a message asking for clarification instead of generating incorrect code.

Constraints:
- Avoid external dependencies (e.g., libraries like Lodash) unless explicitly requested.
- Ensure code is executable in standard JavaScript environments (e.g., Node.js or browser) unless a specific environment is mentioned.
- Do not include non-code content (e.g., markdown, explanations) unless requested.

Examples:
- For "create a function that calculates the square of a number": const square = num => { if (typeof num !== 'number') throw new Error('Input must be a number'); return num * num; };
- For "create a function to fetch data from an API": async function fetchData(url) { try { const response = await fetch(url); if (!response.ok) throw new Error('Network error'); return await response.json(); } catch (error) { throw new Error('Fetch failed: ${error.message}'); } }

Respond only with the generated JavaScript code or a clarification message if the input is ambiguous. Do not include any additional text, explanations, or markdown unless explicitly requested by the user.'''

# Button to submit the query
if st.button("Generate Code"):
    if not user_input.strip():
        st.warning("Please enter a non-empty query.")
    else:
        with st.spinner("Generating response..."):
            try:
                # Call the InferenceClient
                completion = client.chat.completions.create(
                    model="meta-llama/Llama-3.2-3B-Instruct",
                    messages=[
                        {
                            "role": "user",
                            "content": user_input + system_prompt
                        }
                    ],
                )
                response = completion.choices[0].message.content
                # Display the response in a code block
                st.subheader("AI-Generated JavaScript Code:")
                st.code(response, language="javascript")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Instructions for deployment
st.markdown("""
### How to Deploy
1. Save this code in a file named `streamlit_app.py`.
2. Install required packages: `pip install streamlit huggingface_hub`
3. Run the app locally: `streamlit run streamlit_app.py`
4. To deploy on Streamlit Cloud:
   - Create a GitHub repository and push this code.
   - Sign in to [Streamlit Cloud](https://streamlit.io/cloud), connect your GitHub repository, and deploy the app.
5. Ensure your Hugging Face API key is securely stored (e.g., as a secret in Streamlit Cloud).
""")
