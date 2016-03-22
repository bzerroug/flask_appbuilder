# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 15:07:11 2016

@author: bzerroug
"""
import datetime
import pandas as pd
#import random
#from app import db
#import logging
from flask import Flask
from flask.ext.appbuilder import SQLA, AppBuilder
from models import slot_filling, GA, NbOrders, THE_KPIS, orders
from SplunkExtract import process_compute_slot_filling
from sqlalchemy import create_engine, func, and_, or_
from firstScriptGA import getSessions, get_TTR_site

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


#from sqlalchemy import create_engine, func, and_, or_
#from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orm import sessionmaker

#from app import appbuilder, db

app = Flask(__name__)
#app.config.from_pyfile('/Users/bzerroug/projects/first_app/config.py')
app.config.from_pyfile('/home/bzerroug/Virtualenvs/flask_project/flask_app/config.py')
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

#log = logging.getLogger(__name__)




def fillSotFilling(X):

    DF=process_compute_slot_filling(X)
    try:
        for i in range(len(DF)):
            sf=slot_filling()   
            sf.date = datetime.datetime.strptime(DF['Date'][i],'%Y/%m/%d').date()
            sf.csc = DF['No de magasin'][i]
            sf.filling = DF['Taux de remplissage'][i]
            db.session.add(sf)
            db.session.commit()
    except:
        #log.error("Update ViewMenu error: {0}".format(str(e)))
        db.session.rollback()
        
        


#######################################################################################################
#######################################################################################################
def Nombre_de_commandes(date2, date1):
    return int(list(db.session.query(func.count(orders.order_id))\
    .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
    orders.order_date < date1,\
    orders.order_date > date2)))[0][0])
    
def CA(date2, date1):
    return str(int(list(db.session.query(func.sum(orders.amount))\
    .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
    orders.order_date < date1,\
    orders.order_date > date2)))[0][0]))+' euros'

        
def Nombre_moyen_de_produits(date2, date1):  
    return round(float(list(db.session.query(func.avg(orders.nb_items))\
    .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
    orders.order_date < date1,\
    orders.order_date > date2)))[0][0]),2) 
    
def Panier_moyen(date2, date1):
    return str(round(float(list(db.session.query(func.avg(orders.amount))\
    .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
    orders.order_date < date1,\
    orders.order_date > date2)))[0][0]),2))+' euros' 
    

def Nombre_de_commandesN_1(date2, date1):
    date1=date1 - datetime.timedelta(365)
    date2=date2 - datetime.timedelta(365)    
    return int(list(db.session.query(func.count(orders.order_id))\
    .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
    orders.order_date < date1,\
    orders.order_date > date2)))[0][0])

def CAN_1(date2, date1):
    date1=date1 - datetime.timedelta(365)
    date2=date2 - datetime.timedelta(365)    
    return str(int(list(db.session.query(func.sum(orders.amount))\
    .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
    orders.order_date < date1,\
    orders.order_date > date2)))[0][0]))+' euros'

    
def Nombre_moyen_de_produitsN_1(date2, date1):
    date1=date1 - datetime.timedelta(365)
    date2=date2 - datetime.timedelta(365)  
    return round(float(list(db.session.query(func.avg(orders.nb_items))\
    .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
    orders.order_date < date1,\
    orders.order_date > date2)))[0][0]),2) 
    
def Panier_moyenN_1(date2, date1):
    date1=date1 - datetime.timedelta(365)
    date2=date2 - datetime.timedelta(365) 
    return str(round(float(list(db.session.query(func.avg(orders.amount))\
    .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
    orders.order_date < date1,\
    orders.order_date > date2)))[0][0]),2))+' euros'     
    


def fillKPIS():
    all_dates = [datetime.datetime(2016,1,4).date()]
    for i in range(11):
        k=i+1
        all_dates.append( (datetime.datetime(2016,1,4)+datetime.timedelta(k*7)).date() )
        
    for j in range(len(all_dates)-1):
        date1 = all_dates[j]
        date2 = all_dates[j+1]
        #try:
        kpis1=THE_KPIS()
        kpis1.Date_de_Debut = date1
        kpis1.Date_de_Fin = date2
        kpis1.Numero_semaine = date1.isocalendar()[1]
        kpis1.Nombre_de_commandes = Nombre_de_commandes(date1, date2)
        kpis1.CA = CA(date1, date2)
        kpis1.Nombre_moyen_de_produits = Nombre_moyen_de_produits(date1, date2)
        kpis1.Panier_moyen = Panier_moyen(date1, date2)
        kpis1.Nombre_de_commandes_2015 = Nombre_de_commandesN_1(date1, date2)
        kpis1.CA_2015 = CAN_1(date1, date2)
        kpis1.Nombre_moyen_de_produits_2015 = Nombre_moyen_de_produitsN_1(date1, date2)
        kpis1.Panier_moyen_2015 = Panier_moyenN_1(date1, date2)
        db.session.add(kpis1)
        db.session.commit()
        print date1
        #except:# Exception as e:
#        log.error("Update ViewMenu error: {0}".format(str(e)))
         #   db.session.rollback()





#######################################################################################################
#######################################################################################################




def Number_of_orders(date1, date2, csc1):
    #date1 = self.Date_debut
    #date2 = self.Date_fin
    #csc1 = self.No_de_magasin
    myquery = db.session.query(func.count(orders.order_id))\
    .filter(and_(orders.status != 1004, orders.csc == csc1,\
    func.DATE(orders.order_date) >= date1, func.DATE(orders.order_date) <= date2))
        
    out = list(myquery)
    return int(out[0][0])

def fillDataNbCom():
    all_dates = [datetime.datetime(2015,1,1)]
    for i in range(442):
        k=i+1
        all_dates.append( (datetime.datetime(2016,1,1)+datetime.timedelta(k)).date() )
        
    for Date in all_dates:
        for CSC in [11121, 11222, 11223, 11224, 11226, 11227]:
            #myquery = db.session.query(orders.csc, func.count(orders.order_id))\
            #.filter(and_(orders.status != 1004, orders.csc==CSC,\
            #func.DATE(orders.order_date) == Date)).group_by(orders.csc)
            N = Number_of_orders(Date, Date + datetime.timedelta(1), CSC)            
            try:
                norders=NbOrders() 
                norders.Date_debut = Date
                norders.Date_fin = Date + datetime.timedelta(1)
                norders.No_de_magasin = CSC
                norders.Number_of_orders = N
                print N
                db.session.add(norders)
                db.session.commit()
            except:
                #log.error("Update ViewMenu error: {0}".format(str(e)))
                db.session.rollback() 
 



#######################################################################################################
#######################################################################################################

def TTR_site(date1, date2):
    #date1=self.DateDebut
    #date2=self.DateFin
        
    myquery4_site = db.session.query( func.count(orders.order_id) )\
    .filter(and_(orders.order_date >= date1,\
    orders.order_date <= date2, orders.modified_order_id.is_(None),\
    or_(orders.device_type==2, orders.device_type==7))).all()    
        
    sessions_site = int(getSessions('97200935', date1.strftime('%Y-%m-%d'), date2.strftime('%Y-%m-%d')))
    commandes_site = int(list(myquery4_site)[0][0])
    TTR_site = commandes_site/float(sessions_site)
    return TTR_site
    
def TTR_appli(date1, date2):
    #date1=self.DateDebut
    #date2=self.DateFin
    #import datetime
        
    myquery4_appli = db.session.query( func.count(orders.order_id) )\
    .filter(and_(orders.order_date >= date1,\
    orders.order_date <= date2, orders.modified_order_id.is_(None),\
    or_(orders.device_type==6, orders.device_type==5))).all()
        
    sessions_appli = int(getSessions('97198927', date1.strftime('%Y-%m-%d'), date2.strftime('%Y-%m-%d')))
    commandes_appli = int(list(myquery4_appli)[0][0])
    TTR_appli = commandes_appli/float(sessions_appli)
    return TTR_appli   

def fillGA():
    all_dates = [datetime.datetime(2015,3,9).date()]
    for i in range(53):
        k=i+1
        all_dates.append( (datetime.datetime(2015,3,9)+datetime.timedelta(k*7)).date() )
        
    for j in range(len(all_dates)-1):
        Date1=all_dates[j]
        Date2=all_dates[j+1]
        appli=TTR_appli(Date1, Date2)
        site=TTR_site(Date1, Date2)
        print Date1
        try:
            ttr=GA() 
            ttr.DateDebut = Date1
            ttr.DateFin = Date2
            ttr.Numero_semaine = Date1.isocalendar()[1]
            ttr.TTR_site = site
            ttr.TTR_appli = appli
            db.session.add(ttr)
            db.session.commit()
        except:
            #log.error("Update ViewMenu error: {0}".format(str(e)))
            db.session.rollback() 
   
 
#######################################################################################################
#######################################################################################################

#Base = automap_base()
#engine = create_engine('postgresql://dataware:phahvaTh4yua3ie@192.168.58.19:5432/dataware')
#Base.prepare(engine, reflect=True)        
#orders = Base.classes.orders
#session = sessionmaker(bind=engine)()    

def fillMeteo():
    #remplissage des slots
    #from decimal import Decimal
    DF = process_compute_slot_filling(0)
    if len(DF) <= 6:
        L_mag = list(DF['No de magasin'])
        L_date = list(DF['Date'])
        L_remp = list(DF['Taux de remplissage'])
        X=datetime.datetime.strptime(DF['Date'][0], '%Y/%m/%d')
        date = (X+datetime.timedelta(1)).strftime('%Y/%m/%d')
        for i in range(len(L_mag)):
            L_mag.append(DF['No de magasin'][i])
            L_date.append(date)
            L_remp.append(0)
        dic={}
        dic['Date']=L_date
        dic['No de magasin']=L_mag
        dic['Taux de remplissage']=L_remp
        DF_slot_filling = pd.DataFrame(dic)
    else:
        DF_slot_filling = DF
    
    #KPIS des 7 derniers jours    
    myquery = db.session.query(func.count(orders.order_id), func.sum(orders.amount), func.avg(orders.nb_items), func.avg(orders.amount))\
    .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
    func.DATE(orders.order_date) <= (datetime.datetime.now()-datetime.timedelta(1)).date(),\
    func.DATE(orders.order_date) >= (datetime.datetime.now()-datetime.timedelta(7)).date()))
    
    myquery2015 = db.session.query(func.count(orders.order_id), func.sum(orders.amount), func.avg(orders.nb_items), func.avg(orders.amount))\
    .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
    func.DATE(orders.order_date) <= (datetime.datetime.now()-datetime.timedelta(days=1, weeks=52)).date(),\
    func.DATE(orders.order_date) >= (datetime.datetime.now()-datetime.timedelta(days=7, weeks=52)).date()))
    
    out_2015 = list(myquery2015)
    out = list(myquery)
    out2=[]
    
    out2.append(out[0][0])
    out2.append( str(int(round((-float(out_2015[0][0])+float(out[0][0]))/float(out_2015[0][0]),2)*100))+' %' )
    out2.append(str(int(out[0][1]))+' Euros')
    out2.append( str(int(round((-float(out_2015[0][1])+float(out[0][1]))/float(out_2015[0][1]),2)*100))+' %' )
    out2.append(round(out[0][2],1))
    out2.append( str(int(round((-float(out_2015[0][2])+float(out[0][2]))/float(out_2015[0][2]),2)*100))+' %' )
    out2.append(str(round(out[0][3],2))+' Euros')
    out2.append( str(int(round((-float(out_2015[0][3])+float(out[0][3]))/float(out_2015[0][3]),2)*100))+' %' )
        
    out_kpis=out2

    
    #Nombre de commandes des 3 derniers jours    
    myquery2 = db.session.query(orders.csc, func.count(orders.order_id))\
    .filter(and_(orders.status != 1004,\
    orders.order_date >= (datetime.datetime.now().date()-datetime.timedelta(days=4)),\
    orders.order_date <= datetime.datetime.now().date()-datetime.timedelta(days=1))).group_by(orders.csc)
    
    myquery22015 = db.session.query(orders.csc, func.count(orders.order_id))\
    .filter(and_(orders.status != 1004,\
    orders.order_date >= (datetime.datetime.now().date()-datetime.timedelta(days=4, weeks=52)),\
    orders.order_date <= (datetime.datetime.now().date()-datetime.timedelta(days=1, weeks=52)))).group_by(orders.csc)
    
    out = list(myquery2)
    out_2015 = list(myquery22015)
    out4=[]
    for elem in out:
        for elem2015 in out_2015:
            if elem[0] == 11121 and elem2015[0] == 11121:
                out4.append(('Morangis',int(elem[1]), str(int(round((-elem2015[1]+elem[1])/float(elem2015[1]),2)*100))+' %'))
            if elem[0] == 11222 and elem2015[0] == 11222:
                 out4.append(('VLG',int(elem[1]), str(int(round((-elem2015[1]+elem[1])/float(elem2015[1]),2)*100))+' %'))
            if elem[0] == 11223 and elem2015[0] == 11223:
                  out4.append(('Bonneuil',int(elem[1]), str(int(round((-elem2015[1]+elem[1])/float(elem2015[1]),2)*100))+' %'))
            if elem[0] == 11224 and elem2015[0] == 11224:
                  out4.append(('Mions',int(elem[1]), str(int(round((-elem2015[1]+elem[1])/float(elem2015[1]),2)*100))+' %'))
            if elem[0] == 11226 and elem2015[0] == 11226:
                   out4.append(('Lille',int(elem[1]),str(int(round((-elem2015[1]+elem[1])/float(elem2015[1]),2)*100))+' %'))
            if elem[0] == 11227 and elem2015[0] == 11227:
                   out4.append(('Marseille',int(elem[1]), str(int(round((-elem2015[1]+elem[1])/float(elem2015[1]),2)*100))+' %'))
            
    out4.append(('Total', int(sum([ x[1] for x in out])), str(int(round((-sum([ x[1] for x in out_2015])+sum([ x[1] for x in out]))/float(sum([ x[1] for x in out_2015])),2)*100))+' %'))
    out_nb_com = out4
     
    #Nombre de commandes d'aujourd'hui

    myquery3 = db.session.query(orders.csc, func.count(orders.order_id))\
    .filter(and_(orders.status != 1004,\
    func.DATE(orders.order_date) == datetime.datetime.now().date()-datetime.timedelta(days=1))).group_by(orders.csc)
    
    myquery32015 = db.session.query(orders.csc, func.count(orders.order_id))\
    .filter(and_(orders.status != 1004,\
    func.DATE(orders.order_date) == (datetime.datetime.now().date()-datetime.timedelta(days=1, weeks=53)))).group_by(orders.csc)    
    
    out = list(myquery3)
    out_2015 = list(myquery32015)
    out5=[]
    for elem in out:
        if elem[0] == 11121:
            out5.append(('Morangis',int(elem[1]), str(int(round((-out_2015[0][1]+out[0][1])/float(out_2015[0][1]),2)*100))+' %'))
        if elem[0] == 11222:
             out5.append(('VLG',int(elem[1]), str(int(round((-out_2015[1][1]+out[1][1])/float(out_2015[1][1]),2)*100))+' %'))
        if elem[0] == 11223:
              out5.append(('Bonneuil',int(elem[1]), str(int(round((-out_2015[2][1]+out[2][1])/float(out_2015[2][1]),2)*100))+' %'))
        if elem[0] == 11224:
              out5.append(('Mions',int(elem[1]), str(int(round((-out_2015[3][1]+out[3][1])/float(out_2015[3][1]),2)*100))+' %'))
        if elem[0] == 11226:
               out5.append(('Lille',int(elem[1]),str(int(round((-out_2015[4][1]+out[4][1])/float(out_2015[4][1]),2)*100))+' %'))
        if elem[0] == 11227:
               out5.append(('Marseille',int(elem[1]), str(int(round((-out_2015[5][1]+out[5][1])/float(out_2015[5][1]),2)*100))+' %'))

    out5.append(('Total', int(sum([ x[1] for x in out])), str(int(round((-sum([ x[1] for x in out_2015])+sum([ x[1] for x in out]))/float(sum([ x[1] for x in out_2015])),2)*100))+' %'))    
    out_nb_com_today = out5
        
    
    #TTR    
    
    myquery4_appli = db.session.query( func.count(orders.order_id) )\
    .filter(and_(orders.order_date >= (datetime.datetime.now()-datetime.timedelta(7)),\
    orders.order_date <= datetime.datetime.now(), orders.modified_order_id.is_(None),\
    or_(orders.device_type==6, orders.device_type==5))).all()
    
    #myquery4_site = db.session.query( func.count(orders.order_id) )\
    #.filter(and_(orders.order_date >= (datetime.datetime.now()-datetime.timedelta(7)),\
    #orders.order_date <= datetime.datetime.now(), orders.modified_order_id.is_(None),\
    #or_(orders.device_type==2, orders.device_type==7))).all()
    
    N=datetime.datetime.now()
    N1=datetime.datetime.now()-datetime.timedelta(7)        
    
    sessions_appli = int(getSessions('97199161', N1.strftime('%Y-%m-%d'), N.strftime('%Y-%m-%d')))
    commandes_appli = int(list(myquery4_appli)[0][0])
    #sessions_site = int(getSessions('97200935', N1.strftime('%Y-%m-%d'), N.strftime('%Y-%m-%d')))
    #commandes_site = int(list(myquery4_site)[0][0])
    TTR_site = get_TTR_site('97200935', N1.strftime('%Y-%m-%d'), N.strftime('%Y-%m-%d')).get('rows')[0][0]
    TTR_appli = commandes_appli/float(sessions_appli)
    
    out6=[str(round(float(TTR_site),2))+' %', str(round(TTR_appli,4)*100)+' %']
    out_TTR = out6
    
    
    #Exports Files
        
    import csv
    
    DF_slot_filling.to_csv('/Users/bzerroug/projects/first_app/Files/DF_slot_filling.csv', sep=';')
    
    with open('/Users/bzerroug/projects/first_app/Files/out_kpis.csv', 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(out_kpis)
    with open('/Users/bzerroug/projects/first_app/Files/out_nb_com.csv', 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(out_nb_com)
    with open('/Users/bzerroug/projects/first_app/Files/out_TTR.csv', 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(out_TTR)
    with open('/Users/bzerroug/projects/first_app/Files/out_nb_com_today.csv', 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(out_nb_com_today)

#######################################################################################################
#######################################################################################################

def miseAjour():

#    DF=process_compute_slot_filling(4)
#    
#    try:
#        for i in range(len(DF)):
#            if DF['Taux de remplissage'][i] > 0.7:
#                sf=slot_filling()   
#                sf.date = datetime.datetime.strptime(DF['Date'][i],'%Y/%m/%d').date()
#                sf.csc = DF['No de magasin'][i]
#                sf.filling = DF['Taux de remplissage'][i]
#                db.session.add(sf)
#                db.session.commit()
#    except:
#        #log.error("Update ViewMenu error: {0}".format(str(e)))
#        db.session.rollback()
#
#    Date1=(datetime.datetime.now()-datetime.timedelta(7)).date()
#    Date2=datetime.datetime.now().date()
#    appli=TTR_appli(Date1, Date2)
#    site=TTR_site(Date1, Date2)
#    print Date1
#    try:
#        ttr=GA() 
#        ttr.DateDebut = Date1
#        ttr.DateFin = Date2
#        ttr.Numero_semaine = Date1.isocalendar()[1]
#        ttr.TTR_site = site
#        ttr.TTR_appli = appli
#        db.session.add(ttr)
#        db.session.commit()
#    except:
#        #log.error("Update ViewMenu error: {0}".format(str(e)))
#        db.session.rollback()         
        
    dates = [(datetime.datetime.now()-datetime.timedelta(2)).date(), (datetime.datetime.now()-datetime.timedelta(1)).date(), datetime.datetime.now().date()]
    
    #Nombre_de_commandes(date2, date1)
    #for i in range(len(dates)-1):
    #    date1=dates[i]
    #    date2=dates[i]+ datetime.timedelta(1)
        
    for Date in dates:
        for CSC in [11121, 11222, 11223, 11224, 11226, 11227]:
            #myquery = db.session.query(orders.csc, func.count(orders.order_id))\
            #.filter(and_(orders.status != 1004, orders.csc==CSC,\
            #func.DATE(orders.order_date) == Date)).group_by(orders.csc)
            N = Number_of_orders(Date, Date + datetime.timedelta(1), CSC)            
            try:
                norders=NbOrders() 
                norders.Date_debut = Date
                norders.Date_fin = Date + datetime.timedelta(1)
                norders.No_de_magasin = CSC
                norders.Number_of_orders = N
                print N
                db.session.add(norders)
                db.session.commit()
            except:
                #log.error("Update ViewMenu error: {0}".format(str(e)))
                db.session.rollback() 
     




    
    
    
    
#######################################################################################################
#######################################################################################################
   
if __name__ == '__main__':
    #fillDataNbCom()
    #fillData(1000)
    #fillGA()
    #fillKPIS()
    fillMeteo()
    #miseAjour()
#date1=datetime.datetime(2015,3,9).date()
#date2=datetime.datetime(2015,3,16).date()
#myquery4_appli = db.session.query( func.count(orders.order_id) )\
#.filter(and_(orders.order_date >= date1,\
#orders.order_date <= date2, orders.modified_order_id.is_(None),\
#or_(orders.device_type==6, orders.device_type==5))).all()
#        
#sessions_appli = int(getSessions('97199161', date1.strftime('%Y-%m-%d'), date2.strftime('%Y-%m-%d')))
#commandes_appli = int(list(myquery4_appli)[0][0])
#TTR_appli = commandes_appli/float(sessions_appli)
#return TTR_appli   
    
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    
    
    
    
    
    
    