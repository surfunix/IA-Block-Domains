import os
import re
from PyPDF2 import PdfReader

def load_blocked_domains(file_path):
    with open(file_path, 'r') as file:
        blocked_domains = set(file.read().splitlines())
    return blocked_domains

def load_whitelist(file_path):
    with open(file_path, 'r') as file:
        whitelist = set(file.read().splitlines())
    return whitelist

def extract_domains_from_pdf(pdf_path):
    domains = set()
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)):
            text = reader.pages[page_num].extract_text()
            found_domains = re.findall(r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', text)
            domains.update(found_domains)
    return domains

def filter_new_domains(domains, blocked_domains, whitelist):
    new_domains = domains - blocked_domains - whitelist
    return new_domains

def main():
    blocked_domains = load_blocked_domains('../testadores_raw')
    whitelist = load_whitelist('whitelist')
    new_domains = set()

    for root, dirs, files in os.walk('repository'):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                domains = extract_domains_from_pdf(pdf_path)
                new_domains.update(filter_new_domains(domains, blocked_domains, whitelist))

    with open('new_domains', 'w') as file:
        for domain in new_domains:
            file.write(f"{domain}\n")

if __name__ == "__main__":
    main()
