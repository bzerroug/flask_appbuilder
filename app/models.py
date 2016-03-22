#from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
#from sqlalchemy.orm import relationship
from flask.ext.appbuilder import Model
#from app import db
import datetime
import logging

from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy import create_engine, func, and_, or_
from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orm import relationship
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy import inspect
#from SplunkExtract import process_compute_slot_filling

from flask import Flask
from flask.ext.appbuilder import SQLA, AppBuilder
#from flask.ext.babel import lazy_gettext

from firstScriptGA import getSessions

app = Flask(__name__)
app.config.from_pyfile('/Users/bzerroug/projects/first_app/config.py')
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

log = logging.getLogger(__name__)

#from flask.ext.appbuilder.security.registerviews import RegisterUserDBView
#from flask_appbuilder.security.sqla.manager import SecurityManager
#from .sec_models import MyUser
#from .sec_views import MyUserDBModelView



#insp = inspect(engine)
#columns = [ str(col['name']) for col in insp.get_columns('customer_stats')]
Now=datetime.datetime.now()

class orders(Model):
    __bind_key__ = 'postgresql'
    Base = automap_base()
    engine = create_engine('postgresql://dataware:phahvaTh4yua3ie@192.168.58.19:5432/dataware')

    Base.prepare(engine, reflect=True)
    Base.metadata.reflect(engine)
    __table__ = Base.metadata.tables['orders']
    
    
    def __repr__(self):
        return self.name

    def orders_int(self):
        if self.order_date > datetime.datetime(2016, 2, 1) and\
        self.delivery_model == 'LAD' and self.status == 11:
            return self

         

class customer_stats(Model):
    __bind_key__ = 'postgresql'
    Base = automap_base()
    engine = create_engine('postgresql://dataware:phahvaTh4yua3ie@192.168.58.19:5432/dataware')

    Base.prepare(engine, reflect=True)
    Base.metadata.reflect(engine)
    __table__ = Base.metadata.tables['customer_stats']
 
#Base = automap_base()

class slot_filling(Model):
    #__tablename__ = 'slots'
    id = Column(Integer, primary_key=True)
    csc = Column(String)
    date = Column(Date)    
    filling = Column(Float)
    
    
    def __repr__(self):
        return "{0}:{1}:{2}".format(self.csc, self.date, self.filling)
        
        
class THE_KPIS(Model):
    id = Column(Integer, primary_key=True)
    Date_de_Debut = Column(Date)
    Date_de_Fin = Column(Date)
    Numero_semaine = Column(Integer)
    Nombre_de_commandes = Column(Integer)
    CA = Column(Integer)
    Nombre_moyen_de_produits = Column(String)
    Panier_moyen = Column(String)
    Nombre_de_commandes_2015 = Column(Integer)
    CA_2015 = Column(Integer)
    Nombre_moyen_de_produits_2015 = Column(String)
    Panier_moyen_2015 = Column(String)
    #Variation
    
