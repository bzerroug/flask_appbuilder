#import random
import logging
import pandas as pd
import datetime
#import calendar

from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder.views import ModelView
from flask.ext.appbuilder.actions import action
from flask_appbuilder.charts.views import DirectChartView, DirectByChartView, GroupByChartView
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask.ext.appbuilder import BaseView, expose, has_access
from flask import render_template, Flask
from flask.ext.appbuilder import SQLA, AppBuilder
#from flask_appbuilder.models.group import aggregate_count, aggregate_sum, aggregate_avg

from sqlalchemy import create_engine, func, and_, or_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


from firstScriptGA import getSessions
from .models import orders, customer_stats, slot_filling, THE_KPIS, GA, NbOrders
from . import appbuilder, db
from SplunkExtract import process_compute_slot_filling

from flask import g
#from FillData import fillMeteo, miseAjour


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

class ga(ModelView):
    datamodel = SQLAInterface(GA)
    list_columns = ['DateDebut', 'DateFin', 'Numero_semaine', 'TTR_site', 'TTR_appli']


class Nombre_de_commandes(ModelView):
    datamodel = SQLAInterface(NbOrders)
    list_columns = ['Date_debut', 'Date_fin', 'No_de_magasin', 'Number_of_orders']


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

                
        #return self.render_template('method.html', param1 = out2, param2=out3, param3=out4, param4=out5, param5=out6)
        out3 = pd.read_csv('Files/DF_slot_filling.csv', sep=';')
        del out3['Unnamed: 0']
        
        import csv
        with open('Files/out_kpis.csv', 'rb') as f:
            reader = csv.reader(f)
            out = map(tuple, reader)
        out2 = [out[0][i] for i in range(len(out[0]))]
        
        with open('Files/out_nb_com.csv', 'rb') as f:
            reader = csv.reader(f)
            out = map(tuple, reader)
        out5p = [out[0][i].strip('(').strip(')').split(',') for i in range(len(out[0]))]
        
        with open('Files/out_nb_com_today.csv', 'rb') as f:
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


        with open('Files/out_TTR.csv', 'rb') as f:
            reader = csv.reader(f)
            out = map(tuple, reader)
        out6 = [out[0][i] for i in range(len(out[0]))]



        
                
        return self.render_template('method1.html', param1 = out2, param2=out3, param3=out4, param4=out5, param5=out6)
        

	


db.create_all()
appbuilder.add_view(OrdersView, "list of orders", category="database")
appbuilder.add_view(CustomerStatsView, "list customer stats", category="database")
appbuilder.add_view(SlotFillingView, "Slot Filling", icon="fa-table", category="Views")
appbuilder.add_view(kpis, "kpis", icon="fa-table", category="Views")
appbuilder.add_view(ga, "TTR", icon="fa-table", category="Views")
appbuilder.add_view(Nombre_de_commandes, "Nombre de commandes", icon="fa-table", category="Views")

appbuilder.add_view(View, 'tables',icon="fa-folder-open-o", category="Meteo")
#appbuilder.add_view(View, "My View", category="My Forms")


#appbuilder.add_separator("Statistics")
#appbuilder.add_view(CountryStatsDirectChart, "Show Country Chart", icon="fa-dashboard", category="Statistics")
#appbuilder.add_view(CountryGroupByChartView, "Group Country Chart", icon="fa-dashboard", category="Statistics")
appbuilder.add_view(SlotFillingViewChart, 'Slot Filling Evolution', icon="fa-dashboard", category="Charts")
appbuilder.add_view(OrdersChart, 'Orders Evolution', icon="fa-dashboard", category="Charts")

