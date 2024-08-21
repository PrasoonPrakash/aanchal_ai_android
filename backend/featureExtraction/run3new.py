import os
import sys
import json
import numpy as np
from tqdm import tqdm
import json
import pandas as pd
from prompter import OpenAIPrompter
import copy

model = "gpt-3.5-turbo-0125"
prompter = OpenAIPrompter(model, 32)

INSTRUCTIONS = """You are a professional clinician who is experienced in medical scribing. Your task is to help the user understand a conversation between a doctor and a patient. Specifically, the user will show you a transcript of a dialogue between a doctor and a patient. Then, the user will ask a question based on the transcript. You must answer that question correctly and truthfully.

IMPORTANT INSTRUCTIONS:
1. Read the transcript carefully and identify the doctor and patient utterances.
2. Understand the question and search the transcript for the answer.
3. If the question has multiple choice options, select the correct option.
4. Answer the question truthfully.
5. You must provide answer in the following format. Answer: <Your Answer>"""


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
        "default": "GRADUATE"
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
        "default": "MILD"
    },

    'RESIDENCE': {
        "question": "Where does the patient live?",
        "options": {
            "URBAN": "URBAN - The patient resides in an urban area, typically characterized by a high population density and infrastructure.",
            "RURAL": "RURAL - The patient resides in a rural area, typically characterized by countryside or agricultural surroundings.",
            "NR": "NR - Residence type not recorded or not applicable.",
        },
        "default": "URBAN"
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
        "default": 50,
    },

    'HEIGHT (IN CMS)': {
        "question": "What is the height of the patient in CMs?",
        "type": "measurement",
        "default": 150,
    },

    'SBP': {
        "question": "What is the Systolic Blood Pressure of the patient in mmHg?",
        "type": "measurement",
        "default": 100,
    },

    'RBS': {
        "question": "What is the Random Blood Sugar of the patient in mg/dL?",
        "type": "measurement",
        "default": 100,
    },

    'WAIST_CMS': {
        "question": "What is the waist circumference of the patient in CMs?",
        "type": "measurement",
        "default": 100,
    },

    'WHR':{
        "question": "What is the waist to hip ratio of the patient?",
        "type": "measurement",
        "default": 1.5,
    }
}


def create_prompt(text, feat_id):
    prompt = [{'role': 'system', 'content': INSTRUCTIONS}]

    user = "Read the following doctor-patient dialog and answer the follow-up question.\n\n"
    user += f"Dialog:\n{text}\n\n"
    question = feat2question[feat_id]['question']
    options = feat2question[feat_id].get('options', [])

    user += f"Question: {question}"
    if len(options) > 0:
        user += " Select one of the following options.\n"
        for ii, opt in enumerate(options):
            user += f"{opt}: {options[opt]}\n"
    elif feat2question[feat_id].get('type') == 'measurement':
        user += " If answer is not present in the dialog, write the default value provided. Answer is strictly a numerical value."

    prompt.append({'role': 'user', 'content': user})

    return prompt


def postprocess_mcq_response(response, feat_id, defval):
    ret = dict()

    options = sorted(feat2question[feat_id]['options'], key=lambda x: -len(x))
    text = response.replace('Answer:', '').strip()

    found = False
    for opt in options:
        if opt in response and not found:
            ret[opt] = 1
            found = True
        else:
            ret[opt] = 0

    if not found:
        # ret['NR'] = 1
        ret[defval] = 1

    ret1 = {f"{feat_id}_{k}": v for k, v in ret.items()}

    for k, v in ret.items():
        if v == 1:
            return ret1, {feat_id: k}


def postprocess_measurement(response, feat_id, defval):
    ret = dict()
    text = response.replace('Answer:', '').strip()

    def is_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    for word in text.split():
        if is_float(word):
            fval = float(word)
            return {feat_id: fval}

    return {feat_id: defval}


