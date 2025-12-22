import requests
import json
import sys
from datetime import datetime
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import reverse_geocoder as rg
import pycountry
import socket
import dns.resolver
import re

# API Keys Configuration (Replace with your actual API keys)
API_KEYS = {
    'opencage': 'f8c073589bca4d09b09a50e7c600ee10',
    'opencellid': '1f8f328afa8ba5',
    'numverify': 'd4356687121b52819a7ea470c6387d5f',
    'numlookup': 'num_live_B6AfEveoFnwe6TIKV2oL8T6KcY10oRLsQ4HzzSvn',
    'abstract': '7a04b241a273441cb59f333ea80b93d4',
    'ninjas': 'sUsLXVH/ik6Prq3y82s1JA==MemGS6cWyrR31Qn3',
    'lookify': '42c24cb1-b8b3-b198-7116-91b176a6b0e6',
    'neutrino': 'zalco:gbGIAK6VmaXNcgZc8iBMsOPuHCIL5tsNbrD5CzTjxNvB6pEs',
    'hunterio': '374d3258ec737081b981b693ac6590661c87c60d',
    'bigdatacloud': 'bdc_afb64aea91744a5cb05857e673d824f3',
    'ipqualityscore': 'ffEazTnuE5Zw2SMmvL3OUw1yPf7UToTV'
}

def validate_phone_number(phone_number):
    """Validate and format phone number using phonenumbers library"""
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            return None
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    except:
        return None

