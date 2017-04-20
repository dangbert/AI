'''
Name:
Date:
Project 3: Decision trees

Please do not change the signature of train() or classify(), 
or you will break the test suite.
'''

#the following are the values for each attibute in the global context so you can use them as needed
work_class = ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Without-pay", "Never-worked"]

education = ["Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm", "Assoc-voc", "9th", "7th-8th", "12th", 
             "Masters", "1st-4th", "10th", "Doctorate", "5th-6th", "Preschool"]

marital = ["Married-civ-spouse", "Divorced", "Never-married", "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"]

occupation = ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty", "Handlers-cleaners", 
              "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", 
              "Armed-Forces"]

relationship = ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"]

race = ["White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other", "Black"]

sex = ["Female", "Male"]

native_country = ["United-States", "Cambodia", "England", "Puerto-Rico", "Canada", "Germany", "Outlying-US(Guam-USVI-etc)", 
                  "India", "Japan", "Greece", "South", "China", "Cuba", "Iran", "Honduras", "Philippines", "Italy", "Poland", 
                  "Jamaica", "Vietnam", "Mexico", "Portugal", "Ireland", "France", "Dominican-Republic", "Laos", "Ecuador", 
                  "Taiwan", "Haiti", "Columbia", "Hungary", "Guatemala", "Nicaragua", "Scotland", "Thailand", "Yugoslavia", 
                  "El-Salvador", "Trinadad&Tobago", "Peru", "Hong", "Holand-Netherlands"]

def train(data, labels):
    """
    This function should train a decision tree classifier
    on the data. It should return a usable decision tree.
    How you implement the decision tree is up to you 
    (class, dictionary, etc.), but do not use any python packages
    such as scikit-learn. 

    data: a list of attribute vectors, the entire dataset in integer form
    labels: a list of class labels that correspond to the dataset
    """
    return 1

def classify(x, model):
    """
    Given a some data point (known or not) x, this function 
    should apply the model (trained in the above function)
    and return the classification of x based on the model. 
    
    x: a single integer attribute vector for an adult
    """
    return 1

def convert(data_list):
    """This function converts the categorical values of data_list into integers """

    attributes = [work_class, education, marital, occupation, relationship, race, sex, native_country]

    converted_data = []

    for attribute_value in data_list:

        for attribute_values in attributes:

            if attribute_value in attribute_values:
                converted_data.append(attribute_values.index(attribute_value))

    return converted_data
    
def main():

    LABELS = ["<=50K",">50K"]

    #here is some code that reads the data from the current dir
    #feel free to change this as you wish
    with open("adult.data") as f:
        data = []
        labels = []
        for line in f:

            #skip bad data
            if len(line) < 10 or "?" in line:
                continue

            line = line.strip().split(",")
            data.append(convert(line[:-1]))
            labels.append(LABELS.index(line[-1]))

    '''
    #example run:
    dT = train(data, labels)
    sample = ["Private","Bachelors","Married-civ-spouse","Exec-managerial","Husband","Asian-Pac-Islander","Male","Japan"] #>50K
    sample = convert(sample)
    lbl = classify(sample, dT)
    print(sample, lbl)
    '''

if __name__ == "__main__":
    main()