#    def Nombre_de_commandes(self):
#        date1=self.DateFin
#        date2=self.DateDebut
#        return int(list(db.session.query(func.count(orders.order_id))\
#        .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
#        orders.order_date < date1,\
#        orders.order_date > date2)))[0][0])
#    
#    def CA(self):
#        date1=self.DateFin
#        date2=self.DateDebut     
#        return str(int(list(db.session.query(func.sum(orders.amount))\
#        .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
#        orders.order_date < date1,\
#        orders.order_date > date2)))[0][0]))+' euros'
#
#        
#    def Nombre_moyen_de_produits(self):
#        date1=self.DateFin
#        date2=self.DateDebut   
#        return round(float(list(db.session.query(func.avg(orders.nb_items))\
#        .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
#        orders.order_date < date1,\
#        orders.order_date > date2)))[0][0]),2) 
#        
#    def Panier_moyen(self):
#        date1=self.DateFin
#        date2=self.DateDebut  
#        return str(round(float(list(db.session.query(func.avg(orders.amount))\
#        .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
#        orders.order_date < date1,\
#        orders.order_date > date2)))[0][0]),2))+' euros' 
#        
#    
#    def Nombre_de_commandesN_1(self):
#        date1=self.DateFin - datetime.timedelta(365)
#        date2=self.DateDebut - datetime.timedelta(365)
#        return int(list(db.session.query(func.count(orders.order_id))\
#        .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
#        orders.order_date < date1,\
#        orders.order_date > date2)))[0][0])
#    
#    def CAN_1(self):
#        date1=self.DateFin - datetime.timedelta(365)
#        date2=self.DateDebut - datetime.timedelta(365)  
#        return str(int(list(db.session.query(func.sum(orders.amount))\
#        .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
#        orders.order_date < date1,\
#        orders.order_date > date2)))[0][0]))+' euros'
#
#        
#    def Nombre_moyen_de_produitsN_1(self):
#        date1=self.DateFin - datetime.timedelta(365)
#        date2=self.DateDebut - datetime.timedelta(365)
#        return round(float(list(db.session.query(func.avg(orders.nb_items))\
#        .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
#        orders.order_date < date1,\
#        orders.order_date > date2)))[0][0]),2) 
#        
#    def Panier_moyenN_1(self):
#        date1=self.DateFin - datetime.timedelta(365)
#        date2=self.DateDebut - datetime.timedelta(365) 
#        return str(round(float(list(db.session.query(func.avg(orders.amount))\
#        .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
#        orders.order_date < date1,\
#        orders.order_date > date2)))[0][0]),2))+' euros'     
#    
    
    
    
    
    
class GA(Model):
    id = Column(Integer, primary_key=True)
    DateDebut = Column(Date)
    DateFin = Column(Date)
    Numero_semaine = Column(Integer)
    TTR_site = Column(Float)
    TTR_appli = Column(Float)

    
#    def TTR_site(self):
#        date1=self.DateDebut
#        date2=self.DateFin
#        
#        myquery4_site = db.session.query( func.count(orders.order_id) )\
#        .filter(and_(orders.order_date >= date1,\
#        orders.order_date <= date2, orders.modified_order_id.is_(None),\
#        or_(orders.device_type==2, orders.device_type==7))).all()    
#        
#        sessions_site = int(getSessions('97200935', date1.strftime('%Y-%m-%d'), date2.strftime('%Y-%m-%d')))
#        commandes_site = int(list(myquery4_site)[0][0])
#        TTR_site = commandes_site/float(sessions_site)
#        return TTR_site
#    
#    def TTR_appli(self):
#        date1=self.DateDebut
#        date2=self.DateFin
#        
#        myquery4_appli = db.session.query( func.count(orders.order_id) )\
#        .filter(and_(orders.order_date >= date1,\
#        orders.order_date <= date2, orders.modified_order_id.is_(None),\
#        or_(orders.device_type==6, orders.device_type==5))).all()
#        
#        sessions_appli = int(getSessions('97199161', date1.strftime('%Y-%m-%d'), date2.strftime('%Y-%m-%d')))
#        commandes_appli = int(list(myquery4_appli)[0][0])
#        TTR_appli = commandes_appli/float(sessions_appli)
#        return TTR_appli
    
class NbOrders(Model):
    id = Column(Integer, primary_key=True)
    Date_debut = Column(Date)
    Date_fin = Column(Date)
    No_de_magasin = Column(Integer)
    Number_of_orders = Column(Integer)
    
#    def Number_of_orders(self):
#        date1 = self.Date_debut
#        date2 = self.Date_fin
#        csc1 = self.No_de_magasin
#        myquery = db.session.query(func.count(orders.order_id))\
#        .filter(and_(orders.status != 1004, orders.csc == csc1,\
#        func.DATE(orders.order_date) >= date1, func.DATE(orders.order_date) <= date2))
#        
#        out = list(myquery)
#        return int(out[0][0])
        