def validate_email(email):
    """Basic email validation using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_numverify_info(phone_number):
    """Get phone number info from Numverify API"""
    url = f"http://apilayer.net/api/validate?access_key={API_KEYS['numverify']}&number={phone_number}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return {"error": "Numverify API request failed"}

def get_numlookup_info(phone_number):
    """Get phone number info from Numlookup API"""
    url = f"https://api.numlookupapi.com/v1/validate/{phone_number}?apikey={API_KEYS['numlookup']}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return {"error": "Numlookup API request failed"}

def get_abstract_info(phone_number):
    """Get phone number info from Abstract API"""
    url = f"https://phonevalidation.abstractapi.com/v1/?api_key={API_KEYS['abstract']}&phone={phone_number}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return {"error": "Abstract API request failed"}

def get_opencellid_info(phone_number):
    """Get cell tower info from OpenCellID API"""
    url = f"https://us1.unwiredlabs.com/v2/process.php"
    payload = {
        "token": API_KEYS['opencellid'],
        "radio": "gsm",
        "mcc": phone_number[:3],  # Mobile Country Code
        "mnc": phone_number[3:5],  # Mobile Network Code
        "cells": [{"lac": 1, "cid": 2}],  # Sample cell data
        "address": 1
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except:
        return {"error": "OpenCellID API request failed"}

def get_opencage_geolocation(lat, lng):
    """Get geolocation info from OpenCage API"""
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lng}&key={API_KEYS['opencage']}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return {"error": "OpenCage API request failed"}

def get_email_info(email):
    """Get email info from Hunter.io API"""
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={API_KEYS['hunterio']}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return {"error": "Hunter.io API request failed"}

def get_social_media_profiles(email):
    """Get social media profiles associated with email"""
    url = f"https://api.lookup.com/v1/social-media-profiles?email={email}"
    headers = {"Authorization": f"Bearer {API_KEYS['lookify']}"}
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except:
        return {"error": "Social media lookup failed"}

def get_domain_info(domain):
    """Get domain information"""
    url = f"https://companyenrichment.abstractapi.com/v1/?api_key={API_KEYS['abstract']}&domain={domain}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return {"error": "Domain info API request failed"}

def get_mx_records(domain):
    """Get MX records for a domain"""
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return [str(r.exchange) for r in answers]
    except:
        return []

def reverse_email_search(email):
    """Perform reverse email search"""
    domain = email.split('@')[-1]
    results = {
        "domain_info": get_domain_info(domain),
        "mx_records": get_mx_records(domain),
        "social_media": get_social_media_profiles(email),
        "email_verification": get_email_info(email)
    }
    return results

def get_neutrino_info(phone_number):
    """Get phone number info from Neutrino API"""
    url = "https://neutrinoapi.net/phone-validate"
    params = {
        "user-id": "your-user-id",
        "api-key": API_KEYS['neutrino'],
        "number": phone_number,
        "country-code": "",
        "ip": ""
    }
    try:
        response = requests.post(url, data=params)
        return response.json()
    except:
        return {"error": "Neutrino API request failed"}

def get_ipqualityscore_info(phone_number):
    """Get phone number reputation from IPQualityScore"""
    url = f"https://www.ipqualityscore.com/api/json/phone/{API_KEYS['ipqualityscore']}/{phone_number}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return {"error": "IPQualityScore API request failed"}

def get_bigdatacloud_info(ip_address):
    """Get IP geolocation info from BigDataCloud"""
    url = f"https://api.bigdatacloud.net/data/ip-geolocation?ip={ip_address}&key={API_KEYS['bigdatacloud']}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return {"error": "BigDataCloud API request failed"}

def get_phone_carrier(phone_number):
    """Get carrier information using phonenumbers library"""
    try:
        parsed_number = phonenumbers.parse(phone_number)
        return carrier.name_for_number(parsed_number, "en")
    except:
        return "Unknown"

def get_phone_geolocation(phone_number):
    """Get approximate geolocation using phonenumbers library"""
    try:
        parsed_number = phonenumbers.parse(phone_number)
        return geocoder.description_for_number(parsed_number, "en")
    except:
        return "Unknown"

def get_phone_timezone(phone_number):
    """Get timezone using phonenumbers library"""
    try:
        parsed_number = phonenumbers.parse(phone_number)
        return timezone.time_zones_for_number(parsed_number)
    except:
        return ["Unknown"]

def comprehensive_phone_analysis(phone_number):
    """Perform comprehensive phone number analysis"""
    print(f"\n[+] Starting comprehensive analysis for: {phone_number}")
    
    # Basic phone number parsing
    parsed_info = {
        "valid": True,
        "carrier": get_phone_carrier(phone_number),
        "geolocation": get_phone_geolocation(phone_number),
        "timezone": get_phone_timezone(phone_number),
        "e164_format": phone_number
    }
    
    # API-based lookups
    api_results = {
        "numverify": get_numverify_info(phone_number),
        "numlookup": get_numlookup_info(phone_number),
        "abstract": get_abstract_info(phone_number),
        "neutrino": get_neutrino_info(phone_number),
        "ipqualityscore": get_ipqualityscore_info(phone_number)
    }
    
    # Combine all results
    final_result = {
        "basic_info": parsed_info,
        "api_results": api_results,
        "timestamp": datetime.now().isoformat()
    }
    
    return final_result

def comprehensive_email_analysis(email):
    """Perform comprehensive email analysis"""
    print(f"\n[+] Starting comprehensive analysis for: {email}")
    
    # Basic email validation
    parsed_info = {
        "valid": validate_email(email),
        "domain": email.split('@')[-1],
        "username": email.split('@')[0]
    }
    
    # API-based lookups
    api_results = {
        "hunterio": get_email_info(email),
        "social_media": get_social_media_profiles(email),
        "domain_info": get_domain_info(parsed_info['domain'])
    }
    
    # Combine all results
    final_result = {
        "basic_info": parsed_info,
        "api_results": api_results,
        "timestamp": datetime.now().isoformat()
    }
    
    return final_result

def print_results(data):
    """Pretty print the results"""
    print("\n" + "="*50)
    print("OSINT Investigation Results")
    print("="*50)
    print(json.dumps(data, indent=4, ensure_ascii=False))
    print("="*50 + "\n")

def main():
    print("""
    ██████╗ ███████╗██╗███╗   ██╗████████╗
    ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
    ██║   ██║███████╗██║██╔██╗ ██║   ██║   
    ██║   ██║╚════██║██║██║╚██╗██║   ██║   
    ╚██████╔╝███████║██║██║ ╚████║   ██║   
     ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
                                           
    Advanced Phone & Email OSINT Tool SNDK
    """)
    
    target = input("Enter phone number (E.164 format) or email address: ").strip()
    
    if '@' in target:  # Email address
        if not validate_email(target):
            print("[-] Invalid email address format")
            sys.exit(1)
        
        results = comprehensive_email_analysis(target)
    else:  # Phone number
        formatted_number = validate_phone_number(target)
        if not formatted_number:
            print("[-] Invalid phone number format")
            sys.exit(1)
        
        results = comprehensive_phone_analysis(formatted_number)
    
    print_results(results)
    
    # Save results to file
    filename = f"osint_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f"[+] Results saved to {filename}")

if __name__ == "__main__":
    main()
