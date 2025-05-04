from OCR_Project.Extract_Data import GetPrescriptionDetails
import config

if __name__=="__main__":
    obj=GetPrescriptionDetails(config.pytesseract_path,config.folder_path)
    obj.get_prescription_data()