import json

# Function to extract details of each word including pauses and pronunciation levels
def extract_word_details(data):
    performance_data = {
        "fluency_coherence": data["result"]["fluency_coherence"],
        "transcription": data["result"]["transcription"],
        "pause_cnt": data["result"]["fluency_stats"]["pause_cnt"],
        "relevance": data["result"]["relevance"],  # Added relevance as it relates to coherence
        "effective_speech_length": data["result"]["effective_speech_length"],  # Effective speech length
        "speed": data["result"]["speed"],  # Speaking speed in words per minute
        "pause_filler": data["result"].get("pause_filler", {}),  # Pause fillers if present
        "grammar_stats": {  # Extracting grammatical accuracy details
            "grammar_error_cnt": data["result"]["grammar_stats"].get("grammar_error_cnt", 0),
            "accurate_sent_pct": data["result"]["grammar_stats"].get("accurate_sent_pct", 0)
        }
    }
    
    # Extracting word-level details, mainly pauses which affect fluency
    sentences = data["result"]["sentences"]
    word_details = []
    for sentence in sentences:
        for detail in sentence["details"]:
            word = detail["word"]
            pronunciation = detail["pronunciation"]
            if detail["pause"]["type"] == 1:
                pause_duration = detail["pause"]["duration"]
                word_details.append(f"{word} ({pronunciation},{pause_duration})")
            else:
                word_details.append(f"{word} ({pronunciation})")

    performance_data["word_details"] = word_details
    return performance_data

def combine_text_files(file_list, output_file):
    combined_content = ""

    # Iterate over the list of files and read their content
    for file_name in file_list:
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()
            combined_content += content + "\n\n"

    # Write the combined content to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(combined_content)

def convert_to_natural_language_fluency(performance_data):
    # Fluency and Coherence
    fluency_coherence_score = performance_data.get("fluency_coherence", 0)
    pause_count = performance_data.get('pause_cnt', 0)
    fluency_coherence = {
        "Score": f"The student's fluency and coherence score is {fluency_coherence_score} out of 9.",
        "Pauses": f"The student paused {pause_count} times during the speech.",
    }

    # Relevance
    relevance = performance_data.get("relevance", "")
    relevance_description = f"The relevance of the content is noted as: {relevance}."

    # Effective Speech Length
    effective_speech_length = performance_data.get("effective_speech_length", 0)
    effective_speech_length_description = f"The effective speech length is {effective_speech_length} words."

    # Speed
    speed = performance_data.get("speed", 0)
    speed_description = f"The speaking speed is {speed} words per minute."

    # Pause Fillers
    pause_filler = performance_data.get("pause_filler", {})
    if pause_filler:
        pause_filler_description = f"Pause fillers used include: {', '.join(pause_filler.keys())}."
    else:
        pause_filler_description = "No specific pause fillers were noted."

    # Grammatical Accuracy
    grammar_stats = performance_data.get("grammar_stats", {})
    grammar_errors = grammar_stats.get("grammar_error_cnt", 0)
    accurate_sentences_percentage = grammar_stats.get("accurate_sent_pct", 0)
    grammatical_accuracy = {
        "Errors": f"There are {grammar_errors} grammar errors in the speech, with {accurate_sentences_percentage}% of sentences being accurate."
    }

    # Transcription
    transcription = performance_data.get("transcription", "")
    transcript = transcription

    # Word Details
    word_details = performance_data.get("word_details", [])
    word_details_summary = " ".join(word_details)
    word_details_formatted = {
        "WordDetails": word_details_summary
    }

    # Combine all parts into a single JSON object
    output = {
        "New Uner Input Data": {
            "Fluency and Coherence": fluency_coherence,
            "Relevance": relevance_description,
            "Effective Speech Length": effective_speech_length_description,
            "Speed": speed_description,
            "Pause Fillers": pause_filler_description,
            "Grammatical Accuracy": grammatical_accuracy,
            "Transcript": transcript,
            "Word Details (pronunciation scores, pause durations if exist)": word_details_formatted
        }
    }
    # Write the JSON object to a file (optional)
    with open('Fluency_Input_data_to_prompt.json', 'w') as file:
        json.dump(output, file, indent=4)
    return 0 

def extract_lexical_performance_data(data):
    # Extracting required data
    result = data["result"]
    
    # Initialize lexical performance data dictionary
    lexical_performance_data = {
        "lexical_resource": result["lexical_resource"],
        "word_cnt": result["vocabulary_stats"]["word_cnt"],
        "unique_word_cnt": result["vocabulary_stats"]["unique_word_cnt"],
        "academic_words": result["vocabulary_stats"]["academic_words"],
        "CEFR_A1_pct": result["vocabulary_stats"]["CEFR_A1_pct"],
        "CEFR_A2_pct": result["vocabulary_stats"]["CEFR_A2_pct"],
        "CEFR_B1_pct": result["vocabulary_stats"]["CEFR_B1_pct"],
        "CEFR_B2_pct": result["vocabulary_stats"]["CEFR_B2_pct"],
        "CEFR_C1_pct": result["vocabulary_stats"]["CEFR_C1_pct"],
        "CEFR_C2_pct": result["vocabulary_stats"]["CEFR_C2_pct"],
        "transcription": result["transcription"]
    }
    
    # Check if question prompt is present in the input data
    if "question_prompt" in data["params"]["request"]:
        lexical_performance_data["question_prompt"] = data["params"]["request"]["question_prompt"]
    
    return lexical_performance_data