def extract_features(text):
    all_features = dict()
    all_features_noonehot = dict()
    for feat_id in feat2question:
        defval = feat2question[feat_id]["default"]
        try:
            prompt = create_prompt(text, feat_id)
            ret = prompter(prompt)
            if feat2question[feat_id].get('type') == 'measurement':
                fval = postprocess_measurement(ret, feat_id, defval)
                fval_noonehot = copy.deepcopy(fval)
            else:
                fval, fval_noonehot = postprocess_mcq_response(ret, feat_id, defval)

        except Exception as e:
            print(f'ERROR! Failed to extract {feat_id}.')
            print(e)

            if feat2question[feat_id].get('type') == 'measurement':
                fval = {feat_id: defval}
                fval_noonehot = copy.deepcopy(fval)
            else:
                fval = {f"{feat_id}_{opt}": 0 for opt in feat2question[feat_id]['options']}
                # fval['NR'] = 1
                fval[defval] = 1
                fval_noonehot = {feat_id: defval}

        all_features.update(fval)
        all_features_noonehot.update(fval_noonehot)
    print(all_features)

    all_features["BMI"]=(all_features["WEIGHT (IN KGS)"])/((all_features["HEIGHT (IN CMS)"]/100)**2)
    all_features_noonehot["BMI"] = all_features["BMI"]

    if all_features["WHR"]>0.8:
        all_features["ABD_OBESITY_YES"]=1
        all_features["ABD_OBESITY_NO"]=0
        all_features_noonehot["ABD_OBESITY"] = "YES"
    else:
        all_features["ABD_OBESITY_YES"]=0
        all_features["ABD_OBESITY_NO"]=1
        all_features_noonehot["ABD_OBESITY"] = "NO"

    all_features['ABD_OBESITY_#VALUE!']=0

    LIST=['WHO_BMI_CAT_NR', 'WHO_BMI_CAT_OBESE CLASS I',
       'WHO_BMI_CAT_OBESE CLASS II', 'WHO_BMI_CAT_OBESE CLASS III',
       'WHO_BMI_CAT_OVERWEIGHT', 'WHO_BMI_CAT_PRE OBESE',
       'WHO_BMI_CAT_UNDERWEIGHT', "WHO_BMI_CAT_0VERWEIGHT",'WHO_BMI_CAT_NORMAL']

    if all_features["BMI"]<18.5:
        all_features[LIST[6]]=1
        for i in range(0,9):
            if i!=6:
                all_features[LIST[i]]=0
    elif all_features["BMI"]>=18.5 and all_features["BMI"]<25:
        all_features[LIST[8]]=1
        for i in range(0,9):
            if i!=8:
                all_features[LIST[i]]=0
    elif all_features["BMI"]>=25 and all_features["BMI"]<30:
        all_features[LIST[4]]=1
        for i in range(0,9):
            if i!=4:
                all_features[LIST[i]]=0
    elif all_features["BMI"]>=30 and all_features["BMI"]<35:
        all_features[LIST[1]]=1
        for i in range(0,9):
            if i!=1:
                all_features[LIST[i]]=0
    elif all_features["BMI"]>=35 and all_features["BMI"]<40:
        all_features[LIST[2]]=1
        for i in range(0,9):
            if i!=2:
                all_features[LIST[i]]=0
    elif all_features["BMI"]>=40:
        all_features[LIST[3]]=1
        for i in range(0,9):
            if i!=3:
                all_features[LIST[i]]=0

    all_features_noonehot["WHO_BMI_CAT"] = LIST[8]
    for i in range(0,9):
        if all_features[LIST[i]]==1:
            all_features_noonehot["WHO_BMI_CAT"] = LIST[i]
            break

    if all_features["STERILISATION (B/L TUBAL LIGATION)_NR"]==1:
        all_features["STERILISATION (B/L TUBAL LIGATION)_NO"]=1
        all_features_noonehot["STERILISATION (B/L TUBAL LIGATION)"] = "NO"

    return all_features, all_features_noonehot


class featEx:
    def __init__(self,name):
        np.random.seed(42)
        self.name=name
        self.feat_dict={}

    def extractFeatures(self):
        engPath="translatedFiles/"+self.name+"_english.txt"
        with open(engPath,'r', encoding="utf-8") as f:
            engText=f.read()
        #print(engText)

        feat_dict, feat_dict_noonehot = extract_features(engText)
        self.feat_dict = feat_dict

        name=self.name
        df=pd.DataFrame(feat_dict, index=[0])
        df.to_csv("csvFiles/"+name+"_data.csv",index=False)

        name=self.name
        df=pd.DataFrame(feat_dict_noonehot, index=[0])
        df.to_csv("csvNoOneHot/"+name+"_data_nooneshot.csv",index=False)


if __name__ == '__main__':
    name=sys.argv[1]
    obj=featEx(name)
    obj.extractFeatures()
