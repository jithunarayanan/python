import os
import datetime
import win32com.client
base_destination_folder = r"\\10.10.3.23\\my_remote_dest"
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # 6 refers to the Inbox
year_str = datetime.date.today().strftime("%Y")
month_str = datetime.date.today().strftime("%b %Y")
today_str = datetime.date.today().strftime("%d%m%Y")
today_folder_path = os.path.join(base_destination_folder,year_str, month_str, today_str)
xyz = datetime.date.today()
reports = inbox.Items
reports = [msg for msg in reports if msg.Subject.startswith("REPORT") and msg.ReceivedTime.date() == xyz]

if not os.path.exists(today_folder_path):
    os.makedirs(today_folder_path)

for message in reports:
    sender_email = message.SenderEmailAddress
    sender_name = sender_email.split('@')[0]
    formatted_sender_name = sender_name.capitalize()
    employee_folder_path = os.path.join(today_folder_path, formatted_sender_name)
    if not os.path.exists(employee_folder_path):
        os.makedirs(employee_folder_path)
    
    for attachment in message.Attachments:
        attachment_path = os.path.join(employee_folder_path, attachment.FileName)
        attachment.SaveAsFile(attachment_path)
        print(f"Saved {attachment.FileName} to {attachment_path}")