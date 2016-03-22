# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 12:39:11 2016

@author: bzerroug
"""

from flask_appbuilder.security.sqla.manager import SecurityManager
from .sec_models import MyUser
from .sec_views import MyUserDBModelView

class MySecurityManager(SecurityManager):
    user_model = MyUser
    userdbmodelview = MyUserDBModelView