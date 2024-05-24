import os
import datetime
import win32com.client
import time

# Define the base destination folder
base_destination_folder = r"\\10.10.3.23\\Recording"
#base_destination_folder = r"C:\\Users\\jitu\\Desktop\\test"

def extract_date_from_filename(filename):
    try:
        date_substring = filename[:8]
        
        date_ddmmyyyy = datetime.datetime.strptime(date_substring, '%d%m%Y').date()
        return date_ddmmyyyy.strftime('%Y/%b %Y/%d%m%Y')
    except ValueError:
        pass
    
    try:
        date_yyyymmdd = datetime.datetime.strptime(date_substring, '%Y%m%d').date()
        return date_yyyymmdd.strftime('%Y/%b %Y/%d%m%Y')
    except ValueError:
        return None

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
today_folder_path = os.path.join(base_destination_folder, today.strftime("%Y"), today.strftime("%b %Y"), today.strftime("%d%m%Y"))
if not os.path.exists(today_folder_path):
    os.makedirs(today_folder_path)

subject_prefixes = ("CALL", "Call", "CALLS", "Calls", "call", "calls", "recording", "recordings", "Recording", "RECORDING", "Recordings", "RECORDINGS", "FW: CALL")
reports = [msg for msg in inbox.Items if any(msg.Subject.upper().startswith(prefix) for prefix in subject_prefixes) and msg.ReceivedTime.date() == today]

inbox.Display()
outlook.SendAndReceive(True)
time.sleep(60)

for message in reports:
    sender_email = message.SenderEmailAddress
    sender_name = sender_email.split('@')[0]
    formatted_sender_name = sender_name.capitalize()
    
    for attachment in message.Attachments:
        if attachment.FileName.startswith('attachment_date'):
            attachment_path = os.path.join(today_folder_path, attachment.FileName)
            if not os.path.exists(attachment_path):
                attachment.SaveAsFile(attachment_path)
                print(f"Saved {attachment.FileName} to {attachment_path}")
            else:
                print(f"File {attachment.FileName} already exists. Skipping.")
        else:
            attachment_date = extract_date_from_filename(attachment.FileName)
            if attachment_date:
                destination_path = os.path.join(base_destination_folder, attachment_date, formatted_sender_name)
                if not os.path.exists(destination_path):
                    os.makedirs(destination_path)
                
                attachment_path = os.path.join(destination_path, attachment.FileName)
                if not os.path.exists(attachment_path):
                    attachment.SaveAsFile(attachment_path)
                    print(f"Saved {attachment.FileName} to {attachment_path}")
                else:
                    print(f"File {attachment.FileName} already exists. Skipping.")
            else:
                print(f"Skipping {attachment.FileName} due to unrecognized date format")

time.sleep(5)
os.system('taskkill /im outlook.exe /f')
