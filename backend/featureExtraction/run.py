import os
import sys
import json
import numpy as np
from tqdm import tqdm
import json
import pandas as pd
import postprocessing

from prompter import OpenAIPrompter
from feat2question import feat2question, INSTRUCTIONS

with open("/home/prasoon/breast_cancer_project/trial1/featureExtraction/data.json",'r') as file:
    data=json.load(file)
    #print(f'Total {len(data)}')
model = "gpt-3.5-turbo-0125"

prompter = OpenAIPrompter(model, max_tokens=16)

#feat_ids=["AGE"]
np.random.seed(42)

feat_ids = ["AGE", "MARITAL STATUS", "MARRIAGE_DURATION",
         "EDUCATION", "OCCUPATION", "FAMILY TYPE", "RELIGION",
        # Medical
        # "PAST_SURGERY", # --> Missing
         "MENSTRUAL_STATUS",
         "TYPE OF MENOPAUSE(NATURAL/HYSTERECTOMY)", "PHYSICAL ACTIVITY",
         "ABORTION",
        "ABORTION_NO.",]

"""feat_ids=["WEIGHT (IN KGS)",	"HEIGHT (IN CMS)",	"BMI",	"WAIST_CMS",	"RBS",	"WHR",	"SBP",	"CAUSE_MENOPAUSE",	"PAST_SURGERY",	"STERILISATION (B/L TUBAL LIGATION)",	"NON-VEG_FREQUENCY",	"EDUCATION",	"PHYSICAL ACTIVITY_GRADE",	"RESIDENCE",	"SES",	"WHO_BMI_CAT",	"ABD_OBESITY"
]

feat_ids = ["AGE", "MARITAL STATUS", "MARRIAGE_DURATION",
         "EDUCATION", "OCCUPATION", "FAMILY TYPE", "RELIGION",
        # Medical
        # "PAST_SURGERY", # --> Missing
         "MENSTRUAL_STATUS",
         "TYPE OF MENOPAUSE(NATURAL/HYSTERECTOMY)", "PHYSICAL ACTIVITY",
         "ABORTION",
        "ABORTION_NO.",]

np.random.seed(42)
idxs = np.random.choice(len(data), size=1)
#print(idxs)
exemplars = [data[ii] for ii in idxs]

def get_zero_shot_prompt(sample, feat_id):
    prompt_elems = [{'role': 'system', 'content': INSTRUCTIONS}]
    
    usr_prompt = "Read the doctor-patient dialogue and answer the following question.\n\n"
    usr_prompt += "Transcript:\n"
    usr_prompt += sample
    usr_prompt += "\n\n"

    qcfg = feat2question[feat_id]
    usr_prompt += "Question: " + qcfg['question']
    if 'options' in qcfg:
        usr_prompt += " Select one of the following options - " + ', '.join(qcfg['options'])

    prompt_elems.append({"role": "user", "content": usr_prompt})
    prompt_elems.append({"role": "assistant", "content": "Answer: "})

    return prompt_elems


def get_few_shot_prompt(sampleText, exemplars, feat_id):
    prompt_elems = [{'role': 'system', 'content': INSTRUCTIONS}]

    for entry in exemplars:
        usr_prompt = "Read the doctor-patient dialogue and answer the following quesiton.\n\n"
        usr_prompt += "[Transcript]\n"
        usr_prompt += entry['en_dialog']
        usr_prompt += "\n\n"

        qcfg = feat2question[feat_id]
        usr_prompt += "[Question]\n" + qcfg['question']
        if 'options' in qcfg:
            usr_prompt += " Select one of the following options - " + ', '.join(qcfg['options'])
        asst_prompt = qcfg['answer'].format(entry['labels'][feat_id])  ##
        prompt_elems.append({"role": "user", "content": usr_prompt})
        prompt_elems.append({"role": "assistant", "content": asst_prompt})

    usr_prompt = "Read the doctor-patient dialogue and answer the following quesiton.\n\n"
    usr_prompt += "[Transcript]\n"
    usr_prompt += sampleText
    usr_prompt += "\n\n"

    qcfg = feat2question[feat_id]
    usr_prompt += "[Question]\n" + qcfg['question']
    if 'options' in qcfg:
        usr_prompt += " Select one of the following options - " + ', '.join(qcfg['options'])
    asst_prompt = qcfg['answer'].split('{}')[0].strip()  ##
    prompt_elems.append({"role": "user", "content": usr_prompt})
    prompt_elems.append({"role": "assistant", "content": asst_prompt})

    return prompt_elems

def extractFeatures(name):
    feat_dict={} #-->data to be stored in df
#make fn
    for feat in feat_ids:
        elems = get_few_shot_prompt(engText, exemplars, feat)
        ret = prompter(elems)
        feat_dict[feat]=ret
    
    df = pd.DataFrame([feat_dict],)

    # Save the DataFrame to a CSV file
    df.to_csv('.csv', index=False) """
    
