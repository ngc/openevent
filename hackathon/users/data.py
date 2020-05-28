from django.contrib.auth.models import User
from users.models import Team
import csv
import os 
import random
import string
import pandas as pd

usernames = []
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

path = "C:/Users/Nathan/Downloads/MississaugaHacks 2020 Signup (Responses) - Form Responses 1 (7).csv"

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
            first_name = row['FIRST NAME'].replace(" ", ""),
            last_name = row['LAST NAME'].replace(" ", ""),
            email = row['EMAIL'].replace(" ", ""),   
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


zl = list(zip(usernames, pw))
df = pd.DataFrame(zl, columns=["Username", "Password"])
df.to_csv('C:/Users/Nathan/Desktop/logs.csv', index=False)

exit()
#exec(open('users/data.py').read())

