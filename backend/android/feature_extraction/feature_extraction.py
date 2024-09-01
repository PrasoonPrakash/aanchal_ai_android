print('WARNING......')
from .prompter import prompter
from .translate import translate
from .feat_config import INSTRUCTIONS, feat2question

from copy import deepcopy
import pandas as pd
import os
from tqdm import tqdm

os.environ['NO_PROXY'] = "localhost,127.0.0.1"


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
        user += " If answer is not present in the dialog, write -1. Answer is strictly a numerical value." #Use the following format.\n"
        # user += " Answer: <Your Answer>\n"

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
    for feat_id in tqdm(feat2question):
        defval = feat2question[feat_id]["default"]
        try:
            prompt = create_prompt(text, feat_id)
            ret = prompter(prompt, max_new_tokens=512)
            # print(feat_id)
            # print(ret)
            # print()
            if feat2question[feat_id].get('type') == 'measurement':
                fval = postprocess_measurement(ret, feat_id, defval)
                fval_noonehot = deepcopy(fval)
            else:
                fval, fval_noonehot = postprocess_mcq_response(ret, feat_id, defval)

        except Exception as e:
            print(f'ERROR! Failed to extract {feat_id}.')
            print(e)

            if feat2question[feat_id].get('type') == 'measurement':
                fval = {feat_id: defval}
                fval_noonehot = deepcopy(fval)
            else:
                fval = {f"{feat_id}_{opt}": 0 for opt in feat2question[feat_id]['options']}
                # fval['NR'] = 1
                fval[defval] = 1
                fval_noonehot = {feat_id: defval}

        all_features.update(fval)
        all_features_noonehot.update(fval_noonehot)
    # print(all_features)
    return all_features, all_features_noonehot


class featEx:
    def __init__(self, name):
        # np.random.seed(42)
        self.name = name
        self.feat_dict = {}

    def extractFeatures(self):
        # TODO: USE HINDI TRANSCRIPT HERE--- We take care of translation
        hindiPath = "/home/prasoon/breast_cancer_project/trial1/featureExtraction/hindiTranscripts/" + self.name + "_hindi.txt"
        with open(hindiPath,'r', encoding="utf-8") as f:
            hindiText = f.read()

        engText = translate(hindiText)

        engPath = "/home/prasoon/breast_cancer_project/trial1/featureExtraction/translatedFiles/" + self.name + "_english.txt"
        with open(engPath, 'w', encoding='utf-8') as fp:
            fp.write(engText)
        
        feat_dict, feat_dict_noonehot = extract_features(engText)
        self.feat_dict = feat_dict

        name = self.name
        df = pd.DataFrame(feat_dict, index=[0])
        df.to_csv("/home/prasoon/breast_cancer_project/trial1/featureExtraction/csvFiles/" + name + "_data.csv", index=False)

        name = self.name
        df = pd.DataFrame(feat_dict_noonehot, index=[0])
        df.to_csv("/home/prasoon/breast_cancer_project/trial1/featureExtraction/csvNoOneHot/" + name + "_data_nooneshot.csv", index=False)


if __name__ == '__main__':
    obj = featEx('AUD-20240827-WA0001')
    obj.extractFeatures()

