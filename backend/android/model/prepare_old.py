import pandas as pd
import sys
import pickle
#from sklearn.preprocessing import MinMaxScaler

name=sys.argv[1]
csvPath="/home/prasoon/breast_cancer_project/trial1/featureExtraction/csvFiles/"+name+"_data.csv"
df=pd.read_csv(csvPath)
with open('scale.pkl', 'rb') as file:
    scale = pickle.load(file)
numerical_columns = [ 'WEIGHT (IN KGS)','HEIGHT (IN CMS)','BMI', 'WAIST_CMS','RBS','WHR', 'SBP']
categorical_columns = [col for col in df.columns if col not in numerical_columns]
catgeorical_cols = ['CAUSE_MENOPAUSE_HORMONAL TREATMENT',
       'CAUSE_MENOPAUSE_HYSTERECTOMY', 'CAUSE_MENOPAUSE_NATURAL',
       'CAUSE_MENOPAUSE_NR', 'PAST_SURGERY_NR', 'PAST_SURGERY_YES',
       'STERILISATION (B/L TUBAL LIGATION)_YES',
       'NON-VEG_FREQUENCY_FORTNIGHTLY', 'NON-VEG_FREQUENCY_HALF YEARLY',
       'NON-VEG_FREQUENCY_MONTHLY', 'NON-VEG_FREQUENCY_NR',
       'NON-VEG_FREQUENCY_QUARTERLY', 'NON-VEG_FREQUENCY_THRICE WEEKLY',
       'NON-VEG_FREQUENCY_TWICE WEEKLY', 'NON-VEG_FREQUENCY_WEEKLY',
       'NON-VEG_FREQUENCY_YEARLY', 'EDUCATION_ILLITERATE',
       'EDUCATION_INTERMEDIATE', 'EDUCATION_NR', 'EDUCATION_POST GRADUATE',
       'EDUCATION_PRIMARY', 'EDUCATION_SECONDARY',
       'PHYSICAL ACTIVITY_GRADE_MODERATE', 'PHYSICAL ACTIVITY_GRADE_NIL',
       'PHYSICAL ACTIVITY_GRADE_NR', 'PHYSICAL ACTIVITY_GRADE_VIGROUS',
       'RESIDENCE_RURAL', 'RESIDENCE_URBAN', 'SES_Lower Middle', 'SES_Middle',
       'SES_Upper', 'SES_Upper Middle', 'WHO_BMI_CAT_0VERWEIGHT',
       'WHO_BMI_CAT_NORMAL', 'WHO_BMI_CAT_NR', 'WHO_BMI_CAT_OBESE CLASS I',
       'WHO_BMI_CAT_OBESE CLASS II', 'WHO_BMI_CAT_OBESE CLASS III',
       'WHO_BMI_CAT_OVERWEIGHT', 'WHO_BMI_CAT_PRE OBESE',
       'WHO_BMI_CAT_UNDERWEIGHT', 'ABD_OBESITY_#VALUE!', 'ABD_OBESITY_NO',
       'ABD_OBESITY_YES', 'DIAGNOSIS_Notdone']
col_to_drop=['Unnamed: 0',
 'CAUSE_MENOPAUSE_CHEMO-INDUCED',
 'PAST_SURGERY_NO',
 'STERILISATION (B/L TUBAL LIGATION)_NO',
 'NON-VEG_FREQUENCY_DAILY',
 'EDUCATION_GRADUATE',
 'EDUCATION_SECONDARY SCHOOL',
 'PHYSICAL ACTIVITY_GRADE_MILD',
 'RESIDENCE_NR',
 'SES_Lower',
 'WHO_BMI_CAT_0BESE CLASS I',
 'ABD_OBESITY_#DIV/0!',
 'DIAGNOSIS_CA BREAST',
 "STERILISATION (B/L TUBAL LIGATION)_NR"]
