# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('Buy/Sell'),XML('&trade;&nbsp;'),
                  _class="brand",_href="")
response.title = ' '.join(
    word.capitalize() for word in request.application.split('_'))
response.subtitle = T('customize me!')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    if auth.is_logged_in():
        response.menu += [
        (SPAN('Navigate', _class='highlighted'), False, '', [
        (T('List of items'), False, URL('BuySell', 'default', 'list_items')),
        (T('Sell'), False, '', [
        (T('Add Item'), False,
         URL(
         'BuySell', 'default', 'add_item')),
        (T('Your Listed Items'), False,
         URL(
         'BuySell', 'default', 'listed_items')),
        (T('Items Sold'), False,
         URL(
         'BuySell', 'default', 'item_sold')),
        (T('Fulfil Wishes'), False,
         URL(
         'BuySell', 'default', 'fulfil_wishes')),
        ]),
            ('Buy', False, '', [
             (T('Make a wish'), False,
              URL('BuySell', 'default', 'add_wish')),
             (T('Your Wish List'), False,
              URL('BuySell', 'default', 'wish_list')),
             (T('Fulfilled Wishes'), False, URL('BuySell', 'default', 'fulfilled')),
             (T('Items Bought/Bids Won'), False,
              URL('BuySell', 'default', 'item_bought')),
             ]),
            (T('All Categories'), False, 'http://www.web2py.com/book', [
             (T('Arts and Crafts'), False,
              URL('BuySell', 'default', 'categories',args = '1')),
             (T('Clothing'), False,
              URL('BuySell', 'default', 'categories',args = '2')),
             (T('Footwear'), False,
              URL('BuySell', 'default', 'categories',args = '3')),
             (T('Gifts'), False,
              URL('BuySell', 'default', 'categories',args = '4'))
             ]),
            (T('Community'), False, None, [
                        (T('Twitter'), False, 'http://twitter.com/buy_sell'),
                        (T('Live Chat'), False,
                         'http://webchat.freenode.net/?channels=buysell'),
                        ]),
                (T('Help'), False, None, [
                        ('FAQ', False,
                         URL('BuySell', 'default', 'index')),
                        ('Report a Problem', False,
                         URL('BuySell', 'default', 'report')),
                        #(T('Report'), False,
                        # 'http://web2py.com/plugins'),
                        #(T('Others'),
                        # False, 'http://web2py.com/layouts'),
                        ])
                ]
         )]
if DEVELOPMENT_MENU: _()
