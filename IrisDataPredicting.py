import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib


url = "irisData"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pandas.read_csv(url, names=names)

# Shape
print(dataset.shape)
# Head
print(dataset.head(20))
# Summary
print(dataset.describe())
# Class distribution
print(dataset.groupby('class').size())
 

# Univariate Plots to look at plots of each individual variable
dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
plt.show() 
dataset.hist()
plt.show()
 

# Multivariate Plots to look at interactions between variables
scatter_matrix(dataset)
plt.show()
 

# Split-out validation dataset
array = dataset.values
X = array[:,0:4]
Y = array[:,4]
validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)

 
# Splitting dataset into 10 parts; 9 to train and 1 to test
seed = 7
scoring = 'accuracy'
 

# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
 

# Evaluate each model in turn
results = []
names = []

for name, model in models:
    kfold = model_selection.KFold(n_splits=10, random_state=seed)
    cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

       
# Compare Algorithm
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show() 


# Making Prediction
lda = LinearDiscriminantAnalysis()
lda.fit(X_train, Y_train)
predictions = lda.predict(X_validation)
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))


#Predicting for new data set using most accurate algorithm
pipe = make_pipeline(StandardScaler(), LinearDiscriminantAnalysis())
pipe.fit(X_train, Y_train)
joblib.dump(pipe, 'irisTest.pkl')

pipe = joblib.load('irisTest.pkl')
pr = pandas.read_csv("irisTestData")

pred = pandas.Series(pipe.predict(pr))
print(pred)
#print(pr)