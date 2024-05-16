import win32com.client
def refresh_outlook():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)
    inbox.SendReceive(True)
refresh_outlook