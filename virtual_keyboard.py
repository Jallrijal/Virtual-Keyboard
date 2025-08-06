import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller
 
# Buka kamera dengan resolusi yang dapat disesuaikan
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Lebar
cap.set(4, 720)  # Tinggi

# Periksa apakah kamera berhasil dibuka
if not cap.isOpened():
    print("Error: Tidak dapat membuka kamera!")
    exit()

print("Camera opened successfully!")
 
detector = HandDetector(detectionCon=0.8, maxHands=1)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/" , "<"]]
finalText = ""
 
keyboard = Controller()
 
 
def drawAll(img, buttonList, img_width, img_height):
    # Skala responsif berdasarkan ukuran gambar
    scale_factor = min(img_width / 1280, img_height / 720)
    
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        
        # Skala posisi dan ukuran tombol
        scaled_x = int(x * scale_factor)
        scaled_y = int(y * scale_factor)
        scaled_w = int(w * scale_factor)
        scaled_h = int(h * scale_factor)
        
        cvzone.cornerRect(img, (scaled_x, scaled_y, scaled_w, scaled_h),
                          20, rt=0)
        cv2.rectangle(img, (scaled_x, scaled_y), (scaled_x + scaled_w, scaled_y + scaled_h), (255, 0, 255), cv2.FILLED)
        
        # Skala ukuran font
        font_scale = max(0.5, 1.5 * scale_factor)
        font_thickness = max(1, int(2 * scale_factor))
        
        cv2.putText(img, button.text, (scaled_x + int(15 * scale_factor), scaled_y + int(35 * scale_factor)),
                    cv2.FONT_HERSHEY_PLAIN, font_scale, (255, 255, 255), font_thickness)
        
        # Debug: Tampilkan koordinat setiap tombol
        cv2.putText(img, f'({scaled_x},{scaled_y})', (scaled_x, scaled_y - 5), 
                   cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 255), 1)
    return img


class Button():
    def __init__(self, pos, text, size=[50, 50]):
        self.pos = pos
        self.size = size
        self.text = text
 
 
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([60 * j + 50, 60 * i + 50], key))

print("Virtual Keyboard Started!")
print("=== CARA PENGGUNAAN ===")
print("1. Arahkan JARI TENGAH ke tombol yang ingin ditekan")
print("2. Rapatkan JARI TELUNJUK dan JARI TENGAH untuk menekan tombol")
print("3. Tekan 'q' di keyboard fisik untuk keluar")
print("=======================")

try:
    while True:
        success, img = cap.read()
        
        # Periksa apakah frame berhasil dibaca
        if not success:
            print("Error: Tidak dapat membaca frame dari kamera!")
            break
            
        # Flip image untuk mirror effect (temporary disabled untuk debugging)
        # img = cv2.flip(img, 1)
        
        # Deteksi tangan
        hands, img = detector.findHands(img)
        
        # Dapatkan ukuran gambar
        img_height, img_width = img.shape[:2]
        img = drawAll(img, buttonList, img_width, img_height)
     
        if hands:
            # Ambil tangan pertama
            hand = hands[0]
            lmList = hand["lmList"]
            
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
                
                # Debug: Tampilkan tombol yang sedang diperiksa
                cv2.putText(img, f'Checking: {button.text}', (10, 90), 
                           cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2)
                
                # Skala posisi dan ukuran tombol untuk deteksi
                scale_factor = min(img_width / 1280, img_height / 720)
                scaled_x = int(x * scale_factor)
                scaled_y = int(y * scale_factor)
                scaled_w = int(w * scale_factor)
                scaled_h = int(h * scale_factor)
     
                # Debug: Tampilkan koordinat jari tengah dan tombol
                middle_finger_x, middle_finger_y = lmList[12][0], lmList[12][1]
                
                # Karena menggunakan mirror effect, koordinat X perlu disesuaikan
                # middle_finger_x = img_width - middle_finger_x  # Uncomment jika perlu
                
                # Tampilkan koordinat jari tengah di layar
                cv2.putText(img, f'Jari Tengah: ({middle_finger_x}, {middle_finger_y})', (10, 30), 
                           cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                
                if scaled_x < middle_finger_x < scaled_x + scaled_w and scaled_y < middle_finger_y < scaled_y + scaled_h:
                    # Debug: Tampilkan koordinat tombol yang terdeteksi
                    cv2.putText(img, f'Tombol: ({scaled_x}, {scaled_y}) - ({scaled_x + scaled_w}, {scaled_y + scaled_h})', (10, 60), 
                               cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
                    
                    cv2.rectangle(img, (scaled_x - 5, scaled_y - 5), (scaled_x + scaled_w + 5, scaled_y + scaled_h + 5), (175, 0, 175), cv2.FILLED)
                    
                    # Skala ukuran font
                    font_scale = max(0.5, 1.5 * scale_factor)
                    font_thickness = max(1, int(2 * scale_factor))
                    
                    cv2.putText(img, button.text, (scaled_x + int(15 * scale_factor), scaled_y + int(35 * scale_factor)),
                                cv2.FONT_HERSHEY_PLAIN, font_scale, (255, 255, 255), font_thickness)
                    
                    # Hitung jarak antara jari telunjuk dan jari tengah menggunakan numpy
                    try:
                        # Ambil koordinat jari telunjuk (8) dan jari tengah (12)
                        p1 = np.array([lmList[8][0], lmList[8][1]])  # Jari telunjuk
                        p2 = np.array([lmList[12][0], lmList[12][1]])  # Jari tengah
                        
                        # Hitung jarak Euclidean
                        length = np.linalg.norm(p1 - p2)
                        
                        # Gambar garis antara kedua jari
                        cv2.line(img, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (255, 0, 255), 3)
                        
                        # Tampilkan jarak
                        cv2.putText(img, f'{int(length)}', (int((p1[0] + p2[0])/2), int((p1[1] + p2[1])/2)), 
                                   cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
         
                        ## when clicked - rapatkan jari telunjuk dan jari tengah
                        if length < 35:  # Threshold yang lebih besar untuk kemudahan
                            keyboard.press(button.text)
                            cv2.rectangle(img, (scaled_x, scaled_y), (scaled_x + scaled_w, scaled_y + scaled_h), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, button.text, (scaled_x + int(15 * scale_factor), scaled_y + int(35 * scale_factor)),
                                        cv2.FONT_HERSHEY_PLAIN, font_scale, (255, 255, 255), font_thickness)
                            if button.text=='<':
                                if len(finalText)!=0:
                                    finalText=finalText[0:len(finalText)-1]
                            else:
                                finalText += button.text
                            sleep(0.5)
                    except Exception as e:
                        pass  # Abaikan error
     
        # Skala area teks responsif
        scale_factor = min(img_width / 1280, img_height / 720)
        text_area_x = int(50 * scale_factor)
        text_area_y = int(350 * scale_factor)
        text_area_w = int(650 * scale_factor)
        text_area_h = int(100 * scale_factor)
        
        cv2.rectangle(img, (text_area_x, text_area_y), (text_area_x + text_area_w, text_area_y + text_area_h), (175, 0, 175), cv2.FILLED)
        
        # Skala ukuran font untuk teks
        text_font_scale = max(1.0, 2.0 * scale_factor)
        text_font_thickness = max(2, int(3 * scale_factor))
        
        cv2.putText(img, finalText, (text_area_x + int(10 * scale_factor), text_area_y + int(80 * scale_factor)),
                    cv2.FONT_HERSHEY_PLAIN, text_font_scale, (255, 255, 255), text_font_thickness)
     
        cv2.imshow("Virtual Keyboard", img)
        
        # Tunggu key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nProgram interrupted by user")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Bersihkan
    cap.release()
    cv2.destroyAllWindows()
    print("Virtual Keyboard closed!") 