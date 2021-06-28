# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 14:38:36 2021

@author: 91902
"""
from Grocery import db

from Grocery import app
from flask import render_template,redirect,url_for,flash,get_flashed_messages,request
from Grocery.models import Item,User
from Grocery.forms import RegisterForm,LoginForm,PurchaseItemForm,SellItemForm
from flask_login import login_user,logout_user,login_required,current_user

@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def home_page():
    return render_template('home.html')


@app.route('/market',methods=['GET','POST'])
@login_required
def market_page():
    form=PurchaseItemForm()
    selling_form=SellItemForm()
    if request.method=="POST":
        purchased_item=request.form.get('purchased_item')
        p_item=Item.query.filter_by(name=purchased_item).first()
        
        if p_item:
            if current_user.can_purchase(p_item):
                p_item.buy(current_user)
                
                flash("YOU HAVE SUCCESSFULLY ADDED {} for {} Rs.".format(p_item.name,p_item.price),category='success')
            
            else:
                flash("YOU DONT HAVE ENOUGH MONEY", category='danger')
    
    
        
    
    
   
        sold_item=request.form.get('sold_item')
        s_item=Item.query.filter_by(name=sold_item).first()
        
        
        if s_item:
            if current_user.can_sell(s_item):
                s_item.sell(current_user)
                flash("YOU HAVE SUCCESSFULLY SOLD {} for {} Rs.".format(s_item.name,s_item.price),category='success')
            else:
                    flash("SOMETHING WENT WRONG", category='danger')
        return redirect(url_for('market_page'))
    
    
    if request.method=="GET": 
        item=Item.query.all()
        
        owned_items=Item.query.filter_by(owner=current_user.id)
        return render_template('market.html',items=item,form=form,owned_items=owned_items,selling_form=selling_form)
        
    





@app.route('/register',methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(username=form.username.data,password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash("Account Created Successfully! You are logged in as {}".format(user_to_create.username), category='success')
        
        return redirect(url_for('market_page'))
    if(form.errors!={}):
        for err in form.errors.values():
            flash("There was an error {}".format(err),category='danger')
    return render_template('register.html',form=form)








@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash("Success! You are logged in as {}".format(attempted_user.username), category='success')
            return redirect(url_for('market_page'))
        else:
            flash('USername and password are not matched! Please try again', category='danger')

    return render_template('login.html', form=form)






        

@app.route('/logout')
def logout_page():
    logout_user()
    flash("YOU HAVE BEEN LOGGED OUT",category="info")
    return redirect(url_for('home_page'))
    


if __name__=="__main__":
    app.run(debug=True)     