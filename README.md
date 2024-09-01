IELTS Assessment Using Speechsuper API
Step 1: Obtaining Credentials
To use the Speechsuper API, you need an appKey and secretKey. Follow these steps to obtain them:

Sign Up:

Go to the Speechsuper website.
Register for an account if you don't already have one.
Create an Application:

After logging in, navigate to the API management section or dashboard.
Create a new application if one does not already exist. This will allow you to generate the necessary API keys.
Obtain appKey and secretKey:

Once your application is created, you should see your appKey and secretKey in the application details.
Keep these credentials secure as they are used to authenticate your API requests.
Step 2: Setting Up Your Configuration
Create a config.py file in your project directory to store your credentials. This file should look like this:

python
Copy code
# config.py
appKey = "your_app_key_here"
secretKey = "your_secret_key_here"
Replace "your_app_key_here" and "your_secret_key_here" with the values you obtained from Speechsuper.

Step 3: Running the Sample Code
To see how the API can be used, follow these steps:

Read Through the sample_code.ipynb Notebook:

The notebook provides a detailed example of how to use the Speechsuper API for IELTS assessment, including audio format conversion and result extraction.
Modify the Example Code:

In the notebook, locate the section where the API is called. Change the following variables to match your test case:
python
Copy code
q = "What are your hobbies?"  # Replace with your actual question
audio = "converted_What are your hobbies.wav"  # Replace with your actual audio file path
result = get_IELTS_assessment_report(input_audio=audio, question_ielts=q)
Ensure that the audio variable points to a valid audio file path and the q variable contains the appropriate question text.
