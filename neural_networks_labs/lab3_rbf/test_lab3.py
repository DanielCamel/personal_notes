import numpy as np
from itertools import product, combinations
import collections
import pandas as pd
import matplotlib.pyplot as plt

def Activation_function(net):
    if net >= 0:
        return 1
    return 0

def СalculationPhi(x_values, neuron_arr):
    phi=0
    for i in range(len(neuron_arr)):
        phi+=(x_values[i]-neuron_arr[i])*(x_values[i]-neuron_arr[i])*(-1)
    return np.exp(phi)


def СalculationNet(weights,x_values,center_neurons_arrays):
    net = 0
    for i in range(len(center_neurons_arrays)):
        phi = СalculationPhi(x_values, center_neurons_arrays[i])
        net += weights[i+1] * phi
    net += weights[0]
    return net

def Find_neuron_centers(matrixData,SampleVector):
    fal=0
    tru=0
    vic=0
    neuron_centers=[]
    for i in range(len(SampleVector)):
        if SampleVector[i]==0:
            fal=fal+1
        else:
            tru=tru+1
    if fal<=tru:
        vic=0

    else:
        vic=1
    for i in range(len(SampleVector)):
        if SampleVector[i]==vic:
            neuron_centers.append(matrixData[i])
    return neuron_centers



def LearningProcess(matrixData,SampleVector,vector_lerning,sample_lerning, n=0.3, eralim = False):
  
    neuron_centers = Find_neuron_centers(matrixData,SampleVector)
    weights = []
    vector_y=[]
    for i in range(len(neuron_centers)+1):
        weights.append(1)
    for i in range(len (SampleVector)):
        net = СalculationNet(weights, matrixData[i], neuron_centers)
        vector_y.append(Activation_function(net))
    error=0
    for i in range(len (SampleVector)):
        if SampleVector[i]!=vector_y[i]:
            error=error+1
    hamming_distance = error
    error=0
    generation = 0
    data = {'Номер эпохи': list(), 'Вектор весов w': list(), 'Выходной вектор y': list(),
            'Суммарная ошибка Е': list()}
 
    while hamming_distance != 0:  
        generation_s_weights = weights.copy()
        for i in range(len(sample_lerning)):  
            net = СalculationNet(weights, vector_lerning[i], neuron_centers)
            y= Activation_function(net)
            error = sample_lerning[i] - y
            phi_array = [1] + [СalculationPhi(vector_lerning[i], neuro_i) for neuro_i in neuron_centers]
            delta = n * error * np.array(phi_array)
            for i in range(len(weights)):
                weights[i] += delta[i]
        error=0
        generation_s_y = list()
        for i in range(len (SampleVector)):
            net = СalculationNet(weights, matrixData[i], neuron_centers)
            y= Activation_function(net)
            generation_s_y.append(y)
            if SampleVector[i]!=generation_s_y[i]:
                error=error+1
        hamming_distance = error
        data['Номер эпохи'].append(generation)
        data['Вектор весов w'].append(np.round(generation_s_weights, 3))
        data['Выходной вектор y'].append(generation_s_y)
        data['Суммарная ошибка Е'].append(hamming_distance)
        generation += 1

        if eralim - 1 == 0:
            return data, False
        if eralim:
            eralim -= 1

    return data,True



def FindLessProcess(matrixData,SampleVector,n=0.3, lim=30 ):
    sample = list()
    sample_data = None
    vector_y=[]
    flag=False
    
    for index in range(2, len(matrixData)+1):
        all_combinations = list(combinations(matrixData, index))
        print('Проверка набора длины ' + str(index))
        for subset in all_combinations:
            vector_y=[]
            for inter in range(0, len(subset)):
                Irt=matrixData.index(subset[inter])
                vector_y.append(SampleVector[Irt])
            data,flag=LearningProcess(matrixData,SampleVector,subset,vector_y, n,lim)
            if flag:
                sample = subset
                sample_data = data
                return sample, sample_data

    return sample, sample_data



matrixData =[[ 0, 0, 0, 0 ],
    [ 0, 0, 0, 1 ],
    [ 0, 0, 1, 0 ],
    [ 0, 0, 1, 1 ],
    [ 0, 1, 0, 0 ],
    [ 0, 1, 0, 1 ],
    [ 0, 1, 1, 0,],
    [ 0, 1, 1, 1,],
    [ 1, 0, 0, 0,],
    [ 1, 0, 0, 1,],
    [ 1, 0, 1, 0,],
    [ 1, 0, 1, 1,],
    [ 1, 1, 0, 0,],
    [ 1, 1, 0, 1,],
    [ 1, 1, 1, 0,],
    [ 1, 1, 1, 1,]]
    
SampleVector = [ 0,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0 ]

print('\nОбучение на полном наборе: ')
data = LearningProcess(matrixData,SampleVector,matrixData,SampleVector)[0]
print(pd.DataFrame(data).to_string())
plt.figure(figsize=(8, 6))
plt.subplot(2, 2, 1)
plt.plot(data['Номер эпохи'], data['Суммарная ошибка Е'], marker='.', color='red')
plt.plot(data['Номер эпохи'], data['Суммарная ошибка Е'], marker='.', color='darkred', markerfacecolor='white')
plt.title('Cуммарная ошибка НС на всей выборке')
plt.xlabel('Номер эпохи')
plt.ylabel('Суммарная ошибка Е')
plt.grid()

print('\nПоиск минимального набора: ')
sample, sample_data = FindLessProcess(matrixData,SampleVector)
print('\nМинимальный набор:\n' + str(sample))
print(pd.DataFrame(sample_data).to_string())
pd.DataFrame(sample_data).to_csv('data_min_set.csv', sep=';', encoding='cp1251')

plt.subplot(2, 2, 2)
plt.plot(sample_data['Номер эпохи'], sample_data['Суммарная ошибка Е'], marker='.', color='red')
plt.plot(sample_data['Номер эпохи'], sample_data['Суммарная ошибка Е'], marker='.', color='darkred', markerfacecolor='white')

plt.title('Cуммарная ошибка НС на мин выборке ')
plt.xlabel('Номер эпохи\n'+'\nМинимальная выборка:\n'+str(sample))
plt.ylabel('Суммарная ошибка Е')
plt.grid()

plt.show()
