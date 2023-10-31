import cv2
import pytesseract

# Initialize the camera (usually, 0 represents the built-in camera, and 1 represents an external camera)
cap = cv2.VideoCapture(0)  # Adjust the parameter as needed for your camera source.

# Set up the Tesseract configuration
tess_config = '--psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Cannot read video feed")
        break

    # Preprocess the frame (e.g., grayscale conversion, noise reduction)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Number plate detection (use your detection method)
    # Define plate_roi based on your detection logic.
    # For example, you might use contour detection to identify the plate and set plate_roi.
    
    # Ensure that plate_roi is defined based on your detection logic
    # For example:
    # plate_roi = detect_number_plate(gray)  # Replace 'detect_number_plate' with your detection method

    # Once you have the plate_roi, use Tesseract for OCR
    if plate_roi is not None:
        plate_text = pytesseract.image_to_string(plate_roi, lang='eng', config=tess_config)

        # Display the recognized text on the frame
        cv2.putText(frame, f'Number Plate: {plate_text}', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('Car Number Plate Detection', frame)

    # Exit the loop and close the window when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
