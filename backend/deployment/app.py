import os
from feature_extraction import featEx

def featureExtraction(name):
    csvPath = os.path.join('csvFiles', f"{name}_data.csv")

    obj = featEx(name)
    obj.extractFeatures()

    return csvPath

if __name__ == '__main__':
    featureExtraction('audio_1723623102704')