def convert_to_natural_language_lexical(performance_data):
    # Lexical Resource Score
    lexical_score = performance_data["lexical_resource"]
    lexical_scr = f"The student's lexical score is {lexical_score} out of 9."

    # Word Count
    word_count = performance_data["word_cnt"]
    word_cnt = f"The total word count in the text is {word_count}."

    # Unique Word Count
    unique_word_count = performance_data["unique_word_cnt"]
    unique_word_cnt = f"The number of unique words used is {unique_word_count}."

    # Academic Words
    academic_words = performance_data["academic_words"]
    academic_words_list = ", ".join(academic_words)
    academic_words_summary = f"The academic words used in the text are: {academic_words_list}."

    # CEFR Levels
    CEFR_A1_pct = performance_data["CEFR_A1_pct"]
    CEFR_A2_pct = performance_data["CEFR_A2_pct"]
    CEFR_B1_pct = performance_data["CEFR_B1_pct"]
    CEFR_B2_pct = performance_data["CEFR_B2_pct"]
    CEFR_C1_pct = performance_data["CEFR_C1_pct"]
    CEFR_C2_pct = performance_data["CEFR_C2_pct"]

    CEFR_summary = (
        f"The distribution of words across CEFR levels is as follows: "
        f"{CEFR_A1_pct}% at A1, {CEFR_A2_pct}% at A2, {CEFR_B1_pct}% at B1, "
        f"{CEFR_B2_pct}% at B2, {CEFR_C1_pct}% at C1, and {CEFR_C2_pct}% at C2."
    )

    # Transcription
    transcription = performance_data["transcription"]
    transcription_summary = f"The provided transcription is: {transcription}"

    # Initialize the summary dictionary
    lexical_performance_summary = {
        "New User Input Data": {
            "Lexical Score": lexical_scr,
            "Word Count": word_cnt,
            "Unique Word Count": unique_word_cnt,
            "Academic Words": academic_words_summary,
            "CEFR Levels": CEFR_summary,
            "Transcription": transcription_summary
        }
    }

    # Include the question prompt if available
    if "question_prompt" in performance_data:
        question_prompt = performance_data["question_prompt"]
        question_prompt_summary = f"The question prompt given was: {question_prompt}"
        lexical_performance_summary["New User Input Data"]["Question Prompt"] = question_prompt_summary

    # Write summaries to a JSON file
    with open('Lexical_Input_data_to_prompt.json', 'w') as file:
        json.dump(lexical_performance_summary, file, indent=4)

    return 0

def extract_grammar_data(data):
    # Extract transcription and sentences
    transcription = data["result"]["transcription"]
    sentences = [sentence["sentence"] for sentence in data["result"]["sentences"]]

    # Extract grammatical accuracy parameters
    grammar_error_count = data["result"]["grammar_stats"]["grammar_error_cnt"]
    accurate_sentence_pct = data["result"]["grammar_stats"]["accurate_sent_pct"]
    corrected_sentences = [sentence.get("grammar", {}).get("corrected", "") for sentence in data["result"]["sentences"]]
    grammar_operations = [sentence.get("grammar", {}).get("operations", []) for sentence in data["result"]["sentences"]]

    # Compile extracted parameters into a dictionary
    grammar_performance_data = {
        "transcription": transcription,
        "sentences": sentences,
        "grammar_error_count": grammar_error_count,  # Number of grammar errors
        "accurate_sentence_pct": accurate_sentence_pct,  # Percentage of accurate sentences
        "corrected_sentences": corrected_sentences,  # Corrected sentences
        "grammar_operations": grammar_operations  # Specific grammatical corrections
    }

    return grammar_performance_data

def convert_to_natural_language(grammar_performance_data):
    # Generate natural language feedback
    transcription = grammar_performance_data["transcription"]
    sentences = grammar_performance_data["sentences"]
    grammar_error_count = grammar_performance_data["grammar_error_count"]
    accurate_sentence_pct = grammar_performance_data["accurate_sentence_pct"]
    corrected_sentences = grammar_performance_data["corrected_sentences"]
    grammar_operations = grammar_performance_data["grammar_operations"]

    # Feedback for Grammatical Accuracy
    grammatical_accuracy = (
        f"The student's speech contains {grammar_error_count} grammatical errors, "
        f"with {accurate_sentence_pct}% of sentences being accurate.\n"
        "Here are some sentences with suggested corrections:\n"
    )

    problematic_sentences = ""

    for i, sentence in enumerate(sentences):
        original_sentence = sentence
        corrected_sentence = corrected_sentences[i]
        operations = grammar_operations[i]

        if corrected_sentence and operations:
            for operation in operations:
                if operation["type"] == "delete":
                    problematic_sentences += (
                        f"- Original: '{original_sentence}'\n"
                        f"  Correction: '{corrected_sentence}'\n"
                        "  Suggestion: Remove unnecessary words to improve clarity.\n\n"
                    )
                elif operation["type"] == "replace":
                    problematic_sentences += (
                        f"- Original: '{original_sentence}'\n"
                        f"  Correction: '{corrected_sentence}'\n" # When this JSON data is parsed and displayed in a viewer that supports newline characters, the text will appear on separate lines as intended.
                        "  Suggestion: Replace incorrect words to ensure proper grammar usage.\n\n"
                    )

    # Structure the output JSON data
    output_data = {
        "New User Input Data": {
            "Transcript": transcription,
            "Grammatical Accuracy": {
                "Errors": grammatical_accuracy.strip()
            },
            "Problematic Sentences": problematic_sentences.strip()
        }
    }

    # Write the feedback to a JSON file
    with open('Grammar_Input_data_to_prompt.json', 'w') as file:
        json.dump(output_data, file, indent=4)


    return 0

