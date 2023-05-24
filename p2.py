

#import lib

import pickle
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix, classification_report


#load the data
data = pd.read_csv("creditcard.csv")
#data.drop(["Class"],axis="columns",inplace=True)
print(data.head())

#understand the data
res = data.isnull().sum()
print(res)

value = data['Class'].value_counts()
print(value)

legit = data[data.Class == 0]
fraud = data[data.Class == 1]
print(legit.shape)
print(fraud.shape)

legit.Amount.describe()
fraud.Amount.describe()

data['Class'].value_counts()

legit_sample = legit.sample(n=492)

new_data = pd.concat([legit_sample, fraud], axis=0)
new_data.head()
new_data.tail()

new_data.to_csv('file.csv', index=False)


new_data['Class'].value_counts()


#features and data
features = new_data.drop(["Class", "Time"], axis="columns")
target = new_data["Class"]
print(features.head())
print(target.head())

#handle cat data
nfeatures = pd.get_dummies(features)
print(nfeatures.head())

#find N
N = int(len(new_data) ** 0.5)
if N % 2 == 0:
	N = N+1

#train and test
x_train, x_test, y_train, y_test = train_test_split(nfeatures, target)

#model and fit
model = DecisionTreeClassifier()
mf = model.fit(x_train, y_train)

up_data = request.files.get('file')
data = []
messages = []
i = 0
if up_data:
	for row in up_data:
		values = row.decode().strip().split(",")
		row_data = [float(val) for val in values]
		i = i+1
		data.append(row_data)
		pred = model.predict([row_data])
		msg = " Legitimate Transaction " if pred == 'N' else "  Fraudulent Transaction"
		messages.append(str(i) + "]   Transaction is: " + msg + "<br>")

#performance
plot_confusion_matrix(model, x_test, y_test)
plt.show()

input()

cr = classification_report(y_test, model.predict(x_test))
print(cr)

input()

#plot tree
#plot_tree(mf,max_depth=3,fontsize=10)
#plt.savefig("tt.png")
#plt.show()