class featEx:
    def __init__(self,name):
        idxs = np.random.choice(len(data), size=1)
        self.exemplars = [data[ii] for ii in idxs]
        self.name=name
        self.feat_dict={}
        self.engPath="/home/prasoon/breast_cancer_project/trial1/featureExtraction/translatedFiles/"+name+"_english.txt"
        #self.engText=" "
    
    def get_zero_shot_prompt(self, sample, feat_id):
        prompt_elems = [{'role': 'system', 'content': INSTRUCTIONS}]
        
        usr_prompt = "Read the doctor-patient dialogue and answer the following question.\n\n"
        usr_prompt += "Transcript:\n"
        usr_prompt += sample
        usr_prompt += "\n\n"
    
        qcfg = feat2question[feat_id]
        usr_prompt += "Question: " + qcfg['question']
        if 'options' in qcfg:
            usr_prompt += " Select one of the following options - " + ', '.join(qcfg['options'])
    
        prompt_elems.append({"role": "user", "content": usr_prompt})
        prompt_elems.append({"role": "assistant", "content": "Answer: "})
    
        return prompt_elems
        
    def get_few_shot_prompt(self, sampleText, exemplars, feat_id):
        prompt_elems = [{'role': 'system', 'content': INSTRUCTIONS}]
        exemplars=self.exemplars
        
        for entry in exemplars:
            usr_prompt = "Read the doctor-patient dialogue and answer the following quesiton.\n\n"
            usr_prompt += "[Transcript]\n"
            usr_prompt += entry['en_dialog']
            usr_prompt += "\n\n"
    
            qcfg = feat2question[feat_id]
            usr_prompt += "[Question]\n" + qcfg['question']
            if 'options' in qcfg:
                usr_prompt += " Select one of the following options - " + ', '.join(qcfg['options'])
            asst_prompt = qcfg['answer'].format(entry['labels'][feat_id])  ##
            prompt_elems.append({"role": "user", "content": usr_prompt})
            prompt_elems.append({"role": "assistant", "content": asst_prompt})
    
        usr_prompt = "Read the doctor-patient dialogue and answer the following quesiton.\n\n"
        usr_prompt += "[Transcript]\n"
        usr_prompt += sampleText
        usr_prompt += "\n\n"
    
        qcfg = feat2question[feat_id]
        usr_prompt += "[Question]\n" + qcfg['question']
        if 'options' in qcfg:
            usr_prompt += " Select one of the following options - " + ', '.join(qcfg['options'])
        asst_prompt = qcfg['answer'].split('{}')[0].strip()  ##
        prompt_elems.append({"role": "user", "content": usr_prompt})
        prompt_elems.append({"role": "assistant", "content": asst_prompt})
    
        return prompt_elems
        
    def extractFeatures(self):
        #engText=self.engText
        with open(self.engPath,'r', encoding="utf-8") as f:
            engText=f.read()
        feat_dict=self.feat_dict
        exemplars=self.exemplars
        for feat in feat_ids:
            elems = self.get_few_shot_prompt(engText, exemplars, feat)
            ret = prompter(elems)
            feat_dict[feat]=ret
            #print(ret)
        name=self.name
        df=pd.DataFrame(feat_dict, index=[0])
        df.to_csv("/home/prasoon/breast_cancer_project/trial1/featureExtraction/csvFiles/"+name+"_data.csv",index=False)

if __name__ == '__main__':
    name=sys.argv[1]
    obj=featEx(name)
    
    obj.extractFeatures()
    print(obj.feat_dict)
    print(obj.exemplars)
    #print(obj.engText)
    """################ global or init of python object
    with open("/home/prasoon/breast_cancer_project/trial1/featureExtraction/data.json",'r') as file:
        data=json.load(file)
    #print(f'Total {len(data)}')
    model = "gpt-3.5-turbo-0125"

    prompter = OpenAIPrompter(model, max_tokens=16)

    feat_ids = [
         "AGE", "MARITAL STATUS", "MARRIAGE_DURATION",
         "EDUCATION", "OCCUPATION", "FAMILY TYPE", "RELIGION",
        # Medical
        # "PAST_SURGERY", # --> Missing
         "MENSTRUAL_STATUS",
         "TYPE OF MENOPAUSE(NATURAL/HYSTERECTOMY)", "PHYSICAL ACTIVITY",
         "ABORTION",
        "ABORTION_NO.",
    ]

    np.random.seed(42)
    idxs = np.random.choice(len(data), size=1)
    print(idxs)
    exemplars = [data[ii] for ii in idxs]
    ##################
    
    for jj, entry in enumerate(tqdm(data)):
        if model not in entry:
            entry[model] = dict()
        if jj in idxs:
            entry['is_exemplar'] = True
            continue
    
#make dictionary of ret
    with open("/home/prasoon/breast_cancer_project/trial1/extractedFeat.txt", 'w', encoding="utf-8") as fp:
        json.dump(feat_dict, fp, indent=2, ensure_ascii=False)"""
    
