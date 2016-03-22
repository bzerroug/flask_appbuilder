#import random
import logging
import datetime
import pandas as pd
#import calendar

from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder.views import ModelView
#from flask.ext.appbuilder.actions import action
from flask_appbuilder.charts.views import DirectChartView#, DirectByChartView, GroupByChartView
#from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask.ext.appbuilder import BaseView, expose#, has_access
#from flask import render_template, Flask
#from flask.ext.appbuilder import SQLA, AppBuilder
#from flask_appbuilder.models.group import aggregate_count, aggregate_sum, aggregate_avg

from sqlalchemy import create_engine, func, and_, or_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


from firstScriptGA import getSessions
from models import orders, customer_stats, slot_filling, THE_KPIS, GA, NbOrders
from app import appbuilder, db
from SplunkExtract import process_compute_slot_filling

#from flask import g

#app = Flask(__name__)
#app.config.from_pyfile('/Users/bzerroug/projects/first_app/config.py')
#db = SQLA(app)
#appbuilder = AppBuilder(app, db.session)


log = logging.getLogger(__name__)




class OrdersView(ModelView):
    datamodel = SQLAInterface(orders)
    list_columns = ['order_id','order_id_wlec','customer_id','csc','order_date','delivery_date',\
    'amount', 'service_charge','theoric_service_charge', 'discount','status','delivery_model',\
    'last_update', 'nb_items','zip_code','delivery_truck','lost_revenue','margin','bill_lines_avail',\
    'billed_amount','billed_discount','order_lines_avail','modified_order_id','payment_type_code',\
    'device_type','order_rank']
    

    
class CustomerStatsView(ModelView):
    datamodel = SQLAInterface(customer_stats)
    list_columns = ['customer_id','total_orders','total_amount','first_order_date','last_order_date',\
    'total_discounts','total_items','recency','customer_age', 'orders_last_7days', 'orders_last_30days',\
    'orders_last_120days','expected_orders_365_days','proba_not_churned','avg_profit_per_order','clv_365',\
    'row_eff_date','CLV_seg','active_basket_flag','comport_seg','lost_revenue','nb_orders_with_missing','pseudoRF_seg']
    
    

class SlotFillingView(ModelView):
    datamodel = SQLAInterface(slot_filling)
    list_columns = ['date', 'csc', 'filling']
    #base_permissions = ['can_show','can_add']


class SlotFillingViewChart(DirectChartView):
    datamodel = SQLAInterface(slot_filling)
    chart_title = 'Slot filling evolution'
    chart_type = 'LineChart'
    direct_columns = {'General Stats': ('date', 'filling')}
    base_order = ('date', 'asc')
    
    
class kpis(ModelView):
    datamodel = SQLAInterface(THE_KPIS)
    list_columns = ['Date_de_Debut', 'Date_de_Fin', 'Numero_semaine', 'Nombre_de_commandes', 'CA', 'Nombre_moyen_de_produits', 'Panier_moyen'\
    , 'Nombre_de_commandes_2015', 'CA_2015', 'Nombre_moyen_de_produits_2015', 'Panier_moyen_2015']
    #base_permissions = ['can_show','can_add']

class ga(ModelView):
    datamodel = SQLAInterface(GA)
    list_columns = ['DateDebut', 'DateFin', 'Numero_semaine', 'TTR_site', 'TTR_appli']
    #base_permissions = ['can_show','can_add']

class Nombre_de_commandes(ModelView):
    datamodel = SQLAInterface(NbOrders)
    list_columns = ['Date_debut', 'Date_fin', 'No_de_magasin', 'Number_of_orders']
    #base_permissions = ['can_show','can_add']

class OrdersChart(DirectChartView):
    datamodel = SQLAInterface(NbOrders)
    chart_title = 'Number of orders evolution'
    chart_type = 'LineChart'
        
    direct_columns = {'General Stats': ('Date_debut', 'Number_of_orders')}
    base_order = ('Date_debut', 'asc')


class View(BaseView):
    default_view = 'method1'


                    
    @expose('/method1/')  
    def method1(self):  
