from django.contrib.auth.models import User
from users.models import Team
import csv
import os 
import random
import string
import pandas as pd

# This script generates the users from the sign up form you made (Google Form)
# Steps:
# 1. Remove any wrong or conflicting data from your form
#       - All team leader names are case sensitive 
#       - The team leader specified in the row MUST have signed up, if they didn't then clear the cell
#       - Team leader names must match the name that the team leader used when signing up themselves
# 2. Download your form submissions as a csv file with a comma as the delimiter 
# 3. Enter in the specified paths within the script for both the location on the server's system to the input form data, as well as the exported generated user data
# 4. Run the script by executing 'python3 manage.py shell' then enter 'exec(open('users/data.py').read())' 


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

path = "" #Valid path to the sign up's exported csv

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
df.to_csv('', index=False) 

#Use a valid directory for storing your csv with usernames and passwords to be emailed out.
#For security reasons you should urge your users to change these details when they have access to their accounts
#You should also make a copy of this csv file and store it locally on your own machine and delete it from the server

exit()
#exec(open('users/data.py').read())
#Execution Command