from flask import Flask, request, jsonify, render_template, send_file, abort

import os
import pickle
import pandas as pd
import numpy as np

import time
import sys
from datetime import datetime
import json, os

from feature_extraction import extract_features, translate

# ENVIRONMENT SETUP
if 'localhost' in os.environ.get('LLAMA3_SERVICE', 'http://localhost:8000'):
    from transcription import transcribe
else:
    print('Using transcribe2')
    from transcription import transcribe2 as transcribe

STORAGE_BASE = './data/'
UPLOAD_DIR = os.path.join(STORAGE_BASE, 'audio')
FEATURE_DIR = os.path.join(STORAGE_BASE, 'features') # Will extracted features csv
FEATURE_DIR2 = os.path.join(STORAGE_BASE, 'final_features') # Will extracted features csv
TRANSCRIPT_DIR = os.path.join(STORAGE_BASE, 'transcripts')
TRANSLATION_DIR = os.path.join(STORAGE_BASE, 'translations')

TRANSCRIPT = None
TRANSLATION = None

SESSION_TAG = None
EXCEPTION_TAG = False


for dname in [STORAGE_BASE, UPLOAD_DIR, FEATURE_DIR, TRANSCRIPT_DIR, TRANSLATION_DIR, FEATURE_DIR2]:
    os.makedirs(dname, exist_ok=True)

# Load the scaler
with open('./model/scale.pkl','rb') as f:
    preprocessor = pickle.load(f)

