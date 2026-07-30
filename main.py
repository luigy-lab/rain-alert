##################### Extra Hard Starting Project ######################
import random
import smtplib

import pandas as pd
import datetime as dt

#Get list of letter
letters=[]
for _ in range(1, 5):
    try:
        with open(f'letter_templates/letter_{_}.txt', 'r') as f:
            letters.append(f.read())
    except FileNotFoundError:
        pass

# 1. Update the birthdays.csv
data = pd.read_csv("birthdays.csv")

birthdays = data.to_dict(orient="records")
days = [(i["month"], i["day"]) for i in birthdays]

# 2. Check if today matches a birthday in the birthdays.csv
current_time = dt.datetime.now()
current_day = (current_time.month, current_time.day)

#CREDENTIALS
MY_EMAIL = "rei.luismiguelalves@gmail.com"
MY_PASSWORD = "ctfryesduhslpxpb"

if current_day in days:
    person = birthdays[days.index(current_day)]
    # 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
    letter = random.choice(letters)
    letter = letter.replace("[NAME]", person["name"])
    letter = letter.replace("Angela", "Luigy")

    # 4. Send the letter generated in step 3 to that person's email address.
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=person["email"],
                            msg=f"Subject:Happy Birthday!\n\n{letter}")




