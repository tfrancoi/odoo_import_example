# -*- coding: utf-8 -*-
from odoo_csv_tools.lib import mapper
from odoo_csv_tools.lib.transform import Processor
from datetime import datetime
from prefix import SUPPLIER_PREFIX, MESSAGE_PREFIX, SUPPLIER_CONTACT_PREFIX

#STEP 1 : read the needed file(s)
processor = Processor('origin/message.csv')

##STEP 2 : Define the mapping for every object to import
mapping =  {
    'id' : mapper.m2o_map(MESSAGE_PREFIX, mapper.concat("_", 'Company_ID', 'Date')),
    'res_external_id' : mapper.m2o(SUPPLIER_PREFIX, 'Company_ID'),
    'author_id/id': mapper.m2o(SUPPLIER_CONTACT_PREFIX, 'from'),
    'email_from': mapper.val('from'),
    'subject': mapper.val('subject'),
    'body': mapper.val('body'),
    'date': mapper.val('Date', 
       postprocess=lambda x: datetime.strptime(x, "%d/%m/%y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")),
}

#Step 4: Process data
processor.process(mapping, 'data/mail.message.csv', {})

#Step 5: Define output and import parameter
processor.write_to_file("3_supplier_message.sh", python_exe='', path='')

print 'Supplier Message Done'