#        Base = automap_base()
#        engine = create_engine('postgresql://dataware:phahvaTh4yua3ie@192.168.58.19:5432/dataware')
#        Base.prepare(engine, reflect=True)        
#        #orders = Base.classes.orders
#        session = sessionmaker(bind=engine)()        
#        
#        myquery = session.query(func.count(orders.order_id), func.sum(orders.amount), func.avg(orders.nb_items), func.avg(orders.amount))\
#        .filter(and_(orders.status == 11, orders.delivery_model == 'LAD',\
#        orders.order_date < datetime.datetime.now(),\
#        orders.order_date > (datetime.datetime.now()-datetime.timedelta(7))))
#        
#        out = list(myquery)
#        out2=[]
#    
#        out2.append(out[0][0])
#        out2.append(str(int(out[0][1]))+' Euros')
#        out2.append(round(out[0][2],1))
#        out2.append(str(round(out[0][3],2))+' Euros')
#        
#        out3=process_compute_slot_filling(10)
#        
#        myquery2 = session.query(orders.csc, func.count(orders.order_id))\
#        .filter(and_(orders.status != 1004,\
#        func.DATE(orders.order_date) == datetime.datetime.now().date())).group_by(orders.csc)
#        
#        out = list(myquery2)
#        out4=[]
#        for elem in out:
#            if elem[0] == 11121:
#                out4.append(('Morangis',int(elem[1])))
#            if elem[0] == 11222:
#                 out4.append(('VLG',int(elem[1])))
#            if elem[0] == 11223:
#                  out4.append(('Bonneuil',int(elem[1]))) 
#            if elem[0] == 11224:
#                  out4.append(('Mions',int(elem[1])))
#            if elem[0] == 11226:
#                   out4.append(('Lille',int(elem[1])))
#            if elem[0] == 11227:
#                   out4.append(('Marseille',int(elem[1])))
#        out4.append(('Total', int(sum([ x[1] for x in out]))))
#        
#        myquery3 = session.query(orders.csc, func.count(orders.order_id))\
#        .filter(and_(orders.status != 1004,\
#        func.DATE(orders.order_date) >= (datetime.datetime.now().date()-datetime.timedelta(3)))).group_by(orders.csc)
#        
#        out = list(myquery3)
#        out5=[]
#        for elem in out:
#            if elem[0] == 11121:
#                out5.append(('Morangis',elem[1]))
#            if elem[0] == 11222:
#                out5.append(('VLG',elem[1]))
#            if elem[0] == 11223:
#                out5.append(('Bonneuil',elem[1])) 
#            if elem[0] == 11224:
#                out5.append(('Mions',elem[1]))
#            if elem[0] == 11226:
#                out5.append(('Lille',elem[1]))
#            if elem[0] == 11227:
#                out5.append(('Marseille',elem[1]))
#        out5.append(('Total', sum([ x[1] for x in out])))
#        
#        myquery4_appli = session.query( func.count(orders.order_id) )\
#        .filter(and_(orders.order_date >= (datetime.datetime.now()-datetime.timedelta(7)),\
#        orders.order_date <= datetime.datetime.now(), orders.modified_order_id.is_(None),\
#        or_(orders.device_type==6, orders.device_type==5))).all()
#        
#        myquery4_site = session.query( func.count(orders.order_id) )\
#        .filter(and_(orders.order_date >= (datetime.datetime.now()-datetime.timedelta(7)),\
#        orders.order_date <= datetime.datetime.now(), orders.modified_order_id.is_(None),\
#        or_(orders.device_type==2, orders.device_type==7))).all()
#        
#        N=datetime.datetime.now()
#        N1=datetime.datetime.now()-datetime.timedelta(7)        
#        
#        sessions_appli = int(getSessions('97199161', N1.strftime('%Y-%m-%d'), N.strftime('%Y-%m-%d')))
#        commandes_appli = int(list(myquery4_appli)[0][0])
#        sessions_site = int(getSessions('97200935', N1.strftime('%Y-%m-%d'), N.strftime('%Y-%m-%d')))
#        commandes_site = int(list(myquery4_site)[0][0])
#        TTR_site = commandes_site/float(sessions_site)
#        TTR_appli = commandes_appli/float(sessions_appli)
#        
#        out6=[str(round(TTR_site,4)*100)+' %', str(round(TTR_appli,4)*100)+' %']
        
        out3 = pd.read_csv('/Users/bzerroug/projects/first_app/Files/DF_slot_filling.csv', sep=';')
        del out3['Unnamed: 0']
        
        import csv
        with open('/Users/bzerroug/projects/first_app/Files/out_kpis.csv', 'rb') as f:
            reader = csv.reader(f)
            out = map(tuple, reader)
        out2 = [out[0][i] for i in range(len(out[0]))]
        
        with open('/Users/bzerroug/projects/first_app/Files/out_nb_com.csv', 'rb') as f:
            reader = csv.reader(f)
            out = map(tuple, reader)
        out5p = [out[0][i].strip('(').strip(')').split(',') for i in range(len(out[0]))]
        
        with open('/Users/bzerroug/projects/first_app/Files/out_nb_com_today.csv', 'rb') as f:
            reader = csv.reader(f)
            out = map(tuple, reader)
        out4p = [out[0][i].strip('(').strip(')').split(',') for i in range(len(out[0]))]
        out4=[]
        out5=[]     
        for i in range(len(out4p)):
            s=[]
            s1=[]
            for j in range(3):
                if j == 0:
                    s.append( out4p[i][j][1:-1] )
                    s1.append( out5p[i][j][1:-1] )
                elif j==2:
                    s.append( out4p[i][j][2:-1] )
                    s1.append( out5p[i][j][2:-1] )
                else:
                    s.append(out4p[i][j])
                    s1.append(out5p[i][j])
            out4.append(s)
            out5.append(s1)


        with open('/Users/bzerroug/projects/first_app/Files/out_TTR.csv', 'rb') as f:
            reader = csv.reader(f)
            out = map(tuple, reader)
        out6 = [out[0][i] for i in range(len(out[0]))]



        
                
        return self.render_template('method.html', param1 = out2, param2=out3, param3=out4, param4=out5, param5=out6)
        












#class View(BaseView):
#    @expose('/')   
#    def method1(self):
    

db.create_all()
appbuilder.add_view(OrdersView, "list of orders", category="database")
appbuilder.add_view(CustomerStatsView, "list customer stats", category="database")
appbuilder.add_view(SlotFillingView, "Slot Filling", category="Views")
appbuilder.add_view(kpis, "kpis", category="Views")
appbuilder.add_view(ga, "TTR", category="Views")
appbuilder.add_view(Nombre_de_commandes, "Nombre de commandes", category="Views")

appbuilder.add_view(View, "first_view", category="meteo")
#appbuilder.add_view(View, "My View", category="My Forms")


#appbuilder.add_separator("Statistics")
#appbuilder.add_view(CountryStatsDirectChart, "Show Country Chart", icon="fa-dashboard", category="Statistics")
#appbuilder.add_view(CountryGroupByChartView, "Group Country Chart", icon="fa-dashboard", category="Statistics")
appbuilder.add_view(SlotFillingViewChart, 'Slot Filling Evolution', icon="fa-dashboard", category="Charts")
appbuilder.add_view(OrdersChart, 'Orders Evolution', icon="fa-dashboard", category="Charts")
