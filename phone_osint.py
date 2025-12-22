import requests
import json
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import pandas as pd
from datetime import datetime
import time

# API Keys Configuration (replace with your actual keys)
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

def basic_phone_analysis(phone_number):
    """Basic phone analysis using phonenumbers library"""
    try:
        parsed_number = phonenumbers.parse(phone_number)
        results = {
            'carrier': carrier.name_for_number(parsed_number, 'en'),
            'geolocation': geocoder.description_for_number(parsed_number, 'en'),
            'timezone': timezone.time_zones_for_number(parsed_number),
            'national_format': phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL),
            'international_format': phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            'is_valid': phonenumbers.is_valid_number(parsed_number),
            'is_possible': phonenumbers.is_possible_number(parsed_number)
        }
        return results
    except Exception as e:
        return {'error': str(e)}

def numverify_lookup(phone_number):
    """Lookup phone number using NumVerify API"""
    url = f"http://apilayer.net/api/validate?access_key={API_KEYS['numverify']}&number={phone_number}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def numlookup_lookup(phone_number):
    """Lookup phone number using NumLookupAPI"""
    url = f"https://api.numlookupapi.com/v1/validate/{phone_number}?apikey={API_KEYS['numlookup']}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def opencage_geocode(lat, lng):
    """Reverse geocode using OpenCage"""
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lng}&key={API_KEYS['opencage']}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def neutrino_lookup(phone_number):
    """Phone lookup using Neutrino API"""
    url = "https://neutrinoapi.net/phone-validate"
    params = {
        'user-id': API_KEYS['neutrino'].split(':')[0],
        'api-key': API_KEYS['neutrino'].split(':')[1],
        'number': phone_number,
        'ip': '',
        'country-code': ''
    }
    try:
        response = requests.post(url, data=params)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def abstract_lookup(phone_number):
    """Phone lookup using Abstract API"""
    url = f"https://phonevalidation.abstractapi.com/v1/?api_key={API_KEYS['abstract']}&phone={phone_number}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def hunterio_lookup(phone_number):
    """Lookup email associated with phone using Hunter.io"""
    url = f"https://api.hunter.io/v2/phone-number?phone={phone_number}&api_key={API_KEYS['hunterio']}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def ipqualityscore_lookup(phone_number):
    """Check phone reputation using IPQualityScore"""
    url = f"https://www.ipqualityscore.com/api/json/phone/{API_KEYS['ipqualityscore']}/{phone_number}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def bigdatacloud_lookup(phone_number):
    """Phone lookup using BigDataCloud"""
    url = f"https://api.bigdatacloud.net/data/phone-number-validate?number={phone_number}&key={API_KEYS['bigdatacloud']}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def lookify_lookup(phone_number):
    """Phone lookup using Lookify API"""
    url = f"https://api.lookify.co/v1/lookup?phone={phone_number}&api_key={API_KEYS['lookify']}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def ninjas_lookup(phone_number):
    """Phone lookup using API Ninjas"""
    url = f"https://api.api-ninjas.com/v1/validatephone?number={phone_number}"
    headers = {'X-Api-Key': API_KEYS['ninjas']}
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def social_media_search(phone_number):
    """Search for social media profiles associated with phone number"""
    # Note: Actual social media searches may require specialized APIs or web scraping
    return {'message': 'Social media search requires additional implementation'}

def generate_report(phone_number, results):
    """Generate a comprehensive report from all gathered data"""
    report = {
        'phone_number': phone_number,
        'timestamp': datetime.now().isoformat(),
        'basic_analysis': results.get('basic_analysis'),
        'numverify': results.get('numverify'),
        'numlookup': results.get('numlookup'),
        'neutrino': results.get('neutrino'),
        'abstract': results.get('abstract'),
        'hunterio': results.get('hunterio'),
        'ipqualityscore': results.get('ipqualityscore'),
        'bigdatacloud': results.get('bigdatacloud'),
        'lookify': results.get('lookify'),
        'ninjas': results.get('ninjas'),
        'social_media': results.get('social_media')
    }
    
    # Save to JSON file
    filename = f"phone_report_{phone_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=4)
    
    return filename

