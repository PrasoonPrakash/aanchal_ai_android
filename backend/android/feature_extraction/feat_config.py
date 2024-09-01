INSTRUCTIONS = """You are a professional clinician who is experienced in medical scribing. Your task is to help the user understand a conversation between a doctor and a patient. Specifically, the user will show you a transcript of a dialogue between a doctor and a patient. Then, the user will ask a question based on the transcript. You must answer that question correctly and truthfully.

IMPORTANT INSTRUCTIONS:
1. Read the transcript carefully and identify the doctor and patient utterances.
2. Understand the question and search the transcript for the answer.
3. If the question has multiple choice options, select the correct option.
4. Answer the question truthfully.
5. Write down your step-by-step before you reach the final answer.
6. You must provide the final answer in the following format. Answer: <Your Answer>"""


feat2question = {
    "AGE": {
        "question": "What is the current age of the patient?",
        "type": "measurement",
        "default": 30,
    },
    "AGE_FIRST CHILD BIRTH": {
        "question": "At what age did the patient give birth to their first child?",
        "type": "measurement",
        "default": 18,
    },
    "CONTRACEPTIVE_DURATION_MNTHS": {
        "question": "For how many months has the patient used contraceptive methods?",
        "type": "measurement",
        "default": 18,
    },
    "PHYSICAL ACTIVITY_DURATION_MINS": {
        "question": "On average, how many minutes does the patient engage in physical activity daily?",
        "type": "measurement",
        "default": 18,
    },
    "HEIGHT (IN CMS)": {
        "question": "What is the patient's height in centimeters?",
        "type": "measurement",
        "default": 18,
    },
    "EDUCATION": {
        "question": "What is the highest level of education the patient has completed?",
        "options": {
            "GRADUATE": "Graduate level of education",
            "ILLITERATE": "No formal education, unable to read or write",
            "INTERMEDIATE": "Education between primary and secondary levels",
            "POST GRADUATE": "Education beyond the undergraduate level",
            "PRIMARY": "Primary school level education",
            "SECONDARY": "Secondary school level education",
        },
        "default": "ILLITERATE",
    },
    "OCCUPATION": {
        "question": "What is the patient's occupation?",
        "options": {
            "HOUSEWIFE": "HOUSEWIFE",
            "PROFESSIONAL": "PROFESSIONAL",
            "SEMI-PROFESSIONAL": "SEMI-PROFESSIONAL",
            "SEMI-SKILLED": "SEMI-SKILLED",
            "SKILLED": "SKILLED",
            "STUDENT": "STUDENT",
            "UNEMPLOYED": "UNEMPLOYED",
            "UNSKILLED": "UNSKILLED",
        },
        "default": "HOUSEWIFE",
    },
    "FAMILY TYPE": {
        "question": "What type of family structure does the patient belong to? (e.g., nuclear, joint-family)",
        "options": {"NUCLEAR": "NUCLEAR", "JOINT": "JOINT"},
        "default": "NUCLEAR",
    },
    "REG_MENSTRUATION_History": {
        "question": "Has the patient experienced regular menstrual cycles throughout their life?",
        "options": {
            "REGULAR": "REGULAR",
            "IRREGULAR": "IRREGULAR",
            "MISSING": "MISSING",
        },
        "default": "MISSING",
    },
    "MENSTRUAL_STATUS": {
        "question": "What is the patient's current menstrual status? (e.g., pre-menopausal, menopausal, post-menopausal)",
        "options": {
            "PERI-MENOPAUSAL": "PERI-MENOPAUSAL",
            "POST-MENOPAUSAL": "POST-MENOPAUSAL",
            "PRE-MENOPAUSAL": "PRE-MENOPAUSAL",
        },
        "default": "PERI-MENOPAUSAL",
    },
    "HOT FLUSHES": {
        "question": "Has the patient experienced hot flushes?",
        "options": {"YES": "YES", "NO": "NO", "NA": "NA"},
        "default": "NA",
    },
    "CONCEPTION(NATURALLY CONCEIVE/IVF)": {
        "question": "Did the patient have any previous experiences with conception, either naturally or through IVF?",
        "options": {"NATURAL": "NATURAL", "IVF": "IVF", "NA": "NA"},
        "default": "NUCLEAR",
    },
    "HRT": {
        "question": "Has the patient ever undergone Hormone Replacement Therapy (HRT)?",
        "options": {"YES": "YES", "NO": "NO"},
        "default": "NO",
    },
    "FAMILYHO_CANCER": {
        "question": "Does the patient has a family history for cancer? Is any of the patient's family members ever been diagnosed with cancer in the past?",
        "options": {"YES": "YES", "NO": "NO"},
        "default": "NO",
    },
    "FAMILYHO_MEMBER_TYPE": {
        "question": "Is there a history of cancer in the patient's family? What degree of immediate relative had cancer in the patient's family?",
        "options": {"NA": "NA", "FIRST": "FIRST", "SECOND": "SECOND", "THIRD": "THIRD"},
        "default": "NA",
    },
    "RTI/STI": {
        "question": "Has the patient ever contracted a Reproductive Tract Infection (RTI) or a Sexually Transmitted Infection (STI)?",
        "options": {"YES": "YES", "NO": "NO"},
        "default": "NO",
    },
    "FASTING": {
        "question": "Does the patient practice fasting?",
        "options": {"YES": "YES", "NO": "NO"},
        "default": "NO",
    },
    "MUSTARD OIL": {
        "question": "Does the patient use mustard oil in their day-to-day routine?",
        "options": {"YES": "YES", "NO": "NO"},
        "default": "NO",
    },
    "BREAST TRAUMA": {
        "question": "Does the patient have a history of any type of trauma or injury to their breasts? This includes physical injuries, accidents, or any other incidents that may have affected their breast tissue.",
        "options": {"YES": "YES", "NO": "NO"},
        "default": "NO",
    },
    "RADIATION_SITE_CHEST": {
        "question": "Has the patient's chest area ever been exposed to radiation, including but not limited to X-rays, CT scans, or other imaging techniques?",
        "options": {"YES": "YES", "NO": "NO"},
        "default": "NO",
    },
}


