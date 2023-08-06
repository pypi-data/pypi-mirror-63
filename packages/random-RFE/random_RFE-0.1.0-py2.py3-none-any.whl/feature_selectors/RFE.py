from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.validation import check_is_fitted
import numpy as np
import pandas as pd


class RandomRFE(object):
    """
    随机递归特征消除。递归特征消除是通过不断训练模型将最不重要的特征删除，直到停止条件为止。
    这种贪心策略较容易陷入局部最优。在此贪心策略的基础上引入随机因子，当特征重要性都不为0时，我们有一定的
    概率对特征进行随机删除，当执行随机特征删除的时候，越重要的特征被随机删除的概率越小，以此来避免陷入局部最优。
    特征重要性可以由模型的coef_属性或feature_importances_来决定，这里将每个属性的重要性做了取绝对值处理。
    """

    def __init__(self, estimator=RandomForestClassifier(), n_feature_to_select=None, percent_of_random=0.1):
        """
        特征选择器的构造函数。
        :param estimator: 用于评估特征重要性的分类器，必须具有coef_属性，或feature_importances_属性。
        :param n_feature_to_select: 要选择的特征数，默认是训练集特征的一半
        :type n_feature_to_select: int
        :param percent_of_random: 执行随机特征选择的概率，[0.0,1.0]。0：不执行随机特征删除，1：每次都执行随机特征删除。
        :type percent_of_random: float
        """
        self.estimator = estimator
        self.percent_of_random = percent_of_random
        self.n_feature_to_select = n_feature_to_select
        self.feature_names = None

    def _fit(self, X_train: pd.DataFrame, y_train):
        self.feature_names = list(X_train.columns)
        return self.estimator.fit(X_train, y_train)

    @property
    def feature_importance_(self):
        check_is_fitted(self.estimator)
        # Get feature_importance
        if hasattr(self.estimator, 'coef_'):
            feature_importance = self.estimator.coef_.tolist()[0]
        else:
            feature_importance = getattr(self.estimator, 'feature_importances_', None)
        if feature_importance is None:
            raise RuntimeError('The classifier does not expose '
                               '"coef_" or "feature_importances_" '
                               'attributes')
        fp = list(map(lambda x: abs(x), feature_importance))
        return fp

    @property
    def _need_to_random(self):
        if not (0 <= self.percent_of_random <= 1):
            raise ValueError('随机比例错误！')
        return np.random.choice([1, 0], p=[self.percent_of_random, 1 - self.percent_of_random])

    def _random_delete_feature(self):
        prob_to_delete = self.get_prob_to_delete(self.feature_importance_)
        return np.random.choice(self.feature_names, p=prob_to_delete)

    @staticmethod
    def get_prob_to_delete(fp: list):
        """
        输入为特征重要性列表，所有元素均为大于 0 的浮点数。返回被删除的概率。
        """
        prob = list(map(lambda x: 1 / x, fp))
        prob_sum = sum(prob)
        prob_to_delete = list(map(lambda x: x / prob_sum, prob))
        return prob_to_delete

    def auto_select(self, X_train, y_train):
        # 首次训练
        self._fit(X_train, y_train)

        # 初始化数据
        zero_importance = 0
        random_del = 0
        not_random = 0
        feature_selected = self.feature_names
        n_features = X_train.shape[1]

        if self.n_feature_to_select is None:
            n_feature_to_select = n_features // 2
        else:
            n_feature_to_select = self.n_feature_to_select

        while len(feature_selected) > n_feature_to_select:
            # 如果特征重要性中有0重要性特征，则删除0重要性特征，否则有一定概率决定是否进行随机删除。
            for name, importance in zip(self.feature_names, self.feature_importance_):
                if importance == 0:
                    zero_importance += 1
                    feature_selected.remove(name)
                    break
            else:
                if self._need_to_random:
                    random_del += 1
                    deleted = self._random_delete_feature()
                    feature_selected.remove(deleted)
                else:
                    not_random += 1
                    zipped = zip(feature_selected, self.feature_importance_)
                    dic = sorted(zipped, key=lambda x: x[1])
                    deleted = dic[0][0]
                    feature_selected.remove(deleted)
            self._fit(X_train[feature_selected], y_train)
        print('执行了 %s 次零重要性删除，%s 次随机删除，%s 次最不重要特征删除！' % (zero_importance, random_del, not_random))
        return feature_selected
