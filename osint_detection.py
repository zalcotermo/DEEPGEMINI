import re
import requests
import json
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import socket
import dns.resolver
import ipaddress
import concurrent.futures
from datetime import datetime
import configparser

# Load API keys from configuration file
config = configparser.ConfigParser()
config.read('config.ini')

class PersonInfoDetector:
    def __init__(self):
        # Initialize API keys
        self.api_keys = {
            'numverify': config.get('API_KEYS', 'NUMVERIFY_API_KEY', fallback=None),
            'numlookup': config.get('API_KEYS', 'NUMLOOKUP_API_KEY', fallback=None),
            'abstract': config.get('API_KEYS', 'ABSTRACT_API_KEY', fallback=None),
            'ninjas': config.get('API_KEYS', 'NINJAS_API_KEY', fallback=None),
            'hunterio': config.get('API_KEYS', 'HUNTERIO_API_KEY', fallback=None),
            'opencellid': config.get('API_KEYS', 'OPENCELLID_API_KEY', fallback=None),
            'opencage': config.get('API_KEYS', 'OPENCAGE_API_KEY', fallback=None),
            'ipqualityscore': config.get('API_KEYS', 'IPQUALITYSCORE_API_KEY', fallback=None),
            'bigdatacloud': config.get('API_KEYS', 'BIGDATACLOUD_API_KEY', fallback=None),
            'lookify': config.get('API_KEYS', 'LOOKIFY_API_KEY', fallback=None),
            'veriphone': config.get('API_KEYS', 'VERIPHONE_API_KEY', fallback=None),
            'ipgeolocation': config.get('API_KEYS', 'IPGEOLOCATION_API_KEY', fallback=None),
            'ipapi': config.get('API_KEYS', 'IPAPI_API_KEY', fallback=None),
            'neutrino': config.get('API_KEYS', 'NEUTRINO_API_KEY', fallback=None),
            'twilio_sid': config.get('API_KEYS', 'TWILIO_SID', fallback=None),
            'twilio_token': config.get('API_KEYS', 'TWILIO_TOKEN', fallback=None)
        }
        
        # Regex patterns
        self.name_pattern = re.compile(r'([A-Z][a-z]+)\s+([A-Z][a-z]+)')
        self.email_pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
        self.phone_pattern = re.compile(r'(\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4})')

    def extract_names(self, text):
        """Extract first and last names using regex patterns"""
        names = self.name_pattern.findall(text)
        return [{'first_name': name[0], 'last_name': name[1]} for name in names]

    def extract_emails(self, text):
        """Extract email addresses with domain parsing"""
        emails = self.email_pattern.findall(text)
        results = []
        for email in emails:
            domain = email.split('@')[1]
            results.append({
                'email': email,
                'domain': domain
            })
        return results

    def extract_phones(self, text):
        """Extract and validate phone numbers"""
        phones = self.phone_pattern.findall(text)
        validated = []
        for phone in phones:
            try:
                parsed = phonenumbers.parse(phone, None)
                if phonenumbers.is_valid_number(parsed):
                    validated.append(phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164))
            except:
                continue
        return validated

    def numverify_lookup(self, phone_number):
        """Phone number lookup using Numverify API"""
        if not self.api_keys['numverify']:
            return None
            
        url = f"http://apilayer.net/api/validate?access_key={self.api_keys['numverify']}&number={phone_number}"
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            print(f"Numverify error: {e}")
            return None

    def numlookup_lookup(self, phone_number):
        """Phone number lookup using Numlookup API"""
        if not self.api_keys['numlookup']:
            return None
            
        url = f"https://api.numlookupapi.com/v1/validate/{phone_number}?apikey={self.api_keys['numlookup']}"
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            print(f"Numlookup error: {e}")
            return None

    def hunterio_lookup(self, email):
        """Email lookup using Hunter.io API"""
        if not self.api_keys['hunterio']:
            return None
            
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={self.api_keys['hunterio']}"
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            print(f"Hunter.io error: {e}")
            return None

    def opencage_geocode(self, query):
        """Geocoding using OpenCage API"""
        if not self.api_keys['opencage']:
            return None
            
        url = f"https://api.opencagedata.com/geocode/v1/json?q={query}&key={self.api_keys['opencage']}"
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            print(f"OpenCage error: {e}")
            return None

    def ipgeolocation_lookup(self, ip):
        """IP geolocation using IPGeolocation API"""
        if not self.api_keys['ipgeolocation']:
            return None
            
        url = f"https://api.ipgeolocation.io/ipgeo?apiKey={self.api_keys['ipgeolocation']}&ip={ip}"
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            print(f"IPGeolocation error: {e}")
            return None

    def lookify_search(self, query):
        """Social media profile discovery using Lookify"""
        if not self.api_keys['lookify']:
            return None
            
        url = f"https://api.lookify.io/v1/search?query={query}&api_key={self.api_keys['lookify']}"
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            print(f"Lookify error: {e}")
            return None

    def get_domain_info(self, domain):
        """Get domain information including IP and MX records"""
        try:
            # Get IP address
            ip = socket.gethostbyname(domain)
            
            # Get MX records
            mx_records = []
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                for rdata in answers:
                    mx_records.append({
                        'exchange': str(rdata.exchange),
                        'preference': rdata.preference
                    })
            except:
                pass
                
            return {
                'domain': domain,
                'ip_address': ip,
                'mx_records': mx_records
            }
        except Exception as e:
            print(f"Domain info error: {e}")
            return None

    def analyze_person(self, text):
        """Comprehensive analysis of text for person information"""
        results = {
            'names': self.extract_names(text),
            'emails': self.extract_emails(text),
            'phones': self.extract_phones(text),
            'phone_details': [],
            'email_details': [],
            'geolocation': [],
            'social_profiles': []
        }
        
        # Process phone numbers
        with concurrent.futures.ThreadPoolExecutor() as executor:
            phone_futures = {executor.submit(self.numverify_lookup, phone): phone for phone in results['phones']}
            for future in concurrent.futures.as_completed(phone_futures):
                result = future.result()
                if result:
                    results['phone_details'].append(result)
                    
                    # Get geolocation from phone number
                    if 'country_code' in result:
                        geo_result = self.opencage_geocode(result['country_name'])
                        if geo_result:
                            results['geolocation'].append(geo_result)
        
        # Process emails
        with concurrent.futures.ThreadPoolExecutor() as executor:
            email_futures = {executor.submit(self.hunterio_lookup, email['email']): email for email in results['emails']}
            for future in concurrent.futures.as_completed(email_futures):
                result = future.result()
                if result:
                    results['email_details'].append(result)
                    
                    # Get domain info
                    domain = result['data']['email'].split('@')[1]
                    domain_info = self.get_domain_info(domain)
                    if domain_info:
                        results['geolocation'].append(self.ipgeolocation_lookup(domain_info['ip_address']))
        
        # Social profile discovery based on names
        for name in results['names']:
            query = f"{name['first_name']} {name['last_name']}"
            social_result = self.lookify_search(query)
            if social_result:
                results['social_profiles'].append(social_result)
        
        return results

    def reverse_phone_lookup(self, phone_number):
        """Comprehensive reverse phone lookup"""
        results = {}
        
        # Basic phone parsing
        try:
            parsed = phonenumbers.parse(phone_number)
            results['basic_info'] = {
                'international_format': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                'carrier': carrier.name_for_number(parsed, 'en'),
                'geolocation': geocoder.description_for_number(parsed, 'en'),
                'timezone': timezone.time_zones_for_number(parsed)
            }
        except Exception as e:
            print(f"Phone parsing error: {e}")
        
        # API lookups
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                'numverify': executor.submit(self.numverify_lookup, phone_number),
                'numlookup': executor.submit(self.numlookup_lookup, phone_number)
            }
            
            for service, future in futures.items():
                try:
                    result = future.result()
                    if result:
                        results[service] = result
                except Exception as e:
                    print(f"{service} lookup error: {e}")
        
        return results

    def reverse_email_lookup(self, email):
        """Comprehensive reverse email lookup"""
        results = {}
        
        # Hunter.io lookup
        hunter_result = self.hunterio_lookup(email)
        if hunter_result:
            results['hunterio'] = hunter_result
        
        # Domain analysis
        domain = email.split('@')[1]
        domain_info = self.get_domain_info(domain)
        if domain_info:
            results['domain_info'] = domain_info
            
            # IP geolocation
            ip_geo = self.ipgeolocation_lookup(domain_info['ip_address'])
            if ip_geo:
                results['ip_geolocation'] = ip_geo
        
        # Social profile discovery
        social_result = self.lookify_search(email)
        if social_result:
            results['social_profiles'] = social_result
        
        return results

    def name_based_search(self, first_name, last_name, location_filter=None):
        """Search for person based on name with optional location filter"""
        query = f"{first_name} {last_name}"
        if location_filter:
            query += f" {location_filter}"
        
        results = {}
        
        # Lookify search
        lookify_result = self.lookify_search(query)
        if lookify_result:
            results['social_profiles'] = lookify_result
        
        # OpenCage geocoding (if location provided)
        if location_filter:
            geo_result = self.opencage_geocode(location_filter)
            if geo_result:
                results['geolocation'] = geo_result
        
        return results


if __name__ == "__main__":
    detector = PersonInfoDetector()
    
    # Example usage
    sample_text = """
    Salif Sow can be contacted at salifsow764@gmail.com or +221-346-20-91.
    Salif Sow's email is zalco911@hotmail.com and her phone is +221773462091.
    """
    
    print("Analyzing sample text...")
    analysis = detector.analyze_person(sample_text)
    print(json.dumps(analysis, indent=2))
    
    print("\nReverse phone lookup for +221773462091...")
    phone_lookup = detector.reverse_phone_lookup("+221773462091")
    print(json.dumps(phone_lookup, indent=2))
    
    print("\nReverse email lookup for salifsow764@gmail.com...")
    email_lookup = detector.reverse_email_lookup("salifsow764@gmail.com")
    print(json.dumps(email_lookup, indent=2))
    
    print("\nName-based search for Salif Sow...")
    name_search = detector.name_based_search("Salif", "Sow", "Dakar")
    print(json.dumps(name_search, indent=2))
