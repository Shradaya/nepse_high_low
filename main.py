import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import argparse
from mapper import symbol
from mail import Mail


def get_data(sec, receiver_email):
    dictionary = {}
    message = []
    security_list = sec['symbol'].tolist()
    for pagination in range(1, 12):
        url = f"http://www.nepalstock.com/main/todays_price/index/{pagination}/"
        gethtml = requests.get(url)
        html = gethtml.text
        bs = BeautifulSoup(html, "lxml")
        table = bs.find('table', {'class': 'table table-condensed table-hover'})
        tr = table.findAll('tr')[2:-4]

        for row in tr:
            cols = row.find_all('td')
            try:
                mapped = symbol[cols[1].text.strip()]
            except:
                continue
            if mapped in security_list:
                security_list.pop(security_list.index(mapped))
                dictionary[mapped] = {
                    'max_price':  cols[3].text.strip(),
                    'min_price': cols[4].text.strip(),
                    'closing_price': cols[5].text.strip(),
                    'traded_share': cols[6].text.strip(),
                    'amount': cols[7].text.strip(),
                    'previous_closing': cols[8].text.strip()
                }
                if float(dictionary[mapped]['max_price'])>=float(sec[sec['symbol']==mapped]['high'].iloc[0]):
                    message.append(f"Upper Bound breached by security <b>{mapped}</b> <br>")
    
                if float(dictionary[mapped]['min_price'])<=float(sec[sec['symbol']==mapped]['low'].iloc[0]):
                    message.append(f"Lower Bound breached by security <b>{mapped}</b> <br>")
            if len(security_list) == 0:
                break
        if len(security_list) == 0:
            break
    if len(message) != 0 :
        mail = Mail()
        mail.send(receiver_email, message)

if __name__ == '__main__':
    sec = pd.read_csv('security.csv')
    parser = argparse.ArgumentParser(description="Emails which are to be notified...")
    parser.add_argument(
        "--emails",
        dest="emails",
        default=None,
        help="example@email.com,another-example@email.com",
    )
    known_cmd, _ = parser.parse_known_args()
    emails = known_cmd.emails.split(',')
    get_data(sec, emails)
