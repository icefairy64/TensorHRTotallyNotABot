# -*- encoding: utf-8 -*-

import storage
import codecs

def generate_report_for_user(user, out_filename):
    with codecs.open("report_template.txt", "r", encoding="utf-8") as rdr:
        with codecs.open(out_filename, "w", encoding="utf-8") as wtr:
            wtr.writelines(u'\n'.join([x for x in rdr.readlines()]).format(user.name, user.age, user.learn_exp, user.work_exp, user.skills))