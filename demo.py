import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import sys
def perform_ocr(pdf_file):
    images = convert_from_path(pdf_file)
    ocr_text = ""
    
    for page_num, image in enumerate(images, start=1):
        text = pytesseract.image_to_string(image)
        ocr_text += text

    return ocr_text

# Function to search for a word in the extracted text and print the result
def search_word(ocr_text, search_query):
    lines = ocr_text.split('\n')
    
    for line in lines:
        if search_query in line:
            idx = line.find(search_query)
            # print(f"Found '{search_query}' in line: {line}")
            print(f"Text after '{search_query}': {line[idx + len(search_query):].strip()}")
            return
        
    print(f"'{search_query}' not found in the document.")

def main():
    pdf_file = input("Enter the path to the PDF file: ")
    ocr_text = perform_ocr(pdf_file)
    print("OCR completed successfully.")
    
    while True:
        search_query = input("Enter the word you want to search for: ")

        search_word(ocr_text, search_query)


        choice = input("Do you want to search more? (1: Yes, 2: Exit): ")
        
        if choice == '2':
            print("Exiting the program.")
            break
        elif choice != '1':
            print("Invalid choice. Exiting the program.")
            break

if __name__ == "__main__":
    main()
