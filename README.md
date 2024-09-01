## IELTS Assessment Using Speechsuper API

### Step 1: Obtaining Credentials

To use the Speechsuper API, you need an `appKey` and `secretKey`. Follow these steps to obtain them:

1. **Sign Up:**
   - Go to the [Speechsuper website](https://www.speechsuper.com/).
   - Register for an account if you don't already have one.

2. **Create an Application:**
   - After logging in, navigate to the API management section or dashboard.
   - Create a new application if one does not already exist. This will allow you to generate the necessary API keys.

3. **Obtain `appKey` and `secretKey`:**
   - Once your application is created, you should see your `appKey` and `secretKey` in the application details.
   - Keep these credentials secure as they are used to authenticate your API requests.

### Step 2: Setting Up Your Configuration

Create a `config.py` file in your project directory to store your credentials. This file should look like this:

```python
# config.py
appKey = "your_app_key_here"
secretKey = "your_secret_key_here"
```

Replace `"your_app_key_here"` and `"your_secret_key_here"` with the values you obtained from Speechsuper.

### Step 3: Running the SpeechSuper Code

To see how the API can be used, follow these steps:

1. **Read Through the `SpeechSuper.ipynb` Notebook:**
   - The notebook provides a detailed example of how to use the Speechsuper API for IELTS assessment, including audio format conversion and result extraction.

2. **Modify the Example Code:**
   - In the notebook, locate the section where the API is called. Change the following variables to match your test case:

   ```python
   q = "What are your hobbies?"  # Replace with your actual question
   audio = "converted_What are your hobbies.wav"  # Replace with your actual audio file path
   result = get_IELTS_assessment_report(input_audio=audio, question_ielts=q)
   ```

   Ensure that the `audio` variable points to a valid audio file path and the `q` variable contains the appropriate question text.

### Step 4: Speech Performance Analysis

After obtaining the `result.json` file from Step 3, follow these steps to analyze the speech performance:

1. **Process the Results:**

   Use the `run_notebook.py` script to process the `result.json` file. This script will:

   - **Read** the assessment results from `result.json`.
   - **Extract** performance data for each IELTS speaking category: Fluency, Grammar, Lexical Resource, and Pronunciation.
   - **Convert** the performance data into natural language summaries and save them to appropriate files.

2. **Generated Outputs:**

   The script will produce the following files:

   - **`Fluency_Input_data_to_prompt.txt`**: Contains natural language summaries of fluency performance.
   - **`Lexical_Input_data_to_prompt.txt`**: Contains natural language summaries of lexical resource performance.
   - **`Grammar_Input_data_to_prompt.txt`**: Contains natural language summaries of grammar performance.
   - **`Pronunciation_Input_data_to_prompt.json`**: Contains detailed JSON analysis of pronunciation performance.

### Step 5: Generating Tailor-Made Feedback and Recommendations

1. **Prepare System Prompts**: 
   - In OpenAI assistance, set the following system prompts:
     - `System_prompt_Fluency.txt`
     - `System_prompt_Grammar.txt`
     - `System_prompt_Lexical.txt`
     - `System_prompt_Pronunciation.txt`

2. **Match Performance Data**:
   - Load the performance data files into the corresponding OpenAI assistance:

   - Generate tailored feedback and recommendations based on the performance data and system prompts.