def extract_pronunciation_data(data):
    pronunciation_data = {
        "overall_pronunciation": data["result"]["pronunciation"],
        "pronunciation_stats": data["result"]["pronunciation_stats"],
        "sentence_details": [],
        "liaison": data["result"].get("liaison", []),  # Linking or liaison details
        "plosion": data["result"].get("plosion", [])   # Loss of plosion details
    }
    
    # Extracting word-level pronunciation details
 # Extracting word-level details, mainly pauses which affect fluency
    sentences = data["result"]["sentences"]
    word_details = []
    for sentence in sentences:
        for detail in sentence["details"]:
            word = detail["word"]
            pronunciation = detail["pronunciation"]
            if detail["pause"]["type"] == 1:
                pause_duration = detail["pause"]["duration"]
                word_details.append(f"{word} ({pronunciation},{pause_duration})")
            else:
                word_details.append(f"{word} ({pronunciation})")

    pronunciation_data["word_details"] = word_details
    return pronunciation_data

def convert_to_natural_language_and_write_to_json(pronunciation_data):
    overall_pronunciation = pronunciation_data["overall_pronunciation"]
    pronunciation_stats = pronunciation_data["pronunciation_stats"]
    liaisons = pronunciation_data["liaison"]
    plosions = pronunciation_data["plosion"]
    
    # Creating a structured natural language summary
    structured_summary = {
        "New User Input Data": {
            "Overall Pronunciation Score": f"The student's overall pronunciation score is {overall_pronunciation} out of 9.",
            "Good Word Percentage": f"The percentage of words pronounced well is {pronunciation_stats['good_word_pct']}%.",
            "Fair Word Percentage": f"The percentage of words pronounced fairly is {pronunciation_stats['fair_word_pct']}%.",
            "Poor Word Percentage": f"The percentage of words pronounced poorly is {pronunciation_stats['poor_word_pct']}%.",
            # "Word-Level Pronunciation Details": "Word-level pronunciation scores and pause durations are as follows:",
            "Liaison Details": "Liaison details are as follows:",
            "Plosion Details": "Loss of plosion details are as follows:"
        }
    }
    
    # Word Details
    word_details = pronunciation_data.get("word_details", [])
    word_details_summary = " ".join(word_details)
    word_details_formatted = {
        "WordDetails": word_details_summary
    }
    structured_summary["New User Input Data"]["Word Details (pronunciation scores, pause durations (if exist))"] = word_details_formatted
    
    # Liaison Details
    liaison_details = []
    for liaison in liaisons:
        first_word = liaison["first"]["word"]
        second_word = liaison["second"]["word"]
        liaison_details.append(f"Between '{first_word}' and '{second_word}'")
    structured_summary["New User Input Data"]["Liaison Details"] = ", ".join(liaison_details) if liaison_details else "No liaisons detected."
    
    # Plosion Details
    plosion_details = []
    for plosion in plosions:
        first_word = plosion["first"]["word"]
        second_word = plosion["second"]["word"]
        plosion_details.append(f"Between '{first_word}' and '{second_word}'")
    structured_summary["New User Input Data"]["Plosion Details"] = ", ".join(plosion_details) if plosion_details else "No loss of plosion detected."
    
    # Write the summary to a JSON file
    with open('Pronunciation_Input_data_to_prompt.json', 'w') as file:
        json.dump(structured_summary, file, indent=4)




def main():
    with open('results_hobies.json', 'r') as file:
        data = json.load(file)

    # Extract word details and add to performance data
    Fluency_performance_data = extract_word_details(data)
    convert_to_natural_language_fluency(Fluency_performance_data) # write natural language data into performance_data.txt

    lexical_performance_data = extract_lexical_performance_data(data)
    convert_to_natural_language_lexical(lexical_performance_data)

    grammar_performance_data = extract_grammar_data(data)
    convert_to_natural_language(grammar_performance_data)

    pronunciation_data = extract_pronunciation_data(data)
    convert_to_natural_language_and_write_to_json(pronunciation_data)

if __name__ == "__main__":
    main()
