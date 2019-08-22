import pandas as pd
from dateutil.parser import _resultbase
from sodapy import Socrata
import database as db
import time
import urllib.request
import filer
import json


taglist = ['email', 'e_mail', 'email_1', 'email_2',
            'mail_autonomia', 'mail_sede', 'indirizzo_e_mail_autonomia',
            'indirizzo_e_mail_sede_corsi']


def json_url_query(url_string):

    start_time = time.time()

    with urllib.request.urlopen(url_string) as url:
        print('Downloading json file...')
        data = json.loads(url.read().decode())
        print('extracting mails...')
        tmp = filer.jsonlist(data)

        if tmp is not None:
            print('mails founded')
            db.addiscritti(tmp)
            print('added to db.')
        else:
            print('Founded nothing')

    print('----------- Time elapsed : ', round(time.time() - start_time, 6), '----------')


def downloader(client, dataset_id, taglist):

    results = []
    LIMIT = 50000

    for columntag in taglist:
        try:
            print('Trying column :', columntag)
            # default type json
            offset = 0

            while True:
                tmp = client.get(dataset_id,
                                content_type="json",
                                limit=LIMIT,
                                offset=offset,
                                select=columntag)#,
                                #where='classificazione = "Paritaria"')
                results += tmp
                offset += LIMIT
                if not tmp:
                    break
            print('Founded something')

        except Exception as ex:
            print('Exception : ', ex)

    if not results:
        return None
    return results


# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
def downloadata(domain, dataset_id, app_token):

    start_time = time.time()

    client = Socrata(domain, app_token)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(www.dati.lombardia.it,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")

    print('Querying opendata emails...')
    results = downloader(client, dataset_id, taglist)
    if results is not None:
        # Convert to pandas DataFrame
        results_df = pd.DataFrame.from_records(results)
        print('converting mail format')
        tmp = results_df.iloc[:, 0]

        # Convert to list
        mail_list = list(tmp[tmp.notna()])

        # Add iscritti to newsletter
        print('Saving to db')

        db.addiscritti(mail_list)
        print('Done')
    else:
        print('No data written')
    client.close()

    print('----------- Time elapsed : ', round(time.time() - start_time, 6), '----------')

    return
