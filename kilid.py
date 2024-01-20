import requests
from bs4 import BeautifulSoup
import mysql.connector
import re

def creat_table(table_name):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '43055',
        'database': 'Test'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        location VARCHAR(255),
        rooms VARCHAR(255),
        parking VARCHAR(255),
        price VARCHAR(255),
        metr VARCHAR(255)
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()

def save_information(db,location, rooms,parking,price,metr):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '43055',
        'database': 'Test'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    select_query = (f"SELECT * FROM {db} "
                    f"WHERE location = %s AND rooms = %s AND parking = %s AND price = %s AND metr = %s")
    cursor.execute(select_query, (location, rooms,parking,price,metr))
    existing_data = cursor.fetchone()

    if not existing_data:
        insert_query = (f"INSERT INTO {db} (location, rooms,parking,price,metr) "
                        f"VALUES (%s, %s,%s, %s,%s)")
        cursor.execute(insert_query,(location, rooms,parking,price,metr))
        connection.commit()
        print('add')
    print('done')
    cursor.close()
    connection.close()



creat_table('house')
for i in range(200):
    base_url = f'https://kilid.com/buy-apartment/tehran?page={i}'
    response = requests.get(base_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div',class_='pb-4')
        house={}
        i=0
        for div in divs:
            h={}
            p = div.select('div.pb-4 span.text-lg')
            if len(p)!=0:
                price= re.sub(r'قیمت:',r'',p[0].text)
                h['price']=price
            else:
                h['price'] ='توافقی'
            ad = div.select('p.inline-flex span')
            address = ad[0].text
            h['address']=address
            spans = div.select('div.-m-2 span.whitespace-nowrap')
            for span in spans:
                val=str(span.text).split()
                if len(val)==1:
                    noe = val[0]
                elif val[1] == 'متر':
                    metr=val[0]
                    h['metr'] = metr
                elif val[1] == 'خواب':
                    room=val[0]
                    h['room'] = room
                elif val[1] == 'پارکینگ':
                    parking=val[0]
                    h['parking'] = parking
            for key in ['price','address', 'metr', 'room', 'parking']:
                if key not in h.keys():
                      h[key] = 'ثبت نشده'
            save_information('house',h['address'],h['room'],h['parking'],h['price'],h['metr'])



    else:
         print(f'Failed to fetch data')
