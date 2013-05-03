# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

@auth.requires_login()
def list_items():
    #items = db().select(db.item.ALL)
    
    name=TD('Search item:')
    namebox=TD(INPUT(_id='item_title',_name='item[name]',_size='50',_type='text',requires=IS_NOT_EMPTY()),DIV_class='auto_complete',_id='item_name_auto_complete')   
    submit=TD(INPUT(_type='submit',_name='submit',_value='Submit'))
    #descr=TD('Search Publication(s) by Author:')
    #descrbox=TD(INPUT(_id='_des',_name='music[descr]',_size='30',_type='text'),DIV(_class='auto_complete',_id='movie_descr_auto_complete'))
    
    form1=FORM(TABLE(TR(name,namebox,submit)))
    
    items=db().select(db.item.ALL,orderby=db.item.name)
    
    if form1.accepts(request.vars,session):
        search=request.vars['item[name]']
        items=db(db.item.name.upper().like('%'+search.upper()+'%')).select(db.item.ALL,orderby=db.item.name)

    bids = db().select(db.bid.ALL)
    no_bids = {}
    for i in items:
        d = db(i.id == db.bid.item_id).select(db.bid.ALL).first()
        if d == None:
            no_bids[i.id] = i.price
    
    return dict(form1=form1,items=items,bids=bids,no_bids=no_bids)

@auth.requires_login()
def item_d():
    item=db(request.args(0)==db.item.id).select(db.item.ALL).first()
    if item:
        seller = db(item.seller==db.auth_user.id).select(db.auth_user.ALL).first()
    reviews = db(request.args(0)==db.reviews.item_id).select(db.reviews.ALL)
    form = SQLFORM(db.reviews)
    form.vars.item_id = request.args(0)
    if form.accepts(request.vars):
        response.flash = 'Success\n'
        redirect(URL(r=request, f="listed_items",args=request.args(0)))
        
    bids = db().select(db.bid.ALL)
    no_bids = {}
    d=None 
    if item:
        d = db(item.id == db.bid.item_id).select(db.bid.ALL).first()
    if d == None:
        no_bids[item.id] = item.price
                
    return dict(bids=bids,no_bids=no_bids,item=item,seller=seller,reviews=reviews,form=form)

@auth.requires_login()
def seller():
    seller = db(request.args(0)==db.auth_user.id).select(db.auth_user.ALL).first()
    
    avg = 0
    count = 0
    sellr = db(request.args(0)==db.rating.seller).select(db.rating.ALL)
    for i in sellr:
        avg = avg + int(i.rate)
        count = count + 1
    if count > 0:
        av = (float(avg)/float(count))
    else:
        av = 0.0
    
    prod = db(seller.id==db.item.seller).select(db.item.ALL)
    
    form = SQLFORM(db.rating)
    
    form.vars.seller = request.args(0)
    
    if form.accepts(request.vars):
        response.flash = 'Success\n'
    
    items = db(seller.id==db.item.seller).select(db.item.ALL)
    bids = db().select(db.bid.ALL)
    no_bids = {}
    for i in items:
        d = db(i.id == db.bid.item_id).select(db.bid.ALL).first()
        if d == None:
            no_bids[i.id] = i.price
        
    return dict(av=av,seller=seller,form=form,prod=prod,bids=bids,no_bids=no_bids)

@auth.requires_login()
def add_item():
    form = SQLFORM(db.item)
    if form.accepts(request.vars):
        response.flash = 'Success\n'
    return dict(form=form)

@auth.requires_login()
def listed_items():
    seller = db(auth.user_id==db.item.seller).select(db.item.ALL)
    
    bids = db().select(db.bid.ALL)
    no_bids = {}
    for i in seller:
        d = db(i.id == db.bid.item_id).select(db.bid.ALL).first()
        if d == None:
            no_bids[i.id] = i.price
    
    return dict(seller=seller,bids=bids,no_bids=no_bids)

@auth.requires_login()
def add_wish():
    form = SQLFORM(db.wish)
    if form.accepts(request.vars):
        response.flash = 'Success\n'
    return dict(form=form)

@auth.requires_login()
def wish_list():
    wish = db(auth.user_id==db.wish.buyer).select(db.wish.ALL,
                                                       orderby=db.wish.name)
    return dict(wish=wish)

@auth.requires_login()
def wish_d():
    item=db(request.args(0)==db.wish.id).select(db.wish.ALL).first()
    if item:
        seller = db(item.buyer==db.auth_user.id).select(db.auth_user.ALL).first()
                
    return dict(item=item,seller=seller)

@auth.requires_login()
def fulfilled():#Client Side computation
    sold = db().select(db.fulfil.ALL,orderby=db.fulfil.id)
    items = db(auth.user_id==db.wish.buyer).select(db.wish.ALL)
    id = auth.user_id
    return dict(sold=sold,items=items,id=id)

@auth.requires_login()
def categories():
    name=TD('Search item:')
    namebox=TD(INPUT(_id='item_title',_name='item[name]',_size='50',_type='text',requires=IS_NOT_EMPTY()),DIV_class='auto_complete',_id='item_name_auto_complete')   
    submit=TD(INPUT(_type='submit',_name='submit',_value='Submit'))
    #descr=TD('Search Publication(s) by Author:')
    #descrbox=TD(INPUT(_id='_des',_name='music[descr]',_size='30',_type='text'),DIV(_class='auto_complete',_id='movie_descr_auto_complete'))
    
    form1=FORM(TABLE(TR(name,namebox,submit)))
    
    items=db().select(db.item.ALL,orderby=db.item.name)
    
    if(request.args(0) == '1'):
        items = db('Arts and Crafts'==db.item.category).select(db.item.ALL)
    if(request.args(0) == '2'):
        items = db('Clothing'==db.item.category).select(db.item.ALL)
    if(request.args(0) == '3'):
        items = db('Footwear'==db.item.category).select(db.item.ALL)
    if(request.args(0) == '4'):
        items = db('Gifts'==db.item.category).select(db.item.ALL)
    
    if form1.accepts(request.vars,session):
        search=request.vars['item[name]']
        items=db(db.item.name.upper().like('%'+search.upper()+'%')).select(db.item.ALL,orderby=db.item.name)
    
    return dict(items=items,form1=form1)

@auth.requires_login()
def delete_item():
    db(db.item.id==request.args(0)).delete()
    redirect(URL(r=request, f="listed_items"))
    return dict()

@auth.requires_login()
def delete_wish():
    db(db.wish.id==request.args(0)).delete()
    redirect(URL(r=request, f="wish_list"))
    return dict()

"""
@auth.requires_login()
def bids_won():
    placed = db(auth.user_id==db.bid.bidder).select(db.bid.ALL,orderby=db.bid.amount).first()
    if placed:
        if placed.time
    return
"""

@auth.requires_login()
def place_bid():
    placed = db(request.args(0)==db.bid.item_id).select(db.bid.ALL,orderby=db.bid.amount).first()
    if placed == None:
        item=db(request.args(0)==db.item.id).select(db.item.ALL).first().price
    else:
        item = placed.amount
        
    form = SQLFORM(db.bid)
    form.vars.item_id = request.args(0)
    form.vars.bidder = auth.user_id
    
    if request.vars and int(request.vars.amount) > int(item) and form.accepts(request.vars):
        response.flash = 'Success\n'
        if placed:
            db(db.bid.id==placed.id).delete()
    else:
        response.flash = 'Please place a bid greater than the last offer'
    return dict(form=form)        

@auth.requires_login()    
def buy_item():
    form = SQLFORM(db.sold)
    item = db(request.args(0)==db.item.id).select(db.item.ALL).first()
    form.vars.item_id = item.id
    form.vars.price = item.price
    if form.accepts(request.vars):
        response.flash = 'Success\n'
    return dict(form=form)

@auth.requires_login()
def item_sold():#Client side computation to be done
    sold = db().select(db.sold.ALL,orderby=db.sold.id)
    item = db().select(db.item.ALL,orderby=db.item.id)
    id = auth.user_id  
    return dict(sold=sold,item=item,id=id)

@auth.requires_login()
def fulfil_wishes():
    name=TD('Search item:')
    namebox=TD(INPUT(_id='item_title',_name='wish[name]',_size='50',_type='text',requires=IS_NOT_EMPTY()),DIV_class='auto_complete',_id='item_name_auto_complete')   
    submit=TD(INPUT(_type='submit',_name='submit',_value='Submit'))
    #descr=TD('Search Publication(s) by Author:')
    #descrbox=TD(INPUT(_id='_des',_name='music[descr]',_size='30',_type='text'),DIV(_class='auto_complete',_id='movie_descr_auto_complete'))
    
    form1=FORM(TABLE(TR(name,namebox,submit)))
    
    items=db().select(db.wish.ALL,orderby=db.wish.name)
    
    if form1.accepts(request.vars,session):
        search=request.vars['wish[name]']
        items=db(db.wish.name.upper().like('%'+search.upper()+'%')).select(db.wish.ALL,orderby=db.wish.name)

    return dict(form1=form1,items=items)

@auth.requires_login()    
def fulfil():    
    form = SQLFORM(db.fulfil)
    form.vars.wish_id = request.args(0)
    if form.accepts(request.vars):
        response.flash = 'Success\n'
    return dict(form=form)

@auth.requires_login()
def item_bought():
    items=db().select(db.item.ALL,orderby=db.item.name)
    sold = db(auth.user_id == db.sold.buyer).select(db.sold.ALL,orderby=db.sold.id)
    id = auth.user_id  
    return dict(sold=sold,items=items,id=id)

def report():
    form = SQLFORM(db.report)
    if form.accepts(request.vars):
        response.flash = 'Thanks for notifying, appropriate action will be taken in 24 hrs.'
    return dict(form=form)