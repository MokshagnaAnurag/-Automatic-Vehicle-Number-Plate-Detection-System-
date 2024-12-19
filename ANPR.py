import cv2
import pytesseract
import random
states = ["AP", "KA", "TN", "MH", "DL", "RJ", "HR", "WB", "UP", "GJ"]
city_codes = ["01", "05", "10", "12", "14", "26", "20", "32", "01", "31"]
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
def generate_number_plate():
    state = random.choice(states)
    city_code = random.choice(city_codes)
    code = ''.join(random.choices(letters, k=2))
    number = ''.join(random.choices(numbers, k=4))
    return f"{state}{city_code}{code}{number}"

data = [generate_number_plate() for _ in range(2000)]

def extract_number_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    custom_config = r'--oem 3 --psm 6 outputbase digits'
    number_plate_text = pytesseract.image_to_string(threshold, config=custom_config)

    return number_plate_text.strip()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detected_text = extract_number_plate(frame)
  
    if detected_text in data:
        label = "Valid"
        color = (0, 255, 0)  
    else:
        label = "Not Valid"
        color = (0, 0, 255)  
    

    cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    cv2.imshow('Number Plate Recognition', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
