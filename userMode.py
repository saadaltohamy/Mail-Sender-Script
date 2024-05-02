from script import connect_to_gmailAPI, create_message_with_eml, send_message, convert_CSV_Tolist
import time

def MailSender(sender_name, sender_email, eml_file_path, recipeints):
    sender = sender_name + " <" + sender_email + ">"
    service = connect_to_gmailAPI()
    print("===============================================")
    print()
    for idx, recipient in enumerate(recipeints):
        message = create_message_with_eml(eml_file_path, sender, recipient, 'SAAD')
        send_message(service, 'me', message)
        print("\033[92mEmail", idx+1, "sent successfully to", recipient, "\033[0m")
        print()
        time.sleep(1)
    print("===============================================")


'''
sender_name: str
    The name of the sender
sender_email: str
    The email of the sender
eml_file_path: str
    The path of the .eml file
recipeints: list
    The list of recipients
'''
sender_name = "Enter Your Name Here"
sender_email = "Enter Your Email Here"
eml_file_path = 'filepath.eml'
recipeints = convert_CSV_Tolist('filename.csv', 'column_name')

MailSender(sender_name, sender_email, eml_file_path, recipeints)