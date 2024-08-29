import streamlit as st
import requests
import os

hide menu = """
<style>
#Mainenu {
    visibility:hidden;
}
</style>
"""

# Get the API key from the environment variable
API_KEY = os.getenv('GEMINI_API_KEY')

# Set up the Streamlit app
st.title('Blog Writer')
st.write('Generate creative blog posts for your content!')
St.markdown(hide.menu,unsafe_allow_html=True)

# Custom CSS for button styling
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #1f3a93;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        transition-duration: 0.4s;
    }
    .stButton > button:hover {
        background-color: #3c6382;
        color: white;
    }
    .stButton > button:active {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Input fields
user_input = st.text_area('Enter your idea:', height=100)
intent_type = st.selectbox(
    'Select Blog Intent:',
    ['Informational', 'Commercial', 'Transactional', 'Navigational']
)

# Generate blog button and spinner
if st.button('Generate Blog'):
    if user_input:
        with st.spinner('Generating blog post...'):
            prompt = f"""As an expert copywriter specialized in blog writing, your task is to Create a creative post that is around 1000 words long for {user_input} with the intent {intent_type}.
            Please ensure the blog post is engaging, well-researched, and tailored to meet the specified intent. The content should be clear, concise, and provide value to the reader.
            The output should be Only The generated blog."""

            headers = {
                'Content-Type': 'application/json',
            }

            data = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }

            response = requests.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}',
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                try:
                    response_data = response.json()
                    candidates = response_data.get('candidates', [])

                    blogs_list = []
                    for candidate in candidates:
                        content = candidate.get('content', {}).get('parts', [{}])[0].get('text', '')
                        blogs_list.append(content)

                    # Display generated blog
                    blog_placeholder = st.empty()
                    blog_placeholder.markdown('\n\n'.join(blogs_list))

                except Exception as e:
                    st.error('Error parsing response. Please try again.')
            else:
                st.error(f'Error generating blog: {response.status_code} - {response.text}')
    else:
        st.warning('Please enter your idea.')
