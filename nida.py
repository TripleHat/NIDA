#!/bin/python

import base64
import io
import os
import time

import prettytable # type: ignore
import sys

import requests
from PIL import Image # type: ignore

from typing import Dict, Any, BinaryIO

yellow: str = '\033[33m'
blue: str = '\033[34m'
cyan: str = '\033[36m'
green: str = '\033[32;1m'
red: str = '\033[31;1m'
close: str = '\033[0m'


def text_out(text: str) -> None:
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.1)


def nida() -> None:
    print("")
    url: str = "https://ors.brela.go.tz/um/load/load_nida/"
    num: str = input(green + "Enter NIN: " + cyan)

    # replace all - with nothing to enable this to be numbers only
    num = num.replace('-', '')

    # strip any empty spaces around the number
    num = num.strip()

    digit: bool = num.isdigit()
    if str(len(num)) < str("20"):
        text_out(red + "\nNIN is wrong\n" + close)
        exit()
    if not digit:
        text_out(red + "\nNIN cant contain letters\n" + close)
        exit()

    print(close + "")

    # adding a global variable in case the try statement fails
    results: Dict[str, Any]
    profile: str
    sahihi: str

    headers: Dict[str, str] = {'Content-Type': 'application/json', 'Content-Length': '0'}
    try:
        # TODO: refactor to use Union[str, int, float, bool, None]
        # also use 3 json multi-layer representation for filter_
        # instead of nested Dicts of course.
        req: Any = requests.post(url + str(num), headers=headers)
        filter_: Dict[str, Dict[str, Dict[str, Any]]] = req.json()
        results = filter_['obj']['result']
        
        # TODO: define Jpeg custom type
        decode: bytes = base64.b64decode(results['PHOTO'])
        img: Any = Image.open(io.BytesIO(decode))
        img.save(results['FIRSTNAME'] + '.jpg')
        d_sig: bytes = base64.b64decode(results['SIGNATURE'])
        sign: Any = Image.open(io.BytesIO(d_sig))
        sign.save("signature" + results['FirstName'] + ".jpg")

        picture: str = str(results['FirstName'] + ".jpg")
        signature: str = str("signature" + results['FirstName'] + ".jpg")

        pic: Dict[str, BinaryIO] = {'file': open(picture, "rb")}
        sig: Dict[str, BinaryIO] = {'file': open(signature, "rb")}

        req1: Any = requests.post("https://0x0.st", files=pic)
        req2: Any = requests.post("https://0x0.st", files=sig)

        profile = req1.text
        sahihi = req2.text

    except:
        text_out(
            red + "\nERROR SOMETHING IS WRONG, Probably Internet Connection or Your NIN not Found In System\n" + close)
        exit()

    def clean() -> None:
        os.system("rm " + picture)
        os.system("rm " + signature)

    no: str = results['NIN']
    name1: str = results['FIRSTNAME']
    name2: str = results['MIDDLENAME']
    name3: str = results['SURNAME']
    sex: str = results['SEX']
    date: str = results['DATEOFBIRTH']
    r_region: str = results['RESIDENTREGION']
    r_district: str = results['RESIDENTDISTRICT']
    r_ward: str = results['RESIDENTWARD']
    r_village: str = results['RESIDENTVILLAGE']
    r_street: str = results['RESIDENTSTREET']
    r_postcode: str = results['RESIDENTPOSTCODE']
    p_region: str = results['PERMANENTREGION']
    pDistrict: str = results['PERMANENTDISTRICT']
    pWard: str = results['PERMANENTWARD']
    pVillage: str = results['PERMANENTVILLAGE']
    pStreet: str = results['PERMANENTSTREET']
    bCountry: str = results['BIRTHCOUNTRY']
    bRegion: str = results['BIRTHREGION']
    bDistrict: str = results['BIRTHDISTRICT']
    bWard: str = results['BIRTHWARD']
    nation: str = results['NATIONALITY']
    mStatus: str = results['MARITALSTATUS']
    work: str = results['OCCUPATION']
    pSchool: str = results['PRIMARYSCHOOLEDUCATION']
    pSDistrict: str = results['PRIMARYSCHOOLDISTRICT']
    pYear: str = results['PRIMARYSCHOOLYEAR']

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
    t.add_row([green + "PRIMARY SCHOOL DISTRICT" + close, cyan + str(pSDistrict) + close])
    t.add_row([green + "PRIMARY SCHOOL YEAR" + close, cyan + str(pYear) + close])
    t.add_row(["", ""])
    t.add_row([green + "PICTURE" + close, cyan + profile + close])
    t.add_row([green + "SIGNATURE" + close, cyan + sahihi + close])
    print(t.get_string(title=yellow + "NIDA INFO by TH33HT: CITIZEN NAME: " + name1 + close))
    clean()


if __name__ == '__main__':
    nida()
