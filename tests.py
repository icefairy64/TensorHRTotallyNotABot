# -*- encoding:utf-8 -*-

"""
Тесты модуля проверки ответов
"""

import unittest
from quiz.answer_evaluation import *

"""
Для запуска тестов: python tests.py
"""

class TestSingleChoiceAnswer(unittest.TestCase):

    def setUp(self):
        self.ae = AnswerEvaluation.factory(AnswerEvaluation.SINGLE_CHOICE)

    def test_without_infelicity(self):
        self.assertEqual(self.ae.estimate('инкапсуляция', 'Инкапсуляция'), 1)
        self.assertEqual(self.ae.estimate('палиморфизм', 'Полиморфизм'), 0)

    def test_with_infelicity(self):
        self.assertEqual(
            self.ae.estimate('Инкапсу', 'Инкапсуляция'), 0)
        self.assertGreaterEqual(
            self.ae.estimate('Инкапсу', 'Инкапсуляция', 0.45), 0.5)
        self.assertGreaterEqual(
            self.ae.estimate('Енкапселция', 'Инкапсуляция', 0.3), 0.8)
        self.assertGreaterEqual(
            self.ae.estimate('Палиморфизм', 'Полиморфизм', 0.2), 0.9)
        self.assertGreaterEqual(
            self.ae.estimate('Наслiдуване', 'Наследование', 0.3), 0.75)
        self.assertLessEqual(
            self.ae.estimate('успадкування', 'Наследование', 0.9), 0.5)


class TestMultipleChoiceAnswer(unittest.TestCase):

    def setUp(self):
        self.ae = AnswerEvaluation.factory(AnswerEvaluation.MULTIPLE_CHOICE)
        self.ref_answers = ['инкапсуляция', 'полиморфизм', 'наследование']

        self.answer1 = ['инкапсуляция', 'полиморфизм', 'наследование']
        self.answer2 = ['палиморфзм', 'наследавание']
        self.answer3 = ['палиморфзм', 'наследавание', 'инкапсуляция']
        self.answer4 = ['палиморфзм']

    def test_without_infelicity(self):
        self.assertEqual(self.ae.estimate( self.answer1,
                                     {'answers': self.ref_answers}, 0.6), 1)

        self.assertEqual(self.ae.estimate(self.answer2,
                                     {'answers': self.ref_answers}, 0.6), 0)

        self.assertEqual(self.ae.estimate(self.answer3,
                                     {'answers': self.ref_answers}, 0.6), 1)


    def test_with_infelicity(self):
        self.assertEqual(self.ae.estimate(self.answer2,
                                     {'answers': self.ref_answers,
                                      'infelicity': 2}, 0.6), 0.67)
        self.assertEqual(self.ae.estimate(self.answer4,
                                     {'answers': self.ref_answers,
                                      'infelicity': 2}, 0.6), 0)
        self.assertEqual(self.ae.estimate(self.answer4,
                                     {'answers': self.ref_answers,
                                      'infelicity': 1}, 0.6), 0.33)


if __name__ == '__main__':
    unittest.main()