def deep_phone_scan(phone_number):
    """Perform deep scan of phone number using all available APIs"""
    formatted_number = validate_phone_number(phone_number)
    if not formatted_number:
        return {'error': 'Invalid phone number'}
    
    results = {}
    
    # Basic analysis
    results['basic_analysis'] = basic_phone_analysis(formatted_number)
    
    # API lookups
    results['numverify'] = numverify_lookup(formatted_number)
    time.sleep(1)  # Rate limiting
    
    results['numlookup'] = numlookup_lookup(formatted_number)
    time.sleep(1)
    
    results['neutrino'] = neutrino_lookup(formatted_number)
    time.sleep(1)
    
    results['abstract'] = abstract_lookup(formatted_number)
    time.sleep(1)
    
    results['hunterio'] = hunterio_lookup(formatted_number)
    time.sleep(1)
    
    results['ipqualityscore'] = ipqualityscore_lookup(formatted_number)
    time.sleep(1)
    
    results['bigdatacloud'] = bigdatacloud_lookup(formatted_number)
    time.sleep(1)
    
    results['lookify'] = lookify_lookup(formatted_number)
    time.sleep(1)
    
    results['ninjas'] = ninjas_lookup(formatted_number)
    time.sleep(1)
    
    # Social media search
    results['social_media'] = social_media_search(formatted_number)
    
    # Generate report
    report_file = generate_report(formatted_number, results)
    
    return {
        'status': 'completed',
        'report_file': report_file,
        'results': results
    }

if __name__ == "__main__":
    print("Phone OSINT Deep Scan Tool")
    print("--------------------------")
    
    phone_number = input("Enter phone number to scan (include country code): ").strip()
    
    print("\nStarting deep scan...")
    scan_results = deep_phone_scan(phone_number)
    
    if 'error' in scan_results:
        print(f"\nError: {scan_results['error']}")
    else:
        print(f"\nScan completed! Report saved to: {scan_results['report_file']}")
        
        # Display summary
        basic = scan_results['results']['basic_analysis']
        print("\nBasic Information:")
        print(f"Carrier: {basic.get('carrier', 'N/A')}")
        print(f"Location: {basic.get('geolocation', 'N/A')}")
        print(f"Timezone: {', '.join(basic.get('timezone', ['N/A']))}")
        
        # Display validation results from first available API
        validation = next((v for v in [
            scan_results['results']['numverify'],
            scan_results['results']['numlookup'],
            scan_results['results']['abstract']
        ] if 'valid' in v), {})
        
        if validation:
            print("\nValidation Results:")
            print(f"Valid: {validation.get('valid', 'N/A')}")
            print(f"Local Format: {validation.get('local_format', 'N/A')}")
            print(f"International Format: {validation.get('international_format', 'N/A')}")
            print(f"Country: {validation.get('country_name', 'N/A')} ({validation.get('country_code', 'N/A')})")
            print(f"Location: {validation.get('location', 'N/A')}")
            print(f"Carrier: {validation.get('carrier', 'N/A')}")
            print(f"Line Type: {validation.get('line_type', 'N/A')}")
        
        # Display reputation score if available
        reputation = scan_results['results']['ipqualityscore']
        if 'reputation' in reputation:
            print("\nReputation Analysis:")
            print(f"Reputation Score: {reputation.get('reputation', 'N/A')}")
            print(f"Risk Score: {reputation.get('risk_score', 'N/A')}")
            print(f"Fraud Score: {reputation.get('fraud_score', 'N/A')}")
            print(f"Active: {reputation.get('active', 'N/A')}")
        
        print("\nFull details available in the generated report file.")
