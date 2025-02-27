import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def readCSV(path):
    csv = pd.read_csv(path, parse_dates=True, header=None)
    csv.insert(1, 'bias', 1)
    return csv

def preprocess(d):
    d.insert(0, 'label', 0)
    #Please assign labels +1 to number 3 and -1 to label 5. In your produced predictions, please use only +1 and -1 as labels not 3 and 5
    d.loc[d[0] == 3, 'label'] = +1
    d.loc[d[0] == 5, 'label'] = -1
    d = d.drop([0], axis=1)
    return d

def online_perceptron(iterations, Y, X):
    lamb =1
    w = np.zeros(len(np.transpose(X)))
    accuracyList = []
    iterationList = []
    weightList = []
    for iteration in range(iterations):
        t = 0
        for i, x in enumerate(X):
            if (np.dot(w, X[i]))*Y[i] <= 0:
                w = w + (lamb*X[i]*Y[i])
                t = t + 1
        accuracy = ((1 - t/len(Y)) * 100)
        accuracyList.append(accuracy)
        iterationList.append(iteration + 1)
        weightList.append(w)
    return weightList, accuracyList, iterationList


def online_perceptron_valid(iters, Y, X, weightList):
    #setting the weights initially to zero
    w = np.zeros(len(np.transpose(X)))
    accuracyList = []
    iterationList = []

    for itr in range(len(weightList)):
        w = weightList[itr]
        t = 0
        for i, x in enumerate(X):
            # print(u)
            if np.dot(w, X[i]) * Y[i] <= 0:
                t = t + 1

        accuracy = ((1 - t/len(Y)) * 100)
        accuracyList.append(accuracy)
        iterationList.append(itr + 1)

    return accuracyList, iterationList


def online_perceptron_valid(iters, Y, X, weightList):
    #setting the weights initially to zero
    w = np.zeros(len(np.transpose(X)))
    accuracyList = []
    iterationList = []
    for itr in range(len(weightList)):
        w = weightList[itr]
        t = 0
        for i, x in enumerate(X):
            if np.dot(w, X[i]) * Y[i] <= 0:
                t = t + 1
        accuracy = ((1 - t/len(Y)) * 100)
        accuracyList.append(accuracy)
        iterationList.append(itr + 1)

    return accuracyList, iterationList

def average_perceptron_train(X,Y,iters):

    k = len(X)
    # setting the weight
    W = np.zeros(len(np.transpose(X)))
    weight_average = np.empty(shape=[1, 785])
    weight_average.fill(0)
    s = 1
    itr = 0
    weight_list = []
    loss_list = []
    accuracyList= []
    iterationList = []
    while (itr < iters):
        for i in range(k):
            output_y = np.sign(np.dot(X[i, :], W.transpose()))
            if ((Y[i] * output_y) <= 0):
                W = W + Y[i] * X[i, :]

            weight_average = (s * weight_average + W)/(s+1)
            s = s + 1

        calc_loss = 0
        for i in range(k):
            output_y = np.sign(np.dot(X[i, :], weight_average.transpose()))
            if ((Y[i] * output_y) <= 0):
                calc_loss += 1

        calc_loss = (calc_loss * 1)/k
        accuracy_train = (1 - calc_loss)*(100)
        accuracyList.append(accuracy_train)
        weight_list.append(weight_average)
        loss_list.append(calc_loss)
        iterationList.append(itr+1)
        itr += 1

    return weight_list, loss_list, iterationList, accuracyList

def average_perceptron_valid(X, Y, weightlist, iters):
    k = len(X)
    itr = 0
    loss_list = []
    accuracyList = []
    iterationList = []
    while (itr < iters):
        calc_loss = 0
        for i in range(k):
            output_y = np.sign(np.dot(X[i, :], weightlist[itr][:].transpose()))
            if ((Y[i] * output_y) <= 0):
                calc_loss += 1

        calc_loss = (calc_loss * 1) / k
        accuracy_valid = (1 - calc_loss) * (100)
        loss_list.append(calc_loss)
        iterationList.append(itr + 1)
        accuracyList.append(accuracy_valid)
        itr += 1

    return loss_list, iterationList, accuracyList

