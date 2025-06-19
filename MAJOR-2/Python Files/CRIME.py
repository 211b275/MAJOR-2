import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

file_url = r"D:\MAJOR-2\Python Files\crime_dataset_india.csv"

if not os.path.isfile(file_url):
    raise FileNotFoundError(f"The file at {file_url} was not found.")

df = pd.read_csv(file_url)
df.fillna("NULL", inplace=True)
columns_to_drop = ['Police Deployed', 'Case Closed', 'Date Case Closed']
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

crime_ipc_crpc_mapping = {
    "identity theft": ("IPC 419, IPC 420", "CRPC 154", "Up to 3 years and/or fine"),
    "homicide": ("IPC 302", "CRPC 174", "Life imprisonment or death"),
    "kidnapping": ("IPC 363", "CRPC 98", "Up to 7 years and fine"),
    "burglary": ("IPC 454, IPC 380", "CRPC 154", "Up to 10 years and fine"),
    "vandalism": ("IPC 427", "CRPC 107", "Up to 2 years or fine or both"),
    "assault": ("IPC 351", "CRPC 107", "Up to 3 months or fine or both"),
    "vehicle - stolen": ("IPC 379", "CRPC 102", "Up to 3 years and/or fine"),
    "counterfeiting": ("IPC 489A-D", "CRPC 154", "Up to life imprisonment and fine"),
    "extortion": ("IPC 384", "CRPC 155", "Up to 3 years and fine"),
    "public intoxication": ("IPC 510", "CRPC 151", "Fine up to Rs. 100 or imprisonment"),
    "fraud": ("IPC 420", "CRPC 154", "Up to 7 years and fine"),
    "sexual assault": ("IPC 354, IPC 376", "CRPC 154", "7 years to life imprisonment"),
    "drug offense": ("NDPS Act Sections", "CRPC 41", "Up to 20 years and fine"),
    "arson": ("IPC 435, IPC 436", "CRPC 154", "Up to life imprisonment"),
    "cybercrime": ("IT Act Sections, IPC 66", "CRPC 154", "Up to 3 years and/or fine"),
    "traffic violation": ("MV Act 1988 Sections", "CRPC 133", "Fine up to Rs. 5000"),
    "shoplifting": ("IPC 379", "CRPC 154", "Up to 3 years and/or fine"),
    "illegal possession": ("Arms Act Section 25", "CRPC 154", "Up to 3 years and/or fine"),
    "firearm offense": ("Arms Act Section 25", "CRPC 154", "Up to 7 years and/or fine"),
    "robbery": ("IPC 392", "CRPC 154", "Up to 10 years and fine")
}

def predict_severity(crime_description):
    if "murder" in crime_description or "homicide" in crime_description:
        return "Critical"
    elif "theft" in crime_description or "burglary" in crime_description:
        return "Major"
    elif "fraud" in crime_description or "assault" in crime_description:
        return "Minor"
    else:
        return "Unknown"

def predict_time_of_crime():
    import random
    times_of_day = ['Morning', 'Afternoon', 'Evening', 'Night']
    return random.choice(times_of_day)

root = tk.Tk()
root.title("Criminal Data Lookup")
root.attributes('-fullscreen', True)
root.configure(bg="#2C2C3C")

def search_crime():
    crime_code = entry_crime_code.get().strip()
    if not crime_code:
        messagebox.showwarning("Input Error", "Please enter a Crime Code!")
        return
    result = df[df['Crime Code'].astype(str) == crime_code]
    if result.empty:
        messagebox.showinfo("No Data", "No records found.")
    else:
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, result.to_string(index=False))

def predict():
    crime_code = entry_crime_code.get().strip()
    if not crime_code:
        messagebox.showwarning("Input Error", "Please enter a Crime Code for prediction!")
        return
    try:
        result = df[df['Crime Code'].astype(str) == crime_code]
        if result.empty:
            messagebox.showinfo("No Data", "No records found.")
            return
        crime_description = result.iloc[0]['Crime Description'].lower()
        crime_info = crime_ipc_crpc_mapping.get(crime_description)
        severity = predict_severity(crime_description)
        time_of_crime = predict_time_of_crime()
        if crime_info:
            ipc_section, crpc_section, punishment = crime_info
            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, f"Crime Description: {crime_description.capitalize()}\n\n")
            text_output.insert(tk.END, f"Severity: {severity}\n")
            text_output.insert(tk.END, f"Time of Crime Likely: {time_of_crime}\n")
            text_output.insert(tk.END, f"Relevant IPC Section(s): {ipc_section}\n")
            text_output.insert(tk.END, f"Relevant CRPC Section(s): {crpc_section}\n")
            text_output.insert(tk.END, f"Punishment: {punishment}\n")
        else:
            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, "IPC/CRPC information not found for this crime.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while predicting: {e}")

frame_input = tk.Frame(root, bg="#38385B", padx=30, pady=30)
frame_input.pack(pady=30)

label_code = tk.Label(frame_input, text="Crime No:", fg="white", bg="#38385B", font=("Roboto Slab", 20, "bold"))
label_code.pack(side=tk.LEFT, padx=20)

entry_crime_code = ttk.Entry(frame_input, font=("Palatino Linotype", 18), width=30)
entry_crime_code.pack(side=tk.LEFT, padx=10)

btn_search = tk.Button(frame_input, text="Search", fg="white", bg="#38385B", font=("Georgia", 17, "bold"), command=search_crime)
btn_search.pack(side=tk.LEFT, padx=10)

btn_predict = tk.Button(frame_input, text="Predict IPC/CRPC", fg="white", bg="#38385B", font=("Georgia", 17, "bold"), command=predict)
btn_predict.pack(side=tk.LEFT, padx=10)

text_output = tk.Text(root, font=("Courier", 10), bg="#1C1C2E", fg="white")
text_output.pack(expand=False, fill='x', padx=35, pady=35)

def exit_fullscreen(event=None):
    root.destroy()

root.bind("<Escape>", exit_fullscreen)
root.mainloop()