# feat2question = {
#     'AGE': {
#         "question": "What is the current age of the patient?",
#         "type": "measurement",
#         "default": 30,
#     },

#     # "MONTHLY_INCOME": {
#     #     "question": "What is the patient's average monthly income?",
#     #     "type": "measurement",
#     #     "default": -1,
#     # },

#     "PHYSICAL ACTIVITY_DURATION_MINS": {
#         "question": "What is the patient's average physical activity duration in minutes?",
#         "type": "measurement",
#         "default": -1,
#     },

#     'AGE_FIRST CHILD BIRTH': {
#         "question": "At what age did the patient give birth to their first child?",
#         "type": "measurement",
#         "default": 18,
#     },

#     'BF_DURATION_MONTHS': {
#         "question": "For how many months did the patient breastfeed their child/children?",
#         "type": "measurement",
#         "default": 18,
#     },

#     'CONTRACEPTIVE_DURATION_MNTHS': {
#         "question": "For how many months has the patient used contraceptive methods?",
#         "type": "measurement",
#         "default": 18,
#     },

#     'PHYSICAL ACTIVITY_DURATION_MINS': {
#         "question": "On average, how many minutes does the patient engage in physical activity daily?",
#         "type": "measurement",
#         "default": 18,
#     },

#     'HEIGHT (IN CMS)': {
#         "question": "What is the patient's height in centimeters?",
#         "type": "measurement",
#         "default": 18,
#     },

#     'EDUCATION': {
#         "question": "What is the highest level of education the patient has completed?",
#         "options": {
#             "GRADUATE": "Graduate level of education",
#             "ILLITERATE": "No formal education, unable to read or write",
#             "INTERMEDIATE": "Education between primary and secondary levels",
#             "POST GRADUATE": "Education beyond the undergraduate level",
#             "PRIMARY": "Primary school level education",
#             "SECONDARY": "Secondary school level education",
#         },
#         "default": "ILLITERATE"
#     },

#     'OCCUPATION': {
#         "question": "What is the patient's occupation?",
#         "options": {
#             'HOUSEWIFE': 'HOUSEWIFE',
#             'PROFESSIONAL': 'PROFESSIONAL',
#             'SEMI-PROFESSIONAL': 'SEMI-PROFESSIONAL',
#             'SEMI-SKILLED': 'SEMI-SKILLED',
#             'SKILLED': 'SKILLED',
#             'STUDENT': 'STUDENT',
#             'UNEMPLOYED': 'UNEMPLOYED',
#             'UNSKILLED': 'UNSKILLED'
#         },
#         "default": "HOUSEWIFE"
#     },

#     'FAMILY TYPE': {
#         "question": "What type of family structure does the patient belong to? (e.g., nuclear, joint-family)",
#         "options": {
#             'NUCLEAR': 'NUCLEAR',
#             'JOINT': 'JOINT',
#         },
#         "default": "NUCLEAR"
#     },

