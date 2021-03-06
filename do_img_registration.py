# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 15:51:02 2016

@author: dahoiv
"""
from __future__ import print_function
import os
import datetime
import sqlite3

import image_registration
import util


def find_images():
    """ Find images for registration """
    conn = sqlite3.connect(util.DB_PATH)
    conn.text_factory = str

    cursor = conn.execute('''SELECT pid from Patient''')
    ids = []
    for row in cursor:
        cursor2 = conn.execute('''SELECT id from Images where pid = ? AND diag_pre_post = ?''',
                               (row[0], "pre"))
        for _id in cursor2:
            _id = _id[0]
            cursor3 = conn.execute('''SELECT registration_date from Images where id = ? ''', (_id,))

            registration_date = cursor3.fetchone()[0]
            cursor3.close()
            if registration_date:
                continue
            ids.append(_id)

        cursor2.close()

    cursor.close()
    conn.close()
    return ids


# pylint: disable= invalid-name
if __name__ == "__main__":
    os.nice(17)
    HOSTNAME = os.uname()[1]
    if 'unity' in HOSTNAME or 'compute' in HOSTNAME:
        path = "/work/danieli/tumor_reg/"
    else:
        path = "tumor_reg_" + "{:%m_%d_%Y}".format(datetime.datetime.now()) + "/"

    util.setup(path)

    moving_datasets_ids = find_images()
    print(moving_datasets_ids, len(moving_datasets_ids))
    image_registration.get_transforms(moving_datasets_ids,
                                      image_registration.SYN,
                                      save_to_db=True)