def average_PercepPlot(X,Y):
    weightList, lossList, itrList, accuracyList = average_perceptron_train(train_feat, train_y , 15)

    #plotting training loss
    plt.scatter(itrList, accuracyList, color='blue', s=150)
    blue_line, =plt.plot(itrList, accuracyList, color='blue', label='Training Accuracy')
    plt.title("Accuracy vs No. of iterations")
    plt.xlabel("No. of iterations")
    plt.ylabel("Accuracy(%)")

    lossList, itrList, accuracyList = average_perceptron_valid(valid_feat, valid_y, weightList, 15)

    plt.scatter(itrList, accuracyList, color='red', s=150)
    red_line, = plt.plot(itrList, accuracyList, color='red', label='Validation Accuracy')
    plt.legend(handles = [blue_line, red_line])
    plt.show()

    return weightList

def kernel_Matrix(X, Y, p):
    k = (1 + np.matmul(X, Y.transpose()))**p
    return k

def kernel_Perceptron(X, Y, iters, p):
    n = len(X)
    lossList = []
    itrList = []
    accuracyList = []
    alphaList = []

    alpha = np.zeros((n,))
    kernel_Mat= kernel_Matrix(X, X, p)
    itr = 0

    while (itr < iters):
        loss=0
        for i in range(n):
            u = np.sign(np.matmul(kernel_Mat[i][:], alpha * Y))
            if (u * Y[i] <= 0):
                alpha[i] = alpha[i] + 1
                loss = loss + 1

        loss = loss * 1.0/ n
        accuracy = (1-loss)*100
        itrList.append(itr+1)
        lossList.append(loss)
        accuracyList.append(accuracy)
        alphaList.append(alpha * 1)

        itr = itr + 1
    return alphaList, lossList, itrList, accuracyList, kernel_Mat

def kernel_Perceptron_valid(train_feat, train_y, valid_feat, valid_y, weightList, iters, p):
    n=len(valid_feat)
    itr=0
    lossList=[]
    itrList=[]
    accuracyList=[]
    kernel_Mat= kernel_Matrix(valid_feat, train_feat, p)

    for alpha in weightList:
        loss=0
        for i in range(0,n):
            u = np.sign(np.matmul(kernel_Mat[i][:], alpha * train_y))
            if (valid_y[i] * u <=0):
                loss = loss+1

        loss = loss * 1.0 / n
        accuracy = (1-loss)*100
        lossList.append(loss)
        itrList.append(itr+1)
        accuracyList.append(accuracy)
        itr = itr + 1
    return lossList, itrList, accuracyList

def kernel_Percep(train_feat, train_Y):
    pList=[1, 2, 3, 7, 15 ]
    maxAccuracyList = []
    for i in range(len(pList)):

        p = pList[i]
        weightList, lossList, itrList, accuracyList, kernel_mat = kernel_Perceptron(train_feat, train_y, 15, p)


        plt.scatter(itrList, accuracyList, color = 'blue', s =150)
        blue_line, = plt.plot(itrList, accuracyList, color='blue', label='Training Accuracy')
        plt.title("Accuracy(%) vs No. of Iterations".format(p))
        plt.xlabel("No. of Iterations")
        plt.ylabel("Accuracy (%)")

        #Validation
        lossList, itrList, accuracyList = kernel_Perceptron_valid(train_feat, train_y, valid_feat, valid_y, weightList, 15, p)
        maxAccur = max(accuracyList)
        maxAccuracyList.append(maxAccur)

        #Plotting for Validation Loss and Accuracy:
        plt.scatter(itrList, accuracyList, color='red', s =150)
        red_line, = plt.plot(itrList, accuracyList, color='red', label='Validation Accuracy')
        plt.legend(handles = [blue_line, red_line])
        plt.show()

    return maxAccuracyList, pList