all_cols=['WEIGHT (IN KGS)','HEIGHT (IN CMS)','BMI', 'WAIST_CMS','RBS','WHR', 'SBP','CAUSE_MENOPAUSE_HORMONAL TREATMENT',
       'CAUSE_MENOPAUSE_HYSTERECTOMY', 'CAUSE_MENOPAUSE_NATURAL',
       'CAUSE_MENOPAUSE_NR', 'PAST_SURGERY_NR', 'PAST_SURGERY_YES',
       'STERILISATION (B/L TUBAL LIGATION)_YES',
       'NON-VEG_FREQUENCY_FORTNIGHTLY', 'NON-VEG_FREQUENCY_HALF YEARLY',
       'NON-VEG_FREQUENCY_MONTHLY', 'NON-VEG_FREQUENCY_NR',
       'NON-VEG_FREQUENCY_QUARTERLY', 'NON-VEG_FREQUENCY_THRICE WEEKLY',
       'NON-VEG_FREQUENCY_TWICE WEEKLY', 'NON-VEG_FREQUENCY_WEEKLY',
       'NON-VEG_FREQUENCY_YEARLY', 'EDUCATION_ILLITERATE',
       'EDUCATION_INTERMEDIATE', 'EDUCATION_NR', 'EDUCATION_POST GRADUATE',
       'EDUCATION_PRIMARY', 'EDUCATION_SECONDARY',
       'PHYSICAL ACTIVITY_GRADE_MODERATE', 'PHYSICAL ACTIVITY_GRADE_NIL',
       'PHYSICAL ACTIVITY_GRADE_NR', 'PHYSICAL ACTIVITY_GRADE_VIGROUS',
       'RESIDENCE_RURAL', 'RESIDENCE_URBAN', 'SES_Lower Middle', 'SES_Middle',
       'SES_Upper', 'SES_Upper Middle', 'WHO_BMI_CAT_0VERWEIGHT',
       'WHO_BMI_CAT_NORMAL', 'WHO_BMI_CAT_NR', 'WHO_BMI_CAT_OBESE CLASS I',
       'WHO_BMI_CAT_OBESE CLASS II', 'WHO_BMI_CAT_OBESE CLASS III',
       'WHO_BMI_CAT_OVERWEIGHT', 'WHO_BMI_CAT_PRE OBESE',
       'WHO_BMI_CAT_UNDERWEIGHT', 'ABD_OBESITY_#VALUE!', 'ABD_OBESITY_NO',
       'ABD_OBESITY_YES']

numerical_df = df[numerical_columns]
categorical_df = df[categorical_columns]
scaled_val = scale.transform(numerical_df)
numerical_df_median_scaled = pd.DataFrame(scaled_val, columns=numerical_df.columns)

"""cat_df_encoded = pd.get_dummies(categorical_df,drop_first=False).astype(int)
default_value = 0
new_data_entry_dict = {column: default_value for column in catgeorical_cols}
cat_df_encoded_dict=cat_df_encoded.to_dict("records")[0]
cat_data_dict=new_data_entry_dict|cat_df_encoded_dict
new_cat_df=pd.DataFrame([cat_data_dict])"""
new_Df= pd.concat([numerical_df_median_scaled, categorical_df], axis=1)

for col in col_to_drop:
    if col in new_Df.columns:
        new_Df.drop(columns=[col],inplace=True)
        
#if "Unnamed:0" in new_Df.columns:
#    new_Df.drop(columns=["Unnamed:0"],inplace=True)

#name=sys.argv[2]
dff=new_Df[all_cols]
dff.to_csv("/home/prasoon/breast_cancer_project/trial1/featureExtraction/updatedCsvFiles/"+name+"_updated.csv",index=False)

"""with open('model.pkl', 'rb') as file:
    model = pickle.load(file)
#df=pd.read_csv("../updatedCsvFiles/"+name+"_updated.csv
#x=new_Df.drop(columns=["DIAGNOSIS_Notdone"])
        #y=df["DIAGNOSIS_Notdone"]

y_pred=model.predict(dff)
if y_pred[0]==0:
    print("yes")
else:
    print("no")"""