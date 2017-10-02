# -*- coding: utf-8 -*-
from odoo_csv_tools.lib import mapper
from odoo_csv_tools.lib.transform import Processor
from datetime import datetime
from prefix import *

#STEP 1 : read the needed file(s)
processor = Processor('origin/supplier.csv')

##STEP 2 : Define the mapping for every object to import
mapping =  {
    'id' : mapper.m2o(SUPPLIER_PREFIX, 'Company_ID'),
    'name' : mapper.val('Company_Name'),
    'phone' : mapper.val('Phone'),
    'street' : mapper.val('address1'),
    'city' : mapper.val('city'),
    'zip' : mapper.val('zip code'),
    'country_id/id' : mapper.map_val('country', country_map),
    'supplier' : mapper.const('1'),
    'user_id': mapper.val('Account_Manager'),
}

contact_mapping = {
    'id': mapper.m2o(SUPPLIER_CONTACT_PREFIX, 'Contact Email'),
    'parent_id/id': mapper.m2o(SUPPLIER_PREFIX, 'Company_ID'),
    'email': mapper.val('Contact Email'),
    'name': mapper.concat(' ',  'Contact First Name', 'Contact Last Name'),
    'title/id': mapper.m2o(TITLE_PREFIX, 'Contact Title'),
}
 
title_map = {
    'id': mapper.m2o(TITLE_PREFIX, 'Contact Title'),
    'name': mapper.val('Contact Title', skip=True),
    'shortcut': mapper.val('Contact Title')
}



#Step 4: Process data
processor.process(title_map, 'data/res.partner.title.csv', {}, 'set')
processor.process(mapping, 'data/res.partner.supplier.csv', { 'model': 'res.partner'})
processor.process(contact_mapping, 'data/res.partner.supplier.contact.csv', { 'model': 'res.partner'})

#Step 5: Define output and import parameter
processor.write_to_file("2_supplier.sh", python_exe='', path='')

print 'Supplier Done'
