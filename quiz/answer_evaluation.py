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

class AnswerEvaluationSingleChoice(AnswerEvaluation):

    def estimate(self, answer, reference, infelicity=0):
        answer = answer.lower()
        reference = reference.lower()
        if infelicity > 0:
            # Вычисляем разницу в словах
            dam_lev_dis = damerau_levenstein_distance(answer, reference)
            p = dam_lev_dis / len(reference)
            if p < infelicity:
                # Формирование оценки
                return round(1 - p, 2)
            else:
                return 0

        if answer == reference:
            return 1
        else:
            return 0


class AnswerEvaluationMultipleChoice(AnswerEvaluation):

    def estimate(self, answer, reference, infelicity=0):
        if answer is None or reference is None:
            return 0
        result = 0

        ref_inf = reference.get('infelicity', 0)

        if infelicity > 0:
            for ra in reference['answers']:
                for aa in answer:
                    dam_lev_dis = damerau_levenstein_distance(aa, ra)
                    p = dam_lev_dis / len(ra)
                    if p < infelicity:
                        result += 1
        else:
            for ra in reference['answers']:
                if ra in answer:
                    result += 1

        if ref_inf == 0:
            if result == len(reference['answers']):
                return 1
            else:
                return 0

        if result < ref_inf:
            return 0
        else:
            return round(result / len(reference['answers']), 2)


class AnswerEvaluationFreeForm(AnswerEvaluation):

    def estimate(self, answer, reference):
        return 1