def plot(iterations, costLists, title, legends, labels):
    colorsList = ['blue', 'red', 'green']
    print(legends)
    for i in range(0, len(iterations)):
        c = colorsList[i]
        iteration = iterations[i]
        costList = costLists[i]
        plt.plot(iteration, costList, c=c, label=legends[i], markeredgewidth=2)

    plt.ylabel(labels[0])
    plt.xlabel(labels[1])
    plt.legend()
    plt.title(title)
    plt.show()

def testvalues_y(X, W, k):
    n = len(test_feat)
    predicted_Y= []
    for i in range(n):
        u = np.sign(np.matmul(kernel_Mat[i][:], alpha_test * train_y))
        predicted_Y.append(u)

    return predicted_Y

if __name__ == '__main__':
    train_data= readCSV("pa2_train.csv")
    train_data= preprocess(train_data)
    train_y = train_data['label']
    train_y = np.array(train_y)
    train_feat = train_data.drop(['label'], axis=1)
    train_feat = np.array(train_feat)

    iters = 15
    w, accuracyList_train, iterationList_train = online_perceptron(iters, train_y, train_feat)

    print(accuracyList_train)
    print(iterationList_train)

    valid_data= readCSV("pa2_valid.csv")

    valid_data= preprocess(valid_data)

    valid_y = valid_data['label']
    valid_y = np.array(valid_y)

    valid_feat = valid_data.drop(['label'], axis=1)
    valid_feat = np.array(valid_feat)

    iters = 15
    print(len(w))
    accuracyList_valid, iterationList_valid = online_perceptron_valid(iters, valid_y, valid_feat, w)

    z = np.sign(np.dot(valid_feat, np.transpose(w)))

    print(accuracyList_valid)
    print(iterationList_valid)


    accuracy = [accuracyList_train, accuracyList_valid]
    iterations = [iterationList_train, iterationList_valid]
    legends = ["Training Data", "Validation Data"]
    labels = ["Accuracy", "Iterations'"]
    plot(iterations, accuracy, "Accuracy vs Iterations Power", legends, labels)

    #prediction file oplabel.csv
    print(accuracyList_valid[13])
    df = readCSV("pa2_test_no_label.csv")
    a = (np.array([w[13]]))
    output_y = a.dot(np.transpose(df))
    output = pd.DataFrame(np.sign(output_y)).T
    output.to_csv("oplabel.csv", index=False, index_label=False, header=False)


    #read testing data file
    test_feat = readCSV("pa2_test_no_label.csv")
    test_y = np.sign(np.dot(test_feat, np.transpose(w)))

    weightList= average_PercepPlot(train_feat,train_y)

    maxAccuracyList, pList = kernel_Percep(train_feat,  train_y)

    best_alpha = max(maxAccuracyList)
    print(best_alpha)
    print(maxAccuracyList)
    print(pList)

    plt.scatter(pList, maxAccuracyList, color='blue', s=150)
    blue_line, = plt.plot(pList, maxAccuracyList, color='blue', label='Best Validation Accuracy')
    plt.title("Best Validation Accuracy(%) vs Degrees")
    plt.xlabel("Degrees")
    plt.ylabel("Validation Accuracy (%)")
    plt.show()

    best_alpha, lossList, itrList, accuracyList, kernel_mat = kernel_Perceptron(train_feat, train_y, 15, 3)

    kernel_Mat = kernel_Matrix(test_feat, train_feat, 3)
    alpha_test = best_alpha[5]

    yvalues = testvalues_y(test_feat, alpha_test, kernel_Mat)

    output = pd.DataFrame(yvalues)
    output.to_csv("kplabel.csv", index=False, index_label=False, header=False)