# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 12:37:10 2016

@author: bzerroug
"""

from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer, ForeignKey, String, Sequence, Table
from sqlalchemy.orm import relationship, backref
from flask_appbuilder import Model

class MyUser(User):
    extra = Column(String(256))