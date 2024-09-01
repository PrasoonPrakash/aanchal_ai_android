INSTRUCTIONS = """You are a professional clinician who is experienced in medical scribing. Your task is to help the user understand a conversation between a doctor and a patient. Specifically, the user will show you a transcript of a dialogue between a doctor and a patient. Then, the user will ask a question based on the transcript. You must answer that question correctly and truthfully.

IMPORTANT INSTRUCTIONS:
1. Read the transcript carefully and identify the doctor and patient utterances.
2. Understand the question and search the transcript for the answer.
3. If the question has multiple choice options, select the correct option.
4. Answer the question truthfully.
5. Write down your step-by-step before you reach the final answer.
6. You must provide the final answer in the following format. Answer: <Your Answer>"""


feat2question = {
    'CAUSE_MENOPAUSE': {
        "question": "What was the cause of the patient reaching menopause?",
        "options": {
            "CHEMO-INDUCED": "The patient reached menopause as a result of chemotherapy treatment, which can sometimes lead to early menopause.",
            "HORMONAL TREATMENT": "The patient reached menopause due to hormonal treatment, which can induce menopause as a side effect.",
            "NATURAL": "The patient reached menopause naturally, which occurs typically around the age of 50 as part of the normal aging process.",
            "HYSTERECTOMY": "The patient reached menopause following a hysterectomy, a surgical procedure to remove the uterus which can lead to menopause if the ovaries are also removed.",
            "NR": "The cause of the patient reaching menopause is not recorded or not reported."
        },
        "default": "HORMONAL TREATMENT",
    },

    "PAST_SURGERY": {
        "question": "Has the patient undergone any surgeries in the past?",
        "options": {
            "YES": "Yes",
            "NO": "No",
            "NR": "Not Recorded",
        },
        "default": "NO"
    },

    'STERILISATION (B/L TUBAL LIGATION)': {
        "question": "Has the patient ever had a bilateral tubal ligation for permanent birth control?",
        "options": {
            "YES": "Yes",
            "NO": "No",
            "NR": "Not Recorded",
        },
        "default": "NO"
    },

    "NON-VEG_FREQUENCY": {
        "question": "How often does the patient consume non-vegetarian food?",
        "options": {
            "DAILY": "Occurs every day.",
            "FORTNIGHTLY": "Occurs every two weeks (14 days).",
            "HALF YEARLY": "Occurs every six months (twice a year).",
            "MONTHLY": "Occurs once a month.",
            "NR": "Not regular or not specified.",
            "QUARTERLY": "Occurs every three months (four times a year).",
            "THRICE WEEKLY": "Occurs three times a week.",
            "TWICE WEEKLY": "Occurs two times a week.",
            "WEEKLY": "Occurs once a week.",
            "YEARLY": "Occurs once a year.",
        },
        "default": "WEEKLY"
    },

    "EDUCATION": {
        "question": "What is the patient's level of education?",
        "options": {
            "GRADUATE": "Graduate level of education",
            "ILLITERATE": "No formal education, unable to read or write",
            "INTERMEDIATE": "Education between primary and secondary levels",
            "NR": "Not Reported or Not Recorded",
            "POST GRADUATE": "Education beyond the undergraduate level",
            "PRIMARY": "Primary school level education",
            "SECONDARY": "Secondary school level education",
            "SECONDARY SCHOOL": "Same as Secondary, referring specifically to school level",
        },
        "default": "ILLITERATE"
    },

    'PHYSICAL ACTIVITY_GRADE': {
        "question": "What is the patient's level of physical activity?",
        "options": {
            "MILD": "MILD - Engages in mild physical activities like walking or light exercise.",
            "MODERATE": "MODERATE - Engages in moderate physical activities like jogging or cycling.",
            "NIL": "NIL - No physical activity.",
            "NR": "NR - Activity level not recorded or not applicable.",
            "VIGROUS": "VIGROUS - Engages in vigorous physical activities like running or intense sports."
        },
        "default": "MODERATE"
    },

    'RESIDENCE': {
        "question": "Where does the patient live?",
        "options": {
            "URBAN": "URBAN - The patient resides in an urban area, typically characterized by a high population density and infrastructure.",
            "RURAL": "RURAL - The patient resides in a rural area, typically characterized by countryside or agricultural surroundings.",
            "NR": "NR - Residence type not recorded or not applicable.",
        },
        "default": "NR"
    },

    'SES': {
        "question": "What is the socio-economic status of the patient?",
        "options": {
            "Lower": "Lower - Typically indicates lower income and limited access to resources.",
            "Lower Middle": "Lower Middle - Indicates moderate income and some access to resources.",
            "Middle": "Middle - Represents average income and access to basic resources.",
            "Upper": "Upper - Indicates higher income and better access to resources.",
            "Upper Middle": "Upper Middle - Represents high income and significant access to resources."
        },
        "default": "Upper"
    },

    "WEIGHT (IN KGS)": {
        "question": "What is the weight of the patient in KGs?",
        "type": "measurement",
        "default": 65,
    },

    'HEIGHT (IN CMS)': {
        "question": "What is the height of the patient in CMs?",
        "type": "measurement",
        "default": 152,
    },

    'SBP': {
        "question": "What is the Systolic Blood Pressure of the patient in mmHg?",
        "type": "measurement",
        "default": 123,
    },

    'RBS': {
        "question": "What is the Random Blood Sugar of the patient in mg/dL?",
        "type": "measurement",
        "default": 101,
    },

    'WAIST_CMS': {
        "question": "What is the waist circumference of the patient in CMs?",
        "type": "measurement",
        "default": 88,
    },

    'WHR':{
        "question": "What is the waist to hip ratio of the patient?",
        "type": "measurement",
        "default": 0.9,
    }
}
