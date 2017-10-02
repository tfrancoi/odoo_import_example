# -*- coding: utf-8 -*-
import os
from odoo_csv_tools.lib import mapper
from odoo_csv_tools.lib.transform import Processor
from datetime import datetime
from prefix import *

#STEP 1 : read the needed file(s)
processor = Processor('origin%scontact.csv' % os.sep)

##STEP 2 : Define the mapping for every object to import
mapping =  {
    'id' : mapper.m2o_map(CLIENT_PREFIX, mapper.concat('_', 'Client Name','zip code')),
    'name' : mapper.val('Client Name', skip=True),
    'phone' : mapper.val('Phone'),
    'street' : mapper.val('address1'),
    'city' : mapper.val('city'),
    'zip' : mapper.val('zip code'),
    'country_id/id' : mapper.map_val('country', country_map),
    'customer' : mapper.const('1'),
    'lang' : mapper.map_val('Language', lang_map),
    'image' : mapper.binary("Image", "origin/img/"),
    'create_uid': mapper.val('Create BY'),
    'create_date': mapper.val('Create ON', 
        postprocess=lambda x: datetime.strptime(x, "%d/%m/%y").strftime("%Y-%m-%d 00:00:00")),
    'category_id/id': mapper.m2m(PARTNER_CATEGORY_PREFIX, 'Tag', 'Fidelity Grade'),
}

tag_mapping = {
   'id' : mapper.m2m_id_list(PARTNER_CATEGORY_PREFIX, 'Tag'),
   'name' :  mapper.m2m_value_list('Tag'),
}

grade_mapping = {
   'id' : mapper.m2m_id_list(PARTNER_CATEGORY_PREFIX, 'Fidelity Grade'),
   'name' :  mapper.m2m_value_list('Fidelity Grade'),
}

#Step 4: Process data
processor.process(tag_mapping, 'data%sres.partner.category.csv' % os.sep, {}, m2m=True)
processor.process(grade_mapping, 'data%sres.partner.category.grade.csv' % os.sep, {'model': 'res.partner.category'}, m2m=True)
processor.process(mapping, 'data%sres.partner.csv' % os.sep, { 'worker' : 2, 'batch_size' : 20, 'context': {'write_metadata': True}})

#Step 5: Define output and import parameter
processor.write_to_file("1_client.sh", python_exe='', path='')

print 'Client Done'
