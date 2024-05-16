import os
import datetime
import win32com.client
import zipfile

# Define the base destination folder
base_destination_folder = r"C:\\Users\\my\\local\\dest"
#base_destination_folder = r"\\10.10.3.23\\my_remote_dest"

# Function to extract date from filename
def extract_date_from_filename(filename):
    try:
        # Extract date substring from filename
        date_substring = filename[:8]  # Assuming the date is the first 8 characters
        
        # Attempt to parse the date from the extracted substring using ddmmyyyy format
        date_ddmmyyyy = datetime.datetime.strptime(date_substring, '%d%m%Y').date()
        return date_ddmmyyyy.strftime('%Y/%B %Y/%d%m%Y')
    except ValueError:
        pass
    
    try:
        # Attempt to parse the date from the extracted substring using yyyymmdd format
        date_yyyymmdd = datetime.datetime.strptime(date_substring, '%Y%m%d').date()
        return date_yyyymmdd.strftime('%Y/%B %Y/%d%m%Y')
    except ValueError:
        return None

# Connect to Outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # 6 refers to the Inbox

# Function for refresh outlook
def refresh_outlook():
    inbox.SendReceive(True)
refresh_outlook

# Get today's date
today = datetime.date.today()

# Create the folder structure for today's date
today_folder_path = os.path.join(base_destination_folder, today.strftime("%Y"), today.strftime("%B %Y"), today.strftime("%d%m%Y"))
if not os.path.exists(today_folder_path):
    os.makedirs(today_folder_path)

# Filter and process emails with subject starting with "CALL" received today
# reports = [msg for msg in inbox.Items if msg.Subject.startswith("REPORT") and msg.ReceivedTime.date() == today]
yesterday = today - datetime.timedelta(days=1)
reports = [msg for msg in inbox.Items if msg.Subject.startswith("REPORT") and msg.ReceivedTime.date() >= yesterday]
# This is useful for late emails after 00:00 AM. Edit the script as per your usecase.

for message in reports:
    sender_email = message.SenderEmailAddress
    sender_name = sender_email.split('@')[0]
    formatted_sender_name = sender_name.capitalize()
    
    for attachment in message.Attachments:
        # Check if the attachment is a zip file
        if attachment.FileName.endswith('.zip'):
            attachment_path = os.path.join(today_folder_path, attachment.FileName)
            attachment.SaveAsFile(attachment_path)

            # Extract files from the zip archive
            with zipfile.ZipFile(attachment_path, 'r') as zip_ref:
                # Extract files to the today's folder path
                zip_ref.extractall(today_folder_path)
            
            print(f"Extracted files from {attachment.FileName} to {today_folder_path}")
        else:
            attachment_date = extract_date_from_filename(attachment.FileName)
            if attachment_date:
                # Construct the destination path based on the attachment's date and sender's name
                destination_path = os.path.join(base_destination_folder, attachment_date, formatted_sender_name)
                if not os.path.exists(destination_path):
                    os.makedirs(destination_path)
                
                # Save the attachment to the destination path
                attachment_path = os.path.join(destination_path, attachment.FileName)
                attachment.SaveAsFile(attachment_path)
                print(f"Saved {attachment.FileName} to {attachment_path}")
            else:
                print(f"Skipping {attachment.FileName} due to unrecognized date format")
