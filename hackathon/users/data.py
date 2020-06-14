from django.contrib.auth.models import User
from users.models import Team
import csv
import os 
import random
import string
import pandas as pd

usernames = []
emails = []
firstnames = []
pw = []

def GenRandom(length):
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(length))

def genPassword(length=6):
    randomSource = string.ascii_letters + string.digits
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)

    for i in range(length):
        password += random.choice(randomSource)

    passwordList = list(password)
    random.SystemRandom().shuffle(passwordList)
    password = ''.join(passwordList)
    return password

<<<<<<< HEAD
path = "/root/hackathonserver/spreadsheets/MississaugaHacks 2020 Signup (Responses) - Form Responses 1 (9).csv"
=======
path = "C:/Users/Nathan/Downloads/MississaugaHacks 2020 Signup (Responses) - Form Responses 1 (8).csv"
>>>>>>> c29da9e8d905384842bccddbb380527d7c036f20

#Team Handler
teams = []
with open(path) as data:
    reader = csv.DictReader(data)
    for row in reader:
        if(row['TIME'] == ""): continue
        if(row['FIRST NAME'].replace(" ", "") + " " + row['LAST NAME'].replace(" ", "") not in teams):
            p = Team(
                name = row['FIRST NAME'].replace(" ", "") + " " + row['LAST NAME'].replace(" ", "")
            )
            p.save() 


with open(path) as data:
    reader = csv.DictReader(data)
    for row in reader:
        if(row['TIME'] == ""): continue
        pword = genPassword()
        pw.append(pword)
        emails.append(row['EMAIL'].strip())
        firstnames.append(row['FIRST NAME'].strip())
        uname = row['FIRST NAME'].replace(" ", "") + str(GenRandom(3))
        print("Username: " + uname + " | Password: " + pword)
        usernames.append(uname)
        if(row['TEAM'] == ""):
            tname = row['FIRST NAME'].replace(" ", "") + " " + row['LAST NAME'].replace(" ", "")
        else:
            tname = row['TEAM'].strip()

        p = User.objects.create_user(
            username = uname,
            password = pword,
            first_name = row['FIRST NAME'].strip(),
            last_name = row['LAST NAME'].strip(),
            email = row['EMAIL'].strip(),   
        )
        p.save()

        p = User.objects.get(username=uname)
        p.profile.school = (row['SCHOOL'])
        p.profile.save()

        p = User.objects.get(username=uname)
        p.profile.team = Team.objects.get(name=tname)
        p.profile.save()

        p = User.objects.get(username=uname)
        p.submission.team = p.profile.team
        p.submission.save()

        t = Team.objects.get(name=tname)
        t.users.add(User.objects.get(username=uname))
        t.save()


zl = list(zip(usernames, pw, emails, firstnames))
df = pd.DataFrame(zl, columns=["Username", "Password", "Email", "Firstname"])
df.to_csv('/root/hackathonserver/spreadsheets/logs.csv', index=False)

exit()
#exec(open('users/data.py').read())