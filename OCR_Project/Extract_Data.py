import os
import pytesseract
import re
import pandas as pd

class ExtractPrescriptionData:
    def __init__(self, pytesseract_path, folder_path):
        print("init method of ExtractPrescriptionData".center(50, "-"))
        self.pytesseract_path = pytesseract_path
        self.folder_path = folder_path
        self.text_folder_name = "Extracted_Prescription_Text"
        pytesseract.pytesseract.tesseract_cmd = self.pytesseract_path

    def get_extract_text(self):
        self.text_lst = []
        if not os.path.exists(self.text_folder_name):
            os.mkdir(self.text_folder_name)

        self.image_names_lst = os.listdir(self.folder_path)
        for name in self.image_names_lst:
            image_path = os.path.join(self.folder_path, name)
            text = pytesseract.image_to_string(image_path)
            file_name = os.path.join(self.text_folder_name, name.split(".")[0] + ".txt")
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(text)

class GetPrescriptionDetails(ExtractPrescriptionData):
    def __init__(self, pytesseract_path, folder_path):
        print("init  method of GetPrescriptionDetails".center(50, "-"))
        super().__init__(pytesseract_path, folder_path)

    def get_prescription_no(self):
        pre_no_match = re.search(r"\bRX[\d]+\b", self.text)
        return pre_no_match.group() if pre_no_match else "None"

    def get_patient_name(self):
        patient_name_match = re.search(r"(?<=Patient\sName:)\s*[\w\s]+(?=[\n])", self.text)
        return patient_name_match.group().strip() if patient_name_match else "None"
    
    def get_patient_age(self):
        patient_age_match = re.search(r"(?<=Age:)\s*[\w\s]+(?=[\n])", self.text)
        return patient_age_match.group().strip() if patient_age_match else "None"
    
    def get_pre_date(self):
        patient_age_match = re.search(r"[\d]{1,2}-[a-zA-Z]{1,10}-[\d]{2,4}", self.text)
        return patient_age_match.group().strip() if patient_age_match else "None"
    
    def get_doc_name(self):
        doc_name_match = re.search(r"\bDr.[\s\w]+\n",self.text)
        return doc_name_match.group().strip() if doc_name_match else "None"
    
    def get_medicine(self):
        medicine_match = re.findall(r"(?<=\n)[\w\s]+(?=-[\s]?[\d]{1,2}\s)",self.text)
        medicine_match=[medicine_match[i].replace("\n","") for i in range(len(medicine_match))]
        return medicine_match if medicine_match else "None"

    def get_prescription_data(self):
        self.pre_no_lst = []
        self.patient_name_lst = []
        self.patient_age_lst=[]
        self.pre_date_lst=[]
        self.doc_name_lst=[]
        self.pre_medicine_lst=[]

        # Make sure text was extracted first
        self.get_extract_text()

        text_file_lst = os.listdir(self.text_folder_name)
        for name in text_file_lst:
            file_path = os.path.join(self.text_folder_name, name)
            with open(file_path, "r", encoding="utf-8") as file:
                self.text = file.read()
                self.pre_no_lst.append(self.get_prescription_no())
                self.patient_name_lst.append(self.get_patient_name())
                self.patient_age_lst.append(self.get_patient_age())
                self.pre_date_lst.append(self.get_pre_date())
                self.doc_name_lst.append(self.get_doc_name())
                self.pre_medicine_lst.append(self.get_medicine())

        pre_data = {
            "Prescription No": self.pre_no_lst,
            "Patient Name": self.patient_name_lst,
            "Patient Age": self.patient_age_lst,
            "Prescription Date": self.pre_date_lst,
            "Doctor Name":self.doc_name_lst,
            "Medicine":self.pre_medicine_lst
        }
        
        df=pd.DataFrame(pre_data)
        df.to_csv("Extracted_Prescription_Details.csv",index=False)


if __name__ == "__main__":
    pytesseract_path = r"C:\Users\hp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    folder_path = r"D:\Academic\Velocity\Data_Sets\OCR_Prescription_DataSet\Prescription_Printed_Images"
    
    obj = GetPrescriptionDetails(pytesseract_path, folder_path)
    obj.get_prescription_data()
