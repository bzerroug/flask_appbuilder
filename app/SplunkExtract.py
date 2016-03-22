import sys
from datetime import datetime, timedelta
from time import sleep
import splunklib.results as results
import splunklib.client as client
import pandas as pd
import sys
import logging
#import slacker

#from .. import parse_args, setup_logging

logger = logging.getLogger(__name__)


def process_compute_slot_filling(X):
    splunk_service=client.connect(host='94.124.133.189', port=8089, username='bzerroug', password='Bz3rr0ug')    
    
    logger.info('Computing slot filling')
    
    searchquery_normal = "search index=\"adfr_slot_wlec\" NoMagasin!=11225 max_capacity > 0 slot_day=2016* earliest=-"+str(X)+"d@d | eval modification_date=strptime(slot_day,\"%Y%m%d\") | eval new_date=strftime(modification_date,\"%Y/%m/%d\") |  sort 0 by _time | stats last(consumed_capacity) as consumed_capacity,last(max_capacity) as max_capacity by NoMagasin,slot_time,new_date | stats sum(consumed_capacity) as consumed_capacity,sum(max_capacity) as max_capacity by NoMagasin,new_date| eval cap = consumed_capacity/max_capacity | table NoMagasin, new_date, cap"

    kwargs_normalsearch = {"search_mode": "normal", "count": 0}
    
    job = splunk_service.jobs.create(searchquery_normal, **kwargs_normalsearch)
    
    while True:
        while not job.is_ready():
            pass
        stats = {"isDone": job["isDone"],
                 "eventAvailableCount": 0,
                 "doneProgress": float(job["doneProgress"])*100,
                  "scanCount": int(job["scanCount"]),
                  "eventCount": int(job["eventCount"]),
                  "resultCount": int(job["resultCount"])}
    
    
        status = ("\r%(doneProgress)03.1f%%   %(scanCount)d scanned   "
                  "%(eventCount)d matched   %(resultCount)d results") % stats
    
        sys.stdout.write(status)
        sys.stdout.flush()
        if stats["isDone"] == "1":
            sys.stdout.write("\n\nDone!\n\n")
            break
        sleep(1)
    
    # Get the results and display them
    current_time = datetime.now()
    printedList=[]
    for result in results.ResultsReader(job.results(**kwargs_normalsearch)):
        resultDay = dict(result)
        date=datetime.strptime(resultDay['new_date'], '%Y/%m/%d')
        if (current_time - date).days >= -1:
            printedList.append(resultDay)
    
    
    #print printedList
    #sys.stdout.write('\n')
    #print len(printedList)
    #sys.stdout.write('\n')
    
    df=pd.DataFrame()
    Dates=[]
    Csc=[]
    TauxDeRemplissage=[]
    for day in printedList:
        TauxDeRemplissage.append( round( float(day['cap'])*100,2 ) )
        csc='Morangis'
        if day['NoMagasin']== '11222':
            csc='VLG'
        elif day['NoMagasin']== '11223':
            csc='Bonneuil'
        elif day['NoMagasin']== '11224':
            csc='Mions'
        elif day['NoMagasin']== '11226':
            csc='Lille'
        elif day['NoMagasin']== '11227':
            csc='Marseille'
        Dates.append(str(day['new_date']))
        Csc.append(csc)
    
    df['Date'] = Dates
    df['No de magasin'] = Csc
    df['Taux de remplissage'] = TauxDeRemplissage



    return df
    


if __name__ == '__main__':

    #splunk_service = client.connect(host='94.124.133.189', port=8089, username='bzerroug', password='Bz3rr0ug')

    df2=process_compute_slot_filling(2)
    




