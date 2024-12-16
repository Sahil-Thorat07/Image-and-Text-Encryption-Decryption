import tkinter
from tkinter import *
import tkinter.messagebox as mbox
from tkinter import filedialog, simpledialog
from PIL import ImageTk, Image
import cv2
import os
import numpy as np
import random
import string

# created main window
window = Tk()
window.geometry("1200x700")
window.title("Image and Text Encryption Decryption")
window.configure(bg='black')

# Defined variables
global count, emig, frp, tname, con, bright, panelB, panelA, image_encrypted, key
frp = []
tname = []
con = 1
bright = 0
panelB = None
panelA = None

# Functions for path, folder, filename extraction, image handling, encryption, and decryption
def getpath(path):
    a = path.split(r'/')
    fname = a[-1]
    l = len(fname)
    location = path[:-l]
    return location

def getfoldername(path):
    a = path.split(r'/')
    name = a[-1]
    return name

def getfilename(path):
    a = path.split(r'/')
    fname = a[-1]
    a = fname.split('.')
    a = a[0]
    return a

def openfilename():
    filename = filedialog.askopenfilename(title='Open')
    return filename

def open_img():
    global x, panelA, panelB, count, eimg, location, filename
    count = 0
    x = openfilename()
    img = Image.open(x)
    eimg = img
    img = ImageTk.PhotoImage(img)
    temp = x
    location = getpath(temp)
    filename = getfilename(temp)
    if panelA is None or panelB is None:
        panelA = Label(image=img, bg='black')
        panelA.image = img
        panelA.pack(side="left", padx=10, pady=10)
        panelB = Label(image=img)
        panelB.image = img
        panelB.pack(side="right", padx=10, pady=10)
    else:
        panelA.configure(image=img)
        panelB.configure(image=img)
        panelA.image = img
        panelB.image = img

def en_fun():
    global x, image_encrypted, key
    image_input = cv2.imread(x, 0)
    (x1, y) = image_input.shape
    image_input = image_input.astype(float) / 255.0
    mu, sigma = 0, 0.1
    key = np.random.normal(mu, sigma, (x1, y)) + np.finfo(float).eps
    image_encrypted = image_input / key
    cv2.imwrite('image_encrypted.jpg', image_encrypted * 255)  # Save the encrypted image
    imge = Image.open('image_encrypted.jpg')
    imge = ImageTk.PhotoImage(imge)
    panelB.configure(image=imge)
    panelB.image = imge
    mbox.showinfo("Encrypt Status", "Image Encrypted successfully.")

def de_fun():
    global image_encrypted, key
    # Ensure the image is decrypted correctly
    image_output = image_encrypted * key
    image_output *= 255.0
    # Ask the user for the location to save the decrypted image
    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
    if save_path:
        cv2.imwrite(save_path, image_output)  # Save the decrypted image in the chosen path
        imgd = Image.open(save_path)
        imgd = ImageTk.PhotoImage(imgd)
        panelB.configure(image=imgd)
        panelB.image = imgd
        mbox.showinfo("Decrypt Status", "Image decrypted successfully and saved.")

def reset():
    global x, eimg, count, o6
    image = cv2.imread(x)[:, :, ::-1]
    count = 6
    o6 = image
    image = Image.fromarray(o6)
    eimg = image
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image
    mbox.showinfo("Success", "Image reset to original format!")

def save_img():
    global image_encrypted  # Use the encrypted image to save
    if image_encrypted is not None:
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if filename:
            image_to_save = Image.fromarray((image_encrypted * 255).astype(np.uint8))  # Convert back to 0-255 range
            image_to_save.save(filename)
            mbox.showinfo("Success", "Encrypted Image Saved Successfully!")
    else:
        mbox.showerror("Error", "No encrypted image to save.")

def exit_win():
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

# Text Encryption and Decryption functions

def caesar_encrypt(plain_text, shift=3):
    result = ""
    for char in plain_text:
        if char.isalpha():
            shift_amount = 65 if char.isupper() else 97
            result += chr((ord(char) + shift - shift_amount) % 26 + shift_amount)
        else:
            result += char
    return result

def caesar_decrypt(cipher_text, shift=3):
    result = ""
    for char in cipher_text:
        if char.isalpha():
            shift_amount = 65 if char.isupper() else 97
            result += chr((ord(char) - shift - shift_amount) % 26 + shift_amount)
        else:
            result += char
    return result

def encrypt_text():
    plain_text = simpledialog.askstring("Input", "Enter Plain Text to Encrypt:")
    if plain_text:
        cipher_text = caesar_encrypt(plain_text)
        mbox.showinfo("Encrypted Text", f"Encrypted Text: {cipher_text}")
        return cipher_text
    else:
        mbox.showerror("Error", "No text entered.")

def decrypt_text():
    cipher_text = simpledialog.askstring("Input", "Enter Cipher Text to Decrypt:")
    if cipher_text:
        plain_text = caesar_decrypt(cipher_text)
        mbox.showinfo("Decrypted Text", f"Decrypted Text: {plain_text}")
        return plain_text
    else:
        mbox.showerror("Error", "No text entered.")

# UI elements
start1 = Label(text="Image and Text Encryption\nDecryption", font=("roboto", 30), bg="red", fg="black")
start1.place(x=300, y=10)

chooseb = Button(window, text="Choose", command=open_img, font=("Arial", 20), bg="orange", fg="black", borderwidth=3, relief="raised")
chooseb.place(x=30, y=20)

saveb = Button(window, text="Save", command=save_img, font=("Arial", 20), bg="green", fg="black", borderwidth=3, relief="raised")
saveb.place(x=170, y=20)

enb = Button(window, text="Encrypt", command=en_fun, font=("Arial", 20), bg="light green", fg="black", borderwidth=3, relief="raised")
enb.place(x=150, y=620)

deb = Button(window, text="Decrypt", command=de_fun, font=("Arial", 20), bg="orange", fg="black", borderwidth=3, relief="raised")
deb.place(x=450, y=620)

resetb = Button(window, text="Reset", command=reset, font=("Arial", 20), bg="yellow", fg="black", borderwidth=3, relief="raised")
resetb.place(x=800, y=620)

exitb = Button(window, text="EXIT", command=exit_win, font=("Arial", 20), bg="red", fg="black", borderwidth=3, relief="raised")
exitb.place(x=880, y=20)

encrypt_text_button = Button(window, text="Encrypt Text", command=encrypt_text, font=("Arial", 20), bg="light blue", fg="black", borderwidth=3, relief="raised")
encrypt_text_button.place(x=350, y=150)  # Moved the "Encrypt Text" button lower

decrypt_text_button = Button(window, text="Decrypt Text", command=decrypt_text, font=("Arial", 20), bg="light blue", fg="black", borderwidth=3, relief="raised")
decrypt_text_button.place(x=550, y=150)  # Moved the "Decrypt Text" button lower

window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()
