import os
from dotenv import load_dotenv
import time
import requests
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from bs4 import BeautifulSoup
import schedule

load_dotenv()

def get_page_contents(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    page = requests.get(url, headers=headers)

    if page.status_code == 200:
        return page.text

    return None

def get_title_and_temp(page_contents):
    soup = BeautifulSoup(page_contents, 'html.parser')
    title = soup.find_all('span', class_='title')
    temp = soup.find_all('span', class_='temp')
    return title, temp

def send_mail():     
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')

    from_email = os.getenv('FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL')
    subject = 'Temperature report in Brazil'
    body = 'See the attached file to view the data'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    with open('report.csv', 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='csv')
        attachment.add_header('Content-Disposition', 'attachment', filename='report.csv')
        msg.attach(attachment)

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(msg)

if __name__ == '__main__':
    url = 'https://www.accuweather.com/pt/br/brazil-weather'
    page_contents = get_page_contents(url)

    if page_contents:
        title, temp = get_title_and_temp(page_contents)
        
        data = {
            'City': [t.text for t in title],
            'Temp': [t.text for t in temp] 
        }
        df = pd.DataFrame(data)
        df.to_csv('report.csv', index=False)

        schedule.every().day.at("8:00").do(send_mail)
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        print('Failed to get page contents.')