#     'CONCEPTION(NATURALLY CONCEIVE/IVF)': {
#         "question": "Did the patient have any previous experiences with conception, either naturally or through IVF?",
#         "options": {
#             'NATURAL': 'NATURAL',
#             'IVF': 'IVF',
#             'NA': 'NA',
#         },
#         "default": "NUCLEAR"
#     },

#     'RELIGION': {
#         "question": "What is the patient's religious affiliation?",
#         "options": {
#             'HINDU': 'HINDU',
#             'CHRISTIAN': 'CHRISTIAN',
#             'MUSLIM': 'MUSLIM',
#             'SIKH': 'SIKH'
#         },
#         "default": "HINDU"
#     },

#     'REG_MENSTRUATION_History': {
#         "question": "Has the patient experienced regular menstrual cycles throughout their life?",
#         "options": {
#             'REGULAR': 'REGULAR',
#             'IRREGULAR': 'IRREGULAR',
#             'MISSING': 'MISSING',
#         },
#         "default": "MISSING"
#     },

#     'MENSTRUAL_STATUS': {
#         "question": "What is the patient's current menstrual status? (e.g., pre-menopausal, menopausal, post-menopausal)",
#         "options": {
#             'PERI-MENOPAUSAL': 'PERI-MENOPAUSAL',
#             'POST-MENOPAUSAL': 'POST-MENOPAUSAL',
#             'PRE-MENOPAUSAL': 'PRE-MENOPAUSAL',
#         },
#         "default": "PERI-MENOPAUSAL"
#     },

#     'HOT FLUSHES': {
#         "question": "Has the patient experienced hot flushes?",
#         "options": {
#             'YES': 'YES',
#             'NO': 'NO',
#             'NA': 'NA',
#         },
#         "default": "NA"
#     },

#     'HRT': {
#         "question": "Has the patient ever undergone Hormone Replacement Therapy (HRT)?",
#         "options": {
#             'YES': 'YES',
#             'NO': 'NO',
#         },
#         "default": "NO"
#     },

#     'BF_STATUS': {
#         "question": "Did the patient breastfeed their child completely?",
#         "options": {
#             'COMPLETE': 'COMPLETE',
#             'INCOMPLETE': 'INCOMPLETE',
#             'NA': 'NA',
#         },
#         "default": "NA"
#     },

#     'ABORTION': {
#         "question": "Has the patient had any abortions?",
#         "options": {
#             'YES': 'YES',
#             'NO': 'NO',
#         },
#         "default": "NO"
#     },

#     'FAMILYHO_CANCER': {
#         "question": "Does the patient has a family history for cancer? Is any of the patient's family members ever been diagnosed with cancer in the past?",
#         "options": {
#             'YES': 'YES',
#             'NO': 'NO',
#         },
#         "default": "NO"
#     },

#     'RTI/STI': {
#         "question": "Has the patient ever contracted a Reproductive Tract Infection (RTI) or a Sexually Transmitted Infection (STI)?",
#         "options": {
#             'YES': 'YES',
#             'NO': 'NO',
#         },
#         "default": "NO"
#     },

#     'FASTING': {
#         "question": "Does the patient practice fasting?",
#         "options": {
#             'YES': 'YES',
#             'NO': 'NO',
#         },
#         "default": "NO"
#     },

#     'MUSTARD OIL': {
#         "question": "Does the patient use mustard oil in their day-to-day routine?",
#         "options": {
#             'YES': 'YES',
#             'NO': 'NO',
#         },
#         "default": "NO"
#     },

#     'BREAST TRAUMA': {
#         "question": "Does the patient have a history of any type of trauma or injury to their breasts? This includes physical injuries, accidents, or any other incidents that may have affected their breast tissue.",
#         "options": {
#             'YES': 'YES',
#             'NO': 'NO',
#         },
#         "default": "NO"
#     },

#     'RADIATION_SITE_CHEST': {
#         "question": "Has the patient's chest area ever been exposed to radiation, including but not limited to X-rays, CT scans, or other imaging techniques?",
#         "options": {
#             'YES': 'YES',
#             'NO': 'NO',
#         },
#         "default": "NO"
#     },

#     'FAMILYHO_MEMBER_TYPE': {
#         "question": "Is there a history of cancer in the patient's family? What degree of immediate relative had cancer in the patient's family?",
#         "options": {
#             'NA': 'NA',
#             'FIRST': 'FIRST',
#             'SECOND': 'SECOND',
#             'THIRD': 'THIRD',
#         },
#         "default": "NA"
#     },

#     'DIETARY_PREF': {
#         "question": "What are the patient's dietary preferences? (e.g., vegetarian, non-vegetarian)",
#         "options": {
#             'VEGETARIAN': 'VEGETARIAN',
#             'NON-VEG': 'NON-VEG',
#             'VEGETARIAN+EGG': 'VEGETARIAN+EGG',
#         },
#         "default": "VEGETARIAN"
#     },