# Load the trained model
with open('./model/model.pkl', 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_file():
    global SESSION_TAG
    global EXCEPTION_TAG
    global TRANSCRIPT
    global TRANSLATION
    
    print('Starting a new session....')
    SESSION_TAG = None
    EXCEPTION_TAG = False
    TRANSCRIPT = None
    TRANSLATION = None
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Get the extension of the file
    # TODO: Avoid uploads without extensions.
    file_extension = file.filename.rsplit('.', 1)[-1].lower()
    TAG = generate_request_id()
    print('Processing file with tag', TAG)

    filename = f"{TAG}.{file_extension}"
    filename = os.path.join(UPLOAD_DIR, filename)
    file.save(filename)

    try:
        process_audio(audiofile=filename, tag=TAG)
        SESSION_TAG = TAG
        print('Global tag is set to', SESSION_TAG)
        return jsonify({"result":"Audio file uploaded, transcripted and translated. Features have been extracted."})

    except Expection as e:
        print('Audio processing failed with err', str(e))
        SESSION_TAG = None
        EXCEPTION_TAG = True
        TRANSCRIPT = None
        TRANSLATION = None
        return jsonify({"result":"couldn't process file"})


@app.route('/hindi', methods=["GET"])
def hindi():
    global SESSION_TAG
    global EXCEPTION_TAG
    global TRANSCRIPT
    if TRANSCRIPT is None:
        if EXCEPTION_TAG:
            message = "There was an error in processing. Please re-try uploading the audio."
        else:
            message = "Audio file is under process. Please check after a couple of minutes."
        return jsonify({"transcript": message}), 200
    
    # with open(os.path.join(TRANSCRIPT_DIR, f"{SESSION_TAG}.txt"), 'r') as fp:
    #     message = fp.read()
    message = TRANSCRIPT

    return jsonify({"transcript": message}), 200


@app.route('/english',methods=["GET"])
def english():
    global SESSION_TAG
    global EXCEPTION_TAG
    global TRANSLATION
    if TRANSLATION is None:
        if EXCEPTION_TAG:
            message = "There was an error in processing. Please re-try uploading the audio."
        else:
            message = "Audio file is under process. Please check after a couple of minutes."
        return jsonify({"transcript": message}), 200
    
    # with open(os.path.join(TRANSLATION_DIR, f"{SESSION_TAG}.txt"), 'r') as fp:
    #     message = fp.read()
    message = TRANSLATION

    return jsonify({"translation": message}), 200


@app.route('/name',methods=["GET"])
def features():
    global SESSION_TAG
    global EXCEPTION_TAG
    if SESSION_TAG is None:
        if EXCEPTION_TAG:
            message = "There was an error in processing. Please re-try uploading the audio."
        else:
            message = "Audio file is under process. Please check after a couple of minutes."
        return jsonify({"transcript": message}), 200

    return jsonify({"name": SESSION_TAG}), 200


@app.route("/data",methods=["GET"])
def data():
    global SESSION_TAG
    global EXCEPTION_TAG
    if SESSION_TAG is None:
        if EXCEPTION_TAG:
            message = "There was an error in processing. Please re-try uploading the audio."
        else:
            message = "Audio file is under process. Please check after a couple of minutes."
        return jsonify({"transcript": message}), 200

    csvPath = os.path.join(FEATURE_DIR, f"{SESSION_TAG}.csv")
    df = pd.read_csv(csvPath)
    dicti = df.to_dict()
    return jsonify(dicti)


@app.route("/download_csv", methods=['GET'])
def download_csv():
    global SESSION_TAG
    global EXCEPTION_TAG
    if SESSION_TAG is None:
        if EXCEPTION_TAG:
            message = "There was an error in processing. Please re-try uploading the audio."
        else:
            message = "Audio file is under process. Please check after a couple of minutes."
        return jsonify({"transcript": message}), 200

    try:
        csv_file_path = os.path.join(FEATURE_DIR, f"{SESSION_TAG}.csv")
        if not os.path.exists(csv_file_path):
            abort(404, description="CSV file not found")
            print("error 404 file not found")
            
        # Serve the file directly
        return send_file(csv_file_path,
                         as_attachment=True,
                         download_name='extracted_features.csv',  # This is the name that will be used when downloading
                         mimetype='appication/csv')

    except NotFound:
        print("The requested CSV file was not found on the server.")
        return "The requested CSV file was not found on the server.", 404

    except Exception as e:
        app.logger.error(f"Error in download_csv: {str(e)}")
        print(f"Error in download_csv: {str(e)}")
        return "An error occurred while trying to download the file.", 500


@app.route("/uploadCsvAndPredict", methods=['POST'])
def uploadCsvAndPredict():
    """
    Reads the uploaded file, processes it and returns the results.
    """
    global SESSION_TAG
    if SESSION_TAG is None:
        message = "There was an error in processing. Please re-try uploading the audio."
        return jsonify({"transcript": message}), 200

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = f"{SESSION_TAG}.csv"
    filename = os.path.join(FEATURE_DIR2, filename)
    file.save(filename)
    prediction, prob_0, prob_1 = process_and_predict(SESSION_TAG)

    if prediction == 1:
        s = f"मूल्यांकन के आधार पर, स्तन कैंसर की संभावना {prob_1}% अनुमानित है। \n  संदेश - ध्यान दें! इस मरीज को आपके द्वारा दी गई जानकारी के आधार पर एक मैमोग्राफी कराने की सलाह दी जाती है। कृपया मरीज को NCI झज्जर में मैमोग्राम कराने के लिए सलाह दें।\n\nBased on the assessment, the estimated probability of breast cancer is {prob_1}%. \n Message- Attention ! This patient is advised to have a mammography, based on the history you have given us. Please counsel the patient to go to NCI Jhajjar for a mammogram."
    else:
        s = f"मूल्यांकन के आधार पर, स्तन कैंसर नहीं होने की संभावना {prob_0}% अनुमानित है। \n संदेश -  इस मरीज को आपके द्वारा दी गई जानकारी के आधार पर स्तन कैंसर का कोई भी संभावित खतरा नहीं है। कृपया मरीज को अपनी नियमित फॉलो-अप जारी रखने की सलाह दें। \n \n Based on the assessment, the probability of not having breast cancer is estimated to be {prob_0}%. \n Message - There is no potential risk of breast cancer for this patient. Please councel the patient to continue with regular follow-ups as usual."

    
    response = jsonify({"prediction": s})
    print(response.json) 
    
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    
    return response


def process_and_predict(tag):
    fname = os.path.join(FEATURE_DIR2, f"{tag}.csv")
    df = pd.read_csv(fname)
    
    features =  [
        'AGE',
        'AGE_FIRST CHILD BIRTH',
        'CONTRACEPTIVE_DURATION_MNTHS',
        'PHYSICAL ACTIVITY_DURATION_MINS',
        'HEIGHT (IN CMS)',
        'EDUCATION',
        'OCCUPATION',
        'FAMILY TYPE',
        'REG_MENSTRUATION_History',
        'MENSTRUAL_STATUS',
        'HOT FLUSHES',
        'CONCEPTION(NATURALLY CONCEIVE/IVF)',
        'HRT',
        'FAMILYHO_CANCER',
        'FAMILYHO_MEMBER_TYPE',
        'RTI/STI',
        'FASTING',
        'MUSTARD OIL',
        'BREAST TRAUMA',
        'RADIATION_SITE_CHEST'
    ]
    
    numerical_cols = [
        "AGE",
        "AGE_FIRST CHILD BIRTH",
        "CONTRACEPTIVE_DURATION_MNTHS",
        "PHYSICAL ACTIVITY_DURATION_MINS",
        "HEIGHT (IN CMS)"
    ]

    scaled_val = preprocessor.transform(df)
    df = [j for elem in scaled_val for j in elem]
    df = dict(zip(features, df))
    df = pd.DataFrame(df, index=[0])

    input_df = df.rename(columns={
        'AGE': 'num__AGE', 
        'AGE_FIRST CHILD BIRTH':'num__AGE_FIRST CHILD BIRTH',
        'CONTRACEPTIVE_DURATION_MNTHS':'num__CONTRACEPTIVE_DURATION_MNTHS',
        'PHYSICAL ACTIVITY_DURATION_MINS':'num__PHYSICAL ACTIVITY_DURATION_MINS',
        'HEIGHT (IN CMS)':'num__HEIGHT (IN CMS)',
        'EDUCATION':'cat__EDUCATION',
        'OCCUPATION':'cat__OCCUPATION',
        'FAMILY TYPE':'cat__FAMILY TYPE',
        'REG_MENSTRUATION_History':'cat__REG_MENSTRUATION_History',
        'MENSTRUAL_STATUS':'cat__MENSTRUAL_STATUS',
        'HOT FLUSHES':'cat__HOT FLUSHES',
        'CONCEPTION(NATURALLY CONCEIVE/IVF)':'cat__CONCEPTION(NATURALLY CONCEIVE/IVF)',
        'HRT':'cat__HRT',
        'FAMILYHO_CANCER':'cat__FAMILYHO_CANCER',
        'FAMILYHO_MEMBER_TYPE':'cat__FAMILYHO_MEMBER_TYPE',
        'RTI/STI':'cat__RTI/STI',
        'FASTING':'cat__FASTING',
        'MUSTARD OIL':'cat__MUSTARD OIL',
        'BREAST TRAUMA':'cat__BREAST TRAUMA',
        'RADIATION_SITE_CHEST':'cat__RADIATION_SITE_CHEST'
    })

    # Make predictions using the loaded model
    prediction = model.predict(input_df)
    probability_scores = model.predict_proba(input_df)
    probability_scores = [j for elem in probability_scores for j in elem]
    for i in range(len(probability_scores)):
        if i == 0:
            prob_0 = probability_scores[i]
            prob_0 = round((prob_0 * 100), 2)
        else:
            prob_1 = probability_scores[i]
            prob_1 = round((prob_1 * 100), 2)

    print('Model predictions', prob_0, prob_1)

    return prediction, prob_0, prob_1


def generate_request_id():
    # Get the current date and time
    now = datetime.now()
    # Format it as "yyyy-mm-dd-hh-mm-ss"
    request_id = now.strftime("%Y-%m-%d-%H-%M-%S")
    return request_id


def process_audio(audiofile, tag):
    # To show - hindi text, english text, feature_extracted (maybe)
    # What to save on android - CSV.
    global TRANSCRIPT
    global TRANSLATION

    hindi_text = transcribe(os.path.abspath(audiofile))
    with open(os.path.join(TRANSCRIPT_DIR, f"{tag}.txt"), 'w') as fp:
        fp.write(hindi_text)
    print(f'{tag} Transcription completed...')
    TRANSCRIPT = hindi_text

    eng_text = translate(hindi_text)
    with open(os.path.join(TRANSLATION_DIR, f"{tag}.txt"), 'w') as fp:
        fp.write(eng_text)
    print(f'{tag} Translation completed...')
    TRANSLATION = eng_text

    _, feats = extract_features(eng_text)
    tdf = pd.DataFrame([feats])
    tdf.to_csv(os.path.join(FEATURE_DIR, f'{tag}.csv'), index=False)
    print(f'{tag} feature extraction completed...')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
