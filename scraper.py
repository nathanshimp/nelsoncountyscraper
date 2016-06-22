import requests
from bs4 import BeautifulSoup
from db import Business, Contact, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def process_address(soup):
    if soup is not None:
        address1 = soup.find('div', class_='address1')
        address3 = soup.find('div', class_='address3')
        if address1 is not None and address3 is not None:
            return address1.string + " " + address3.string
    else:
        return None

def process_contact(soup):
    if soup is not None:
        contact = Contact()
        full_name = soup.find('div', class_='contact-name')
        if full_name != None:
            full_name = full_name.string.split()
            first_name = " ".join(full_name[:-1])
            last_name = full_name[-1]
            contact.first_name = first_name
            contact.last_name = last_name

        phone = soup.find('div', class_='phone')
        if phone is not None:
            contact.phone = phone.string

        email = soup.find('div', class_='email')
        if email is not None:
            contact.email = email.string

        session.add(contact)
        session.commit()
        return contact.id
    else:
        return None

def process_organization(soup):
    business = Business()
    contact_info = soup.find('div', class_='contactinfo')
    contact_id = process_contact(contact_info)

    business.contact_id = contact_id
    business.name = soup.h3.string

    physical_address = process_address(soup.find('div', 'physicaladdress'))
    if physical_address is not None:
        business.physical_address = physical_address

    mailing_address = process_address(soup.find('div', 'mailingaddress'))
    if mailing_address is not None:
        business.mailing_address = mailing_address

    website = soup.find('div', class_='ext_url')
    if website is not None:
        business.website = website.a.string

    session.add(business)
    session.commit()
    print(business.name, '[OK]')


def process_organization_category(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    orgs = soup.find_all('div', class_='organization')
    for org in orgs:
        process_organization(org)


if __name__ == '__main__':
    engine = create_engine('sqlite:///businesses.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    business_list_url = 'http://www.nelsoncounty-va.gov/directories/business-directory/'
    business_unparsed = requests.get(business_list_url).text
    soup = BeautifulSoup(business_unparsed, 'html.parser')

    business_list_links = soup.find_all('li', class_='cat-item')
    business_links = [li.a['href'] for li in business_list_links]

    for link in business_links:
        process_organization_category(link)

    session.commit()
