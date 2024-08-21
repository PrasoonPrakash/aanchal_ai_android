INSTRUCTIONS = """You are a medical scribe and a language expert. Your task is to help the user understand a conversation between a doctor and a patient. Specifically, the user will show you a transcript of a dialogue between a doctor and a patient. Then, the user will ask a question based on the transcript. You must answer that question correctly and truthfully.

IMPORTANT INSTRUCTIONS:
1. Read the transcript carefully and identify the doctor and patient utterances.
2. Understand the question and search the transcript for the answer.
3. Answer the question truthfully. If the question is a multiple choice questions, select the answer from the given options.
4. Follow the answer format from the examples."""


feat2question = {
    "AGE": {
        "question": "What is the age of the patient in completed years?",
        "answer": "[Answer]\nThe age of the patient is  {} years."
    },
    "MARITAL STATUS": {
        "question": "What is the marital status of the patient?",
        "options": ["Single", "Married", "Divorced", "Widowed"],
        "answer": "[Answer]\nMarital status of the patient is {}."
    },
    "MARRIAGE_DURATION": {
        "question": "For how many years has the patient been married?",
        "answer": "[Answer]\n{} years."
    },
    "EDUCATION": {
        "question": "What is the educational level of the patient?",
        "options":[
            "Illiterate", "Primary", "Secondary School Completed",
            "Intermediate", "Graduate", "Post graduate"
        ],
        "answer": "[Answer]\nEducation level of the patient is {}."
    },
    "OCCUPATION": {
        "question": "What is the occupation of the patient?",
        "options": [
            "Professional", "Semi Professional", "Clerical/Shop Owner/ Farmer",
            "Skilled", "Semi-skilled", "Unskilled", "Student/Housewife", "Unemployed"
        ],
        "answer": "[Answer]\nOccupation of the patient is {}."
    },
    "FAMILY TYPE": {
        "question": "What is the family type of the patient?",
        "options": ["Joint", "Nuclear", "others"],
        "answer": "[Answer]\nFamily type of the patient is {}."
    },
    "RELIGION": {
        "question": "What is the religion of the patient?",
        "options": ["Hindu", "Muslim", "Sikh", "Christian", "others"],
        "answer": "[Answer]\nReligion of the patient is {}."
    },
    # Medical
    "MENSTRUAL_STATUS": {
        "question": "What is the menstrual status of the patient?",
        "options": ["PRE-MENOPAUSAL", "POST-MENOPAUSAL", "NONE"],
        "answer": "[Answer]\nMenstrual status of the patient is {}."
    },
    #"PAST_SURGERY": {
    #    "question": "What is the menstrual status of the patient?",
    #    "options": ["PRE-MENOPAUSAL", "POST-MENOPAUSAL", "NONE"],
     #   "answer": "[Answer]\nMenstrual status of the patient is {}."
    #},
    "TYPE OF MENOPAUSE(NATURAL/HYSTERECTOMY)": {
        "question": "Is the patient's menopause natural or induced (hormonal/hysterectomy/chemo-induced)?",
        "options": ["HORMONAL TREATMENT", "CHEMO-INDUCED", "HYSTERECTOMY", "NONE"],
        "answer": "[Answer]\nMenopause type of the patient is {}."
    },
    "PHYSICAL ACTIVITY": {
        "question": "Does the patient regularly engage in an physical activity?",
        "options": ["YES", "NO"],
        "answer": "[Answer]\n{}."
    },
    "ABORTION": {
        "question": "Has the patient experienced any pregnancies that ended in abortion?",
        "options": ["YES", "NO"],
        "answer": "[Answer]\n{}."
    },
    "ABORTION_NO.": {
        "question": "How many abortions has the patient had?",
        "answer": "[Answer]\nNumber of abortions: {}."
    },
    
}