#     'HO_BREASTABNORMALITY': {
#         "question": "Does the patient have a history of any breast abnormalities?",
#         "options": {
#             'YES': 'YES',
#             'NO': 'NO',
#         },
#         "default": "NO"
#     },

#     'RADIATION H/O': {
#         "question": "Has the patient ever been exposed to any radiation in the past around their chest?",
#         "options": {
#             'YES': 'YES',
#             'NO': 'NO',
#         },
#         "default": "NO"
#     },


#     "NON-VEG_FREQUENCY": {
#         "question": "How often does the patient consume non-vegetarian food?",
#         "options": {
#             "DAILY": "Occurs every day.",
#             "FORTNIGHTLY": "Occurs every two weeks (14 days).",
#             "HALF YEARLY": "Occurs every six months (twice a year).",
#             "MONTHLY": "Occurs once a month.",
#             "NR": "Not regular or not specified.",
#             "QUARTERLY": "Occurs every three months (four times a year).",
#             "THRICE WEEKLY": "Occurs three times a week.",
#             "TWICE WEEKLY": "Occurs two times a week.",
#             "WEEKLY": "Occurs once a week.",
#             "YEARLY": "Occurs once a year.",
#         },
#         "default": "WEEKLY"
#     },

#     # "EDUCATION": {
#     #     "question": "What is the patient's level of education?",
#     #     "options": {
#     #         "GRADUATE": "Graduate level of education",
#     #         "ILLITERATE": "No formal education, unable to read or write",
#     #         "INTERMEDIATE": "Education between primary and secondary levels",
#     #         "NR": "Not Reported or Not Recorded",
#     #         "POST GRADUATE": "Education beyond the undergraduate level",
#     #         "PRIMARY": "Primary school level education",
#     #         "SECONDARY": "Secondary school level education",
#     #         "SECONDARY SCHOOL": "Same as Secondary, referring specifically to school level",
#     #     },
#     #     "default": "ILLITERATE"
#     # },

#     'PHYSICAL ACTIVITY_GRADE': {
#         "question": "What is the patient's level of physical activity?",
#         "options": {
#             "MILD": "MILD - Engages in mild physical activities like walking or light exercise.",
#             "MODERATE": "MODERATE - Engages in moderate physical activities like jogging or cycling.",
#             "NIL": "NIL - No physical activity.",
#             "NR": "NR - Activity level not recorded or not applicable.",
#             "VIGROUS": "VIGROUS - Engages in vigorous physical activities like running or intense sports."
#         },
#         "default": "MODERATE"
#     },

#     'RESIDENCE': {
#         "question": "Where does the patient live?",
#         "options": {
#             "URBAN": "URBAN - The patient resides in an urban area, typically characterized by a high population density and infrastructure.",
#             "RURAL": "RURAL - The patient resides in a rural area, typically characterized by countryside or agricultural surroundings.",
#             "NR": "NR - Residence type not recorded or not applicable.",
#         },
#         "default": "NR"
#     },

#     'SES': {
#         "question": "What is the socio-economic status of the patient?",
#         "options": {
#             "Lower": "Lower - Typically indicates lower income and limited access to resources.",
#             "Lower Middle": "Lower Middle - Indicates moderate income and some access to resources.",
#             "Middle": "Middle - Represents average income and access to basic resources.",
#             "Upper": "Upper - Indicates higher income and better access to resources.",
#             "Upper Middle": "Upper Middle - Represents high income and significant access to resources."
#         },
#         "default": "Upper"
#     },

#     "WEIGHT (IN KGS)": {
#         "question": "What is the weight of the patient in KGs?",
#         "type": "measurement",
#         "default": 65,
#     },

#     # 'HEIGHT (IN CMS)': {
#     #     "question": "What is the height of the patient in CMs?",
#     #     "type": "measurement",
#     #     "default": 152,
#     # },

#     'SBP': {
#         "question": "What is the Systolic Blood Pressure of the patient in mmHg?",
#         "type": "measurement",
#         "default": 123,
#     },

#     'RBS': {
#         "question": "What is the Random Blood Sugar of the patient in mg/dL?",
#         "type": "measurement",
#         "default": 101,
#     },

#     'WAIST_CMS': {
#         "question": "What is the waist circumference of the patient in CMs?",
#         "type": "measurement",
#         "default": 88,
#     },

#     'WHR':{
#         "question": "What is the waist to hip ratio of the patient?",
#         "type": "measurement",
#         "default": 0.9,
#     }
# }
