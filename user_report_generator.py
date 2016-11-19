# -*- encoding: utf-8 -*-

import storage
import codecs


def generate_report_for_user(user, out_filename):
    template_file = codecs.open('report_template.html', 'r', 'utf-8')
    template = template_file.read()
    template_file.close()

    report = template.format(
        name=user.name,
        age=user.age,
        learn_exp=user.learn_exp,
        work_exp=user.work_exp,
        skills=user.skills
    )

    with codecs.open(out_filename, "w", encoding="utf-8") as report_file:
        report_file.write(report)

if __name__ == '__main__':
    from storage import User

    generate_report_for_user(User(1,
                                  '1',
                                  u'Василий Пупкин',
                                  25,
                                  u'Закончил КГТУ',
                                  u'Нигде ещё не работал, тольк отучился',
                                  u'C# и разработка игр',
                                  u'программист c#'),
                             'report.html')
