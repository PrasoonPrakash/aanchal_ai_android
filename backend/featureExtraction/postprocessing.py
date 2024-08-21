import numpy as np
import pandas as pd
import sys
import re

def extract_age(text):
    pattern = r"(\d+) year"
    mts = re.findall(pattern, text)
 
    if len(mts) == 0:
        return -1
 
    return int(mts[0])
 
 
def extract_marital_status(text):
    tt = text.lower()
 
    if 'single' in tt or 'unmarried' in tt:
        return 'SINGLE'
 
    if 'married' in tt:
        return 'MARRIED'
 
    if 'divorced' in tt:
        return 'DIVORCED'
 
    if 'widowed' in tt:
        return 'WIDOWED'
 
 
def extract_marriage_duration(text):
    return extract_age(text)
 
 
def extract_education(text):
    tt = text.lower()
 
    if 'post graduate' in tt or 'postgraduate' in tt or 'post-graduate' in tt:
        return 'POST GRADUATE'
 
    if 'graduate' in tt or 'bachelor' in tt or 'bachelors' in tt:
        return 'GRADUATE'
 
    if 'secondary school completed' in tt or 'high school' in tt or 'secondary education' in tt:
        return 'SECONDARY SCHOOL COMPLETED'
 
    if 'primary' in tt or 'elementary' in tt:
        return 'PRIMARY'
 
    if 'intermediate' in tt or 'diploma' in tt:
        return 'INTERMEDIATE'
 
    if 'illiterate' in tt:
        return 'ILLITERATE'
 
    return "None"  # If no match is found
 
 
def extract_occupation(text):
    tt = text.lower()
 
    if any(keyword in tt for keyword in ['professional']):
        return 'Professional'.upper()
 
    if any(keyword in tt for keyword in ['semi professional', 'semi-professional']):
        return 'Semi Professional'.upper()
 
    if any(keyword in tt for keyword in ['clerical', 'shop owner', 'farmer']):
        return 'Clerical/Shop Owner/ Farmer'.upper()
 
    if any(keyword in tt for keyword in ['skilled']):
        return 'Skilled'.upper()
 
    if any(keyword in tt for keyword in ['semi skilled', 'semi-skilled']):
        return 'Semi-skilled'.upper()
 
    if any(keyword in tt for keyword in ['unskilled']):
        return 'Unskilled'.upper()
 
    if any(keyword in tt for keyword in ['student', 'housewife']):
        return 'Student/Housewife'.upper()
 
    if 'unemployed' in tt:
        return 'Unemployed'.upper()
 
    return 'None'  # Return None if no occupation match is found
 
 
def extract_family_type(text):
    tt = text.lower()
 
    if 'joint' in tt:
        return 'JOINT'
 
    if 'nuclear' in tt:
        return 'NUCLEAR'
 
    # You can add more specific conditions for other types if needed
    # For simplicity, any other text will be categorized as 'others'
    return 'OTHERS'
 
 
def extract_religion(text):
    tt = text.lower()
 
    if 'hindu' in tt:
        return 'Hindu'.upper()
 
    if 'muslim' in tt or 'islam' in tt:
        return 'Muslim'.upper()
 
    if 'sikh' in tt:
        return 'Sikh'.upper()
 
    if 'christian' in tt:
        return 'Christian'.upper()
 
    return 'Others'.upper()
 
 
def extract_menstrual_status(text):
    ttext = text.lower()
 
    if 'POST-MENOPAUSAL'.lower() in ttext:
        return 'POST-MENOPAUSAL'
 
    if 'PRE-MENOPAUSAL'.lower() in ttext:
        return 'PRE-MENOPAUSAL'
 
    return 'NONE'
 
 
def extract_menopause_type(text):
    if text is None:
        return 'NONE'
    ttext = text.lower()
 
    if "HORMONAL TREATMENT".lower() in ttext:
        return "HORMONAL TREATMENT"
 
    if "CHEMO-INDUCED".lower() in ttext:
        return "CHEMO-INDUCED"
 
    if "HYSTERECTOMY".lower() in ttext:
        return "HYSTERCTOMY"
 
    return 'NONE'
 
 
def extract_physical_activity(text):
    if text is None:
        return 'NONE'
 
    ttext = text.lower()
 
    if 'yes' in ttext:
        return 'YES'
 
    elif 'no' in ttext:
        return 'NO'
 
    return 'NONE'
 
extract_abortion = extract_physical_activity
 
def extract_abortion_number(text):
    if text is None:
        return 'NONE'
 
    if text == 'nan':
        return 'NONE'
 
    elif 'Number of abortions:' in text:
        ttext = text.replace('Number of abortions:', '').strip()
        ttext = int(float(ttext))
 
        if ttext == 0:
            return 'NONE'
 
        return str(ttext)
 
    elif text.isalnum():
        return str(int(float(text)))
 
    else:
        return 'NONE'

name=sys.argv[1]
csvPath="/home/prasoon/breast_cancer_project/trial1/featureExtraction/csvFiles/" + name + "_data.csv"
df=pd.read_csv(csvPath)
       
def process_column(column_name, series):
    function_name = f'extract_{column_name.lower()}'
    if function_name in globals():
        function = globals()[function_name]
        return series.apply(function)
    else:
        return series

# Apply the post-processing functions to the corresponding columns
for column in df.columns:
    df[column] = process_column(column, df[column])

#text=extract_abortion_number(df["ABORTION_NO."][0])
#series1=df["ABORTION_NO."]
func1=globals()["extract_abortion_number"]
df["ABORTION_NO."].apply(func1)

#text=extract_menopause_type(df["TYPE OF MENOPAUSE(NATURAL/HYSTERECTOMY)"][0])
#series2=df["TYPE OF MENOPAUSE(NATURAL/HYSTERECTOMY)"]
func2=globals()["extract_menopause_type"]
df["TYPE OF MENOPAUSE(NATURAL/HYSTERECTOMY)"].apply(func2)
    
df.to_csv("/home/prasoon/breast_cancer_project/trial1/featureExtraction/afterPP/"+name+"_afterPP.csv", index=False)