# 随机递归特征消除
## 1、概述
为了提高模型性能，我们通常会给数据进行降维，一种有效的方法就是删掉一些无用的或者无效的特征，以达到8。递归特征消除就是这样方法之一，即通过不断训练模型，每次训练都将重要性最小的特征删除，直到满足停止条件。

这是一种贪心策略，不断删除最不重要的特征并不能保证一定能够获得最优子集，一种有效的方式是在删除特征的时候加入一些随机因素。

随机递归特征消除在递归特征消除的过程中加入了随机因子，随机因子用于控制当前特征删除是执行随机删除还是将最不重要的特征删除，当执行随机特征删除时，将随机删除一个特征，每个特征被删除的概率不同，越重要的特征具有越小的被删除概率，其中特征重要性有模型的coef_属性或feature_importances_属性决定，其值做了取绝对值处理以防止权重为负，导致负概率的发生。
## 2、用法
```python
from feature_selectors.RFE import RandomRFE
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('your_datasets_path.txt')
X = df.drop(columns=['label'])
y = df['label']
X_train,X_test,y_train,y_test = train_test_split(X,y)

# 构建一个选择器实例，其他参数请参考请help一下，代码有注释。 
fs = RandomRFE(percent_of_random=0.1)
selected_feature = fs.auto_select(X_train,y_train)

```
## 3、后续
其他特征选择方法，后续陆续加入，争取做个特性选择器，欢迎大神指正，并完善特征选择器，方便你我他！



