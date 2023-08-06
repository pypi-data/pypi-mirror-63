# DeepTables

## DeepTables: Deep-learning Toolkit for Tabular data
DeepTables(DT) is a easy-to-use toolkit that enables deep learning to unleash great power on tabular data.


## Overview

MLP (also known as Fully-connected neural networks) have been shown inefficient in learning distribution representation. The "add" operations of the perceptron layer have been proven poor performance to exploring multiplicative feature interactions. In most cases, manual feature engineering is necessary and this work requires extensive domain knowledge and very cumbersome. How learning feature interactions efficiently in neural networks becomes the most important problem.

Various models have been proposed to CTR prediction and continue to outperform existing state-of-the-art approaches to the late years. Well-known examples include FM, DeepFM, Wide&Deep, DCN, PNN, etc. These models can also provide good performance on tabular data under reasonable utilization.

DT aims to utilize the latest research findings to provide users with an end-to-end toolkit on tabular data.

DT has been designed with these key goals in mind:

* Easy to use, non-experts can also use.
* Provide good performance out of the box.
* Flexible architecture and easy expansion by user.


## Example：
``` python
import numpy as np
from deeptables.models import deeptable, deepnets
from examples.datasets import utils as dsutils
from sklearn.model_selection import train_test_split

#loading data
df = dsutils.load_bank()
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

y = df_train.pop('y')
y_test = df_test.pop('y')

config = deeptable.ModelConfig(nets=deepnets.DeepFM)

#training
dt = deeptable.DeepTable(config=config)
model, history = dt.fit(df_train, y, epochs=10)

#evaluation
result = dt.evaluate(df_test,y_test, batch_size=512, verbose=0)
print(result)

#scoring
preds = dt.predict(df_test)

```