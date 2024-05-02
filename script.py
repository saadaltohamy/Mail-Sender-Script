import base64
from email import policy
from email.parser import BytesParser
from email.message import EmailMessage

def install_packages():
    # if the user doesn't have the required packages, install them
    import subprocess
    import sys
    required_packages = ["pandas", "google_auth_oauthlib", "googleapiclient"]
    for idx, package in enumerate(required_packages):
        try:
            __import__(package)
        except ImportError:
            if idx == 2:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "google-api-python-client"])
            else:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def convert_CSV_Tolist(file, column_name):
    import pandas as pd
    df = pd.read_csv(file)
    return df[column_name].tolist()


def connect_to_gmailAPI():
    install_packages()
    global service
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    
    # connnect to the gmail API
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    service = build("gmail", "v1", credentials=creds)
    return service


def create_message_with_eml(eml_file_path, new_from, new_to, recipient_name):
    f = open(eml_file_path, 'rb')
    msg = BytesParser(policy=policy.default).parse(f)
    new_msg = EmailMessage()

    # Copy headers
    for key, value in msg.items():
        new_msg[key] = value
    
    # Copy parts
    if msg.is_multipart():
        for part in msg.iter_parts():
            if part.get_content_type() == 'text/plain':
                body = part.get_content()
                new_body = body.replace('&_NAME_&', recipient_name)
                new_part = EmailMessage()
                new_part.set_content(new_body, subtype='plain')
                new_msg.attach(new_part)
            else:
                new_msg.attach(part)
        del msg   
    else:
        body = msg.get_content()
        new_body = body.replace('&_NAME_&', recipient_name)
        new_msg.set_content(new_body)

    new_msg.replace_header('From', new_from)
    new_msg.replace_header('To', new_to)
    raw = base64.urlsafe_b64encode(new_msg.as_bytes())
    raw = raw.decode()
    # f.close()
    return {"raw": raw}


def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        return message
    except Exception as e:
        print('An error occurred: %s' % e)
        return None

