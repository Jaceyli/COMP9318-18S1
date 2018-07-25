import pandas as pd
import submission as submission


raw_data = pd.read_csv('./asset/data.txt', sep='\t')
# print(raw_data.head())

def tokenize(sms):
    return sms.split(' ')

def get_freq_of_tokens(sms):
    tokens = {}
    for token in tokenize(sms):
        if token not in tokens:
            tokens[token] = 1
        else:
            tokens[token] += 1
    return tokens

training_data = []
for index in range(len(raw_data)):
    training_data.append((get_freq_of_tokens(raw_data.iloc[index].text), raw_data.iloc[index].category))







sms = 'I am not spam'

# submission.train(training_data)
print(submission.multinomial_nb(training_data, tokenize(sms)))