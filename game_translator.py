import numpy as np
import cv2
import pyautogui
from PIL import Image
from pytesseract import pytesseract
from googletrans import Translator
import time

path_to_tesseract = r"D:\Tesseract\tesseract.exe"
extract_language = r"--oem 3 --psm 6 -l eng"
translate_language = "zh-CN"

previous_text = ""

def translate(text):
    translator = Translator()
    translation = translator.translate(text, dest=translate_language)
    return translation.text

def screen_shot(left=0, top=0, width=1920, height=1080):
    image = pyautogui.screenshot(region=(left, top, width, height))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return image

def extract_word(img):
    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(img, config=extract_language)
    return text.strip()

input("Move the mouse to the top-left corner of the translated area and press Enter")
top_left = pyautogui.position()

input("Move the mouse to the bottom-right corner of the translated area and press Enter")
bottom_right = pyautogui.position()

try:
    while True:
        start_time = time.time()

        image = screen_shot(top_left[0], top_left[1], bottom_right[0]-top_left[0], bottom_right[1]-top_left[1])

        text = extract_word(Image.fromarray(image))

        if text and text != previous_text:
            print(f"Original: {text}")
            translation = translate(text)
            print(f"Translated: {translation}\n")
            previous_text = text

        elapsed_time = time.time() - start_time
        delay = max(0, 1.0/30 - elapsed_time)
        time.sleep(delay)
except KeyboardInterrupt:
    print("Translation stopped.")