# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

db.define_table('item',                         
                Field('name',requires = IS_NOT_EMPTY()),
                Field('category',
                      requires = IS_IN_SET(['Arts and Crafts','Clothing','Gifts','Footwears']),
                      default = 'Arts and Crafts'),        
                Field('price', 'integer',requires = IS_NOT_EMPTY()),
                Field('image','upload'),
                Field('selling_type',requires = IS_IN_SET(['Bid','Buy']),default = 'Bid'),
                Field('seller',
                      db.auth_user,
                      default=auth.user_id,
                      writable=False,
                      readable=False,
                      requires=IS_IN_DB(db, db.auth_user.id,'%(first_name)s')),
                Field('description','text',requires = IS_NOT_EMPTY()),
                Field('created_on','datetime',
                      default=request.now,
                      update=request.now,
                      writable=False))

db.define_table('sold',
                Field('item_id',db.item, requires=IS_IN_DB(db,db.item.id, '%(name)s')),
                Field('price','integer',
                      writable = False,
                      readable = False),
                Field('buyer',
                      db.auth_user,
                      default=auth.user_id,
                      writable=False,
                      readable=False,
                      requires=IS_IN_DB(db, db.auth_user.id,'%(first_name)s')))

db.define_table('wish',
                Field('name',requires = IS_NOT_EMPTY()),
                Field('category',
                      requires = IS_IN_SET(['Arts and Crafts','Clothing','Gifts','Footwears']),
                      default = 'Arts and Crafts'),
                Field('price', 'integer'),
                Field('image','upload'),
                Field('buyer',
                      db.auth_user,
                      default=auth.user_id,
                      writable=False,
                      readable=False,
                      requires=IS_IN_DB(db, db.auth_user.id,'%(first_name)s')),
                Field('description','text',requires = IS_NOT_EMPTY()))

db.define_table('bid',
                Field('item_id',db.item,
                      readable = False,
                      writable = False, 
                      requires=IS_IN_DB(db,db.item.id, '%(name)s')),
                Field('amount','integer'),
                Field('bidder',
                      db.auth_user,
                      default=auth.user_id,
                      writable=False,
                      readable=False,
                      requires=IS_IN_DB(db, db.auth_user.id,'%(first_name)s')),
                Field('created_on','datetime',
                      default=request.now,
                      update=request.now,
                      writable=False))

db.define_table('buy',
                Field('item_id'),
                Field('buyer',
                      db.auth_user,
                      default=auth.user_id,
                      writable=False,
                      readable=False,
                      requires=IS_IN_DB(db, db.auth_user.id,'%(first_name)s')))

db.define_table('fulfil',
                Field('wish_id',db.wish, requires=IS_IN_DB(db,db.wish.id, '%(name)s')),
                Field('item_id',db.wish, requires=IS_IN_DB(db,db.item.id, '%(name)s')),
                )

db.define_table('rating',
                Field('rate',requires = IS_INT_IN_RANGE(0,6)),
                Field('seller',
                      db.auth_user,
                      writable = False,
                      readable = False,
                      requires=IS_IN_DB(db, db.auth_user.id)))

db.define_table('cart',
                Field('item_id',db.item, requires=IS_IN_DB(db,db.wish.id, '%(name)s')),
                Field('user_id',
                      db.auth_user,
                      default=auth.user_id,
                      writable=False,
                      readable=False,
                      requires=IS_IN_DB(db, db.auth_user.id,'%(first_name)s')))

db.define_table('reviews',
                Field('item_id',db.item,
                      requires=IS_IN_DB(db,db.wish.id, '%(name)s'),
                      readable=False,
                      writable=False),
                Field('name','string',default="Anon"),
                Field('review','text'))

db.define_table('report',
                Field('user_id',
                      db.auth_user,
                      default=auth.user_id,
                      writable=False,
                      readable=False,
                      requires=IS_IN_DB(db, db.auth_user.id,'%(first_name)s')),
                Field('you_are_a',requires=IS_IN_SET(['Buyer','Seller']),default="Buyer"),
                Field('Description','text'))