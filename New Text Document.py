import cv2
import pytesseract
import re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def send_email(subject, message):
    email_address = "minip2024@gmail.com"  # Your email address
    email_password = "taro hfcw qxwp ihan"         # Your email password
    smtp_server = "smtp.gmail.com"           # SMTP server (for Gmail)
    smtp_port = 587                         # SMTP port (for Gmail)
    rec_mail = "anushatippireddy17@gmail.com"

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, email_password)

        msg = MIMEMultipart()
        msg["From"] = email_address
        msg["To"] = rec_mail  # You can send the email to yourself
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        server.sendmail(email_address, rec_mail, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")

def detect_license_plate():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny_edge = cv2.Canny(gray_image, 170, 200)
        contours, new = cv2.findContours(canny_edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

        contour_with_license_plate = None
        license_plate = None
        x = None
        y = None
        w = None
        h = None

        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
            if len(approx) == 4:
                contour_with_license_plate = approx
                x, y, w, h = cv2.boundingRect(contour)
                license_plate = gray_image[y:y + h, x:x + w]
                break

        (thresh, license_plate) = cv2.threshold(license_plate, 127, 255, cv2.THRESH_BINARY)
        license_plate = cv2.bilateralFilter(license_plate, 11, 17, 17)
        (thresh, license_plate) = cv2.threshold(license_plate, 150, 180, cv2.THRESH_BINARY)

        text = pytesseract.image_to_string(license_plate)
        text = text.replace(" ", "").upper()

        if not text:
            text = "No license plate found"
        else:
            message="The number plate "+str(text)+" has detected to cross the signal light at NTR stadium. So penality for that was 1500/-"
            send_email(text, message)
        """if re.search("MH20EE7598", text):
            messagebox.showinfo("License Plate Detection", "License Plate: {}\nBoom!".format(text))
        elif re.search("MMH20EE7597", text):
            subject = "Lorry Number Plate Detected"
            message = f"Lorry Number Plate Detected: {text}"
            send_email(subject, message)
            messagebox.showinfo("License Plate Detection", "Lorry Number Plate Detected: {}\nEmail Sent.".format(text))
        else:"""
        
        messagebox.showinfo("License Plate Detection", "License Plate: {}".format(text))

        # Display the processed image with the detected license plate
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 3)
        cv2.putText(image, text, (x - 100, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("License Plate Detection", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Create the main GUI window
root = tk.Tk()
root.title("License Plate Detection")

# Create an H1 tag using a Label widget
header = tk.Label(root, text="License Plate Detection", font=("Helvetica", 20))
header.pack()

# Create a button to select an image
select_button = tk.Button(root, text="Select Image", command=detect_license_plate)
select_button.pack()

expected_text = "MH20EE7598"  # The expected license plate text

root.mainloop()
