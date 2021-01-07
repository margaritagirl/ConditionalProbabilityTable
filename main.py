#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


data = pd.read_excel('data.xlsx')


# ### Checking for no. of Questions

# In[3]:


data.qcode.unique()


# ### Sample Row of Dataframe

# In[4]:


data.iloc[1]


# ### No. of Students

# In[5]:


len(data.userID.unique())


# ### Redefining data with only relevant columns

# In[7]:


mod_data = data[['userID', 'qcode', 'R']]


# ### Storing Question Identifier, Student Identifier 

# In[8]:


qid = list(np.sort(np.array(mod_data.qcode.unique())))
studID = list(np.sort(np.array(mod_data.userID.unique())))


# ### Augmenting Data for Missing Responses 
# #### There are entries for students where they have answered only some questions, say Question 1, Question 4, and not all of them. We augment the dataset so that there is a response for each question for each student.
# #### Note: Skipping a question (R = 2) means the answer to that question is wrong (Assumption\)

# In[9]:


final_data = []

for item in studID:
    for element in qid:
        temp = mod_data[(mod_data['userID'] == item) & (mod_data['qcode'] == element)]
        
        if(temp.empty == False):
            obj = list(temp.iloc[0, :])
            final_data.append(obj)
        else:
            obj = [item, element, 0]
            final_data.append(obj)


# ### Checking length of augmented data (No.of Students * 5)

# In[10]:


len(final_data)


# In[11]:


df = pd.DataFrame(final_data, columns=['userID', 'qcode', 'R'])


# ### Replacing R = 2 with 0 (from Assumption)

# In[12]:


df = df.replace(2, 0)


# ### Calculating Probabilities of Each Question correctly answered

# In[13]:


qid_prob = []

for element in qid:
    qid_prob.append(df[df.qcode == element].R.sum()/len(final_data))


# In[14]:


for idx, item in enumerate(qid_prob):
    print('P(Question {} correctly answered) = \t'.format(idx + 1), item)


# ### Calculating Intersection Probabilties

# In[15]:


intersection = np.zeros((len(qid), len(qid)))

for item in studID:
    
    each_student = df[df.userID == item]
    response = []
    
    for element in qid:
        each_question = each_student[each_student.qcode == element]
        response.append(each_question.iloc[0, 2])
    
    for idx in range(len(response)):
        for item in range(len(response)):
            intersection[idx][item] += response[idx]*response[item]
        


# In[16]:


intersection = intersection/len(final_data)


# ### Calculating Conditional Probabilities

# In[21]:


cp_array = intersection/np.array(qid_prob)


# ### Write to .csv

# In[18]:


columns = ['X', 'Q1 is correct', 'Q2 is correct', 'Q3 is correct', 'Q4 is correct', 'Q5 is correct']


# In[24]:


fields = [list(cp_array[item]) for item in range(cp_array.shape[0])]

for idx, item in enumerate(fields):
    item[idx] = 'N/A'
    item.insert(0, 'P(Question {} is answered correctly | X)'.format(idx + 1))


# In[19]:


import csv


# In[26]:


with open('CPT.csv', 'w') as csvfile: 
    csvwriter = csv.writer(csvfile) 
      
    csvwriter.writerow(columns) 
      
    csvwriter.writerows(fields)


# In[27]:


cpt = pd.read_csv('CPT.csv')


# ### Conditional Probability Table

# In[28]:


cpt
