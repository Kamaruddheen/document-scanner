from matplotlib import pyplot as plt
from dotenv import load_dotenv
import numpy as np
import pytesseract
import cv2
import os

load_dotenv()

# Set path to tesseract executable 
pytesseract.pytesseract.tesseract_cmd = r'' + os.environ.get("TESSERACT_LOC")


# Helper function to display OpenCV image with title
def plt_imshow(title, image):
	# Convert OpenCV BGR image to matplotlib RGB format
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	plt.imshow(image)
	plt.title(title)
	plt.grid(False)
	plt.show()


# Preprocess image and find contours
def find_contours(image):    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    
    # Otsu's thresholding
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    # Dilate to combine text contours
    kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
    dilate = cv2.dilate(thresh, kernal, iterations=5)

    # Finding the max border lines
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])

    # Get bounding box coordinates
    lx, ly, lxw, lyh = [], [], [], []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)        
        lx.append(x)
        ly.append(y)
        lxw.append(x+w)
        lyh.append(y+h)

    # Finding the four points to find the text area
    x = min([n for n in lx if n>0], default=0)
    y = min([n for n in ly if n>0], default=0)
    xw = max(n for n in lxw if n>0)
    yh = max(n for n in lyh if n>0)

    return (x, y, xw, yh)


# Extract text from ROI using Pytesseract OCR 
def find_text_with_ocr(image, x, y, xw, yh):
    results  = []

    # Extract ROI
    roi = image[y:yh, x:xw]
    cv2.rectangle(image, (x, y), (xw, yh), (36, 255, 12), 5)

    # OCR using Pytesseract
    ocr_result = pytesseract.image_to_string(roi)

    # print(ocr_result)

    # Split text into lines
    ocr_arr_result = ocr_result.split("\n")

    for item in ocr_arr_result:        
        results.append(item)

    return results, ocr_result


# Save structured text in Excel file
def create_excel(text):
    import xlsxwriter
    
    # Create a new Excel workbook
    workbook = xlsxwriter.Workbook('excel.xlsx')    
    
    # Add a new worksheet to the workbook
    sheet1 = workbook.add_worksheet(name="Scanned")
    
    # Write the extracted text into the worksheet  
    # Starts at cell A1, writes each element of the text list in a column
    sheet1.write_column(0, 0, text)

    # Close the workbook to save the file
    workbook.close()


def execute(title, input_file):
    # Read image from input file
    nparr = np.fromstring(input_file.read(), np.uint8) 
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Find contours and ROI
    (x, y, xw, yh) = find_contours(image)

    # Extract text using OCR
    image_to_text = find_text_with_ocr(image, x, y, xw, yh)    
    array, text = image_to_text

    # Save to Excel
    create_excel(array)

    return text
    # return "Successful"


# plt_imshow("Input", image)
# cv2.imwrite("temp/index_gray.png", gray)
# cv2.imwrite("temp/index_blur.png", blur)
# cv2.imwrite("temp/index_thresh.png", thresh)
# cv2.imwrite("temp/index_kernal.png", kernal)
# cv2.imwrite("temp/index_dilate.png", dilate)
# cv2.imwrite("temp/index_bbox_new.png", image)
# plt_imshow("Final Image", image[y:yh, x:xw])