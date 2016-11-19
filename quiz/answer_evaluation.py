# -*- encoding: utf-8 -*-

from quiz.utils import *

class AnswerEvaluation(object):
    """
    Базовый класс проверки ответов соискателя
    """

    SINGLE_CHOICE = 0
    MULTIPLE_CHOICE = 1
    FREE_FORM = 2

    @staticmethod
    def factory(type):
        if type == AnswerEvaluation.SINGLE_CHOICE:
            return AnswerEvaluationSingleChoice()
        if type == AnswerEvaluation.MULTIPLE_CHOICE:
            return AnswerEvaluationMultipleChoice()
        if type == AnswerEvaluation.FREE_FORM:
            return AnswerEvaluationFreeForm()

        assert 0, "Bad answer type: " + type


    def estimate(self, answer, reference, pos_infelicity=0):
        """
        Метод оценить. Принимает ответ пользователя, параметры эталонного
        ответа и возможную погрешность в ответе.
        Если погрешность ответа не превышает допустимую - выставляем оценку
        от 0 до 1. Если нет - минимальная оценка за вопрос - 0
        """
        raise NotImplementedError(
            'Необходимо реализовать метод estimate (оценить)')
