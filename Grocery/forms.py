# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 20:30:12 2021

@author: 91902
"""
from Grocery.models import Item,User
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,EqualTo,DataRequired,ValidationError


class RegisterForm(FlaskForm):
    
    def validate_username(self,utc):
        user=User.query.filter_by(username=utc.data).first()
        if(user):
            raise ValidationError('USERNAME ALREADY EXIST ! PLEASE TRY NEW USERNAME')
        
    
    username=StringField(label='Username:',validators=[Length(min=5,max=30),DataRequired()])
    password1=PasswordField(label='Password:',validators=[Length(min=5),DataRequired()])
    password2=PasswordField(label='Confirm Password:',validators=[EqualTo('password1'),DataRequired()])
    submit=SubmitField(label='CREATE ACCOUNT')
        
class LoginForm(FlaskForm):

    
    def validate_username(self,utc):
        user=User.query.filter_by(username=utc.data).first()
        if(not user):
            raise ValidationError("Username doesn't exist")

    
    username=StringField(label='Username:',validators=[DataRequired()])
    password=PasswordField(label='Password:',validators=[DataRequired()])
    submit=SubmitField(label='Login')
    
class PurchaseItemForm(FlaskForm):
    
     submit=SubmitField(label="PURCHASE ITEM !")
     
    
    
class SellItemForm(FlaskForm):
    
     submit=SubmitField(label="SELL ITEM !")