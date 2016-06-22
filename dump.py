from csv import DictWriter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Business, Contact, Base


if __name__ == '__main__':
    engine = create_engine('sqlite:///businesses.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    with open('output.csv', 'w') as f:
        fieldnames = [
            'name',
            'mailing_address',
            'physical_address',
            'street_address',
            'city',
            'state',
            'zipcode',
            'website',
            'contact_first_name',
            'contact_last_name',
            'contact_phone',
            'contact_email'
        ]

        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        businesses = session.query(Business).distinct(Business.name)
        for business in businesses.group_by(Business.name):
            if business.contact is not None:
                if business.mailing_address is not None:
                    address = business.mailing_address
                else:
                    address = business.physical_address

                try:
                    address = address.split()
                    street_address = ' '.join(address[:-3])
                    city = address[-3][:-1]
                    state = address[-2]
                    zipcode = address[-1]
                    row = {
                        'name': business.name,
                        'mailing_address': business.mailing_address,
                        'physical_address': business.physical_address,
                        'street_address': street_address,
                        'city': city,
                        'state': state,
                        'zipcode': zipcode,
                        'website': business.website,
                        'contact_first_name': business.contact.first_name,
                        'contact_last_name': business.contact.last_name,
                        'contact_phone': business.contact.phone,
                        'contact_email': business.contact.email
                    }
                except (TypeError, AttributeError):
                    row = {
                        'name': business.name,
                        'mailing_address': business.mailing_address,
                        'physical_address': business.physical_address,
                        'website': business.website,
                        'contact_first_name': business.contact.first_name,
                        'contact_last_name': business.contact.last_name,
                        'contact_phone': business.contact.phone,
                        'contact_email': business.contact.email
                    }
                finally:
                    writer.writerow(row)
