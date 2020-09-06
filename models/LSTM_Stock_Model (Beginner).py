# https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/
# multivariate output stacked lstm example
from numpy import array
from numpy import hstack
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import pandas as pd


# split a multivariate sequence into samples
def split_sequences(sequences, n_steps):
    X, y = list(), list()
    for i in range(len(sequences)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the dataset
        if end_ix > len(sequences) - 1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)


df_ge = pd.read_csv("../data/sample/sp500.training.txt", engine='python')
df_td = pd.read_csv("../data/sample/sp500.test.txt", engine='python')

# define input sequence
# in_seq1 = array([10, 20, 30, 40, 50, 60, 70, 80, 90])
# in_seq2 = array([15, 25, 35, 45, 55, 65, 75, 85, 95])
# out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])

in_seq1 = df_ge["Close"]
in_seq2 = df_ge["Open"]
in_seq3 = df_ge["GDP"]
in_seq4 = df_ge["Fund_Rate"]

out_seq = []
for i in range(len(in_seq1)):
    if in_seq1[i] - in_seq2[i] > 0:
        out_val = 1
    else:
        out_val = 0
    out_seq.append(out_val)
out_seq = array(out_seq)

# convert to [rows, columns] structure
in_seq1 = in_seq1.values.reshape((len(in_seq1), 1))
in_seq2 = in_seq2.values.reshape((len(in_seq2), 1))
in_seq3 = in_seq3.values.reshape((len(in_seq3), 1))
in_seq4 = in_seq4.values.reshape((len(in_seq4), 1))
out_seq = out_seq.reshape((len(out_seq), 1))

# horizontally stack columns
# dataset = hstack((in_seq1, in_seq2, in_seq3, out_seq))
dataset = hstack((in_seq1, in_seq2, in_seq3, in_seq4, out_seq))

# choose a number of time steps
n_steps = 30

# convert into input/output
X, y = split_sequences(dataset, n_steps)

# the dataset knows the number of features, e.g. 2
n_features = X.shape[2]

# define model
model = Sequential()
model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
model.add(LSTM(100, activation='relu'))
model.add(Dense(n_features))
model.compile(optimizer='adam', loss='mse')

# fit model
model.fit(X, y, epochs=100, verbose=0)
# demonstrate prediction

# x_input = array([[70,75,5], [80,85,5], [90,95,5]])
# x_input = array([[22.879, 23.133000000000003, -0.25400000000000134], [22.46, 22.834, -0.3739999999999988], [21.974, 22.331999999999997, -0.357999999999997]])

t_seq1 = df_td["Close"]
t_seq2 = df_td["Open"]
t_seq3 = df_td["GDP"]
t_seq4 = df_td["Fund_Rate"]
t_out = array([t_seq2[i] - t_seq1[i] for i in range(len(t_seq1))])

x_input = []
for i in range(len(t_seq1)):
    tempArray = [t_seq1[i], t_seq2[i], t_seq3[i], t_seq4[i], t_out[i]]
    x_input.append(tempArray)

# print (x_input)

x_input = array(x_input)
x_input = x_input.reshape((1, n_steps, n_features))
yhat = model.predict(x_input, verbose=0)
print(yhat)

# saving model
model.save('../models/trained_model')

# print(t_out)

# if (yhat[2] < 0):
# 	print("Stock price will drop")
# elif (yhat[2] == 0):
# 	print("Stock price will stay the same")
# else:
# 	print("Stock price will increase")
