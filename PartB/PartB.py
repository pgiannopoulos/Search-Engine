import glob
import urllib
from nltk import pos_tag, word_tokenize
import os.path
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from collections import Counter
import operator
from nltk.stem import PorterStemmer
from scipy import linalg, mat, dot
import math
from decimal import Decimal
import numpy as np

def tf_idf_calculation(stem,occurences,list2):
	#getting the number of files containing the stem
	files_containing_stem = sum(1 for j in list2 if stem in j)
	idf = math.log(len(list2) / (1 + files_containing_stem))
	tf_idf = occurences * idf
	return tf_idf

def total_stems_add(Counted, total_stems_E,list2):
	for stem, occurences in Counted.iteritems():
		#getting the number of files containing the stem
		files_containing_stem = sum(1 for j in list2 if stem in j)
		idf = math.log(len(list2) / (1 + files_containing_stem))
		tf_idf = occurences * idf
		if stem in total_stems_E:
			# append the tf-idf of the file to the existing array at this slot
			total_stems_E[stem] += tf_idf
		else:
			# create a new array in this slot
			total_stems_E[stem] = tf_idf

#creating the collection A
A_rec_files = glob.glob('C:\\Users\\panos\\Desktop\\Ceid\\Glwssiki\\Project 2016-2017\\5496_Ling_Tech_Project_2016-2017\\PartB\\collection_A\\rec.test\\*')
A_sci_files = glob.glob('C:\\Users\\panos\\Desktop\\Ceid\\Glwssiki\\Project 2016-2017\\5496_Ling_Tech_Project_2016-2017\\PartB\\collection_A\\sci.test\\*')
A_files = A_rec_files + A_sci_files
print('-----------------------------------------')
print('|Initialization has begun.|')
print('-----------------------------------------')
print('Length of collection A is: ')+str(len(A_files))
print('-----------------------------------------')
#creating the collection E
E_rec_files = glob.glob('C:\\Users\\panos\\Desktop\\Ceid\\Glwssiki\\Project 2016-2017\\5496_Ling_Tech_Project_2016-2017\\PartB\\collection_E\\rec.train\\*')
E_sci_files = glob.glob('C:\\Users\\panos\\Desktop\\Ceid\\Glwssiki\\Project 2016-2017\\5496_Ling_Tech_Project_2016-2017\\PartB\\collection_E\\sci.train\\*')
E_files = E_rec_files+ E_sci_files
print('Length of collection E is: ')+str(len(E_files))
print('-----------------------------------------')
#categorizing the files of the collection E
E_categorized = {}
for i in range(len(E_rec_files)):
    E_categorized[E_rec_files[i]] = 'rec'
for j in range(len(E_sci_files)):
    E_categorized[E_sci_files[j]] = 'sci'
print('All E_files have been categorized')
print('-----------------------------------------')
#creating the Porter stemmer named "ps"
ps = PorterStemmer()

#creating a list to hold each documents stems so they can be counted
stems = []

#creating the dictionary to hold all of the stems with their weights
total_stems_E = dict()

#-------------------------CREATION OF THE CHAR. SPACE "S"-----------------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
print('Initiating the creation the characteristic space S')
print('-----------------------------------------')
stems_all_E = []
for i in range (len(E_files)):
	#reading the text from each file
	temp = open(E_files[i])
	text = temp.read().decode('utf8', 'ignore')
	temp.close()	
	#tokenizing the text
	tok = word_tokenize(text)
	#creating the vector of stems for each file
	stems = [ps.stem(j) for j in tok]
	#need to save all of the stems of each file in order to calculate each term's idf
	stems_all_E.extend(stems)
	#counting occurence of every stem
	Counted = Counter(stems)
	#adding the stems of this document to the total_stems_E dictionary
	total_stems_add(Counted,total_stems_E,stems_all_E)
#sorting the total dictionary to get the first 500 stems, based on tf-idf
sorted_total_stems_E = sorted(total_stems_E.items(), key=operator.itemgetter(1), reverse=True)

#creating the characteristics space S based on the 500 most used stems in the collection E
S_space = []
for key, value in sorted_total_stems_E[:500]:
	S_space.append(key)
print('Done! Length of characteristic space S is: ')+str(len(S_space))
print('-----------------------------------------')
#------------------CREATION OF THE VECTORS OF THE COLLECTION E FILES------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
print('Initiating the creation of the characteristic vectors for each file of collection E')
print('-----------------------------------------')
E_files_stems = []
for i in range (len(E_files)):
	E_files_stems.append([])
	#reading the text from each file
	temp = open(E_files[i])
	text = temp.read().decode('utf8', 'ignore')
	temp.close()	
	#tokenizing the text
	tok = word_tokenize(text)
	#creating the vector of stems for each file
	stems = [ps.stem(j) for j in tok]
	#need to save all of the stems of each file in order to calculate each term's idf
	stems_all_E.extend(stems)
	#counting occurence of every stem
	Counted = Counter(stems)
	for k in S_space:
		#creating the vector for each file that holds every S_space stem's occurences
		E_files_stems[i].append(tf_idf_calculation(k,Counted[k],stems_all_E))
print('TF-IDF for each stem of each file from collection E has been calculated')
print('-----------------------------------------')
print('Characteristic vectors for all files of collection E have been created ')
print('-----------------------------------------')
#------------------CREATION OF THE VECTORS OF THE COLLECTION A FILES------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------	
print('Initiating the creation the characteristic vectors for each file of collection A')
print('-----------------------------------------')
A_files_stems = []
stems_all_A = []
for i in range (len(A_files)):
	A_files_stems.append([])
	#reading the text from each file
	temp = open(A_files[i])
	text = temp.read().decode('utf8', 'ignore')
	temp.close()	
	#tokenizing the text
	tok = word_tokenize(text)
	#creating the vector of stems for each file
	stems = [ps.stem(j) for j in tok]
	#need to save all of the stems of each file in order to calculate each term's idf
	stems_all_A.extend(stems)
	#counting occurence of every stem
	Counted = Counter(stems)
	for k in S_space:
		#creating the vector for each file that holds every S_space stem's occurences
		A_files_stems[i].append(tf_idf_calculation(k,Counted[k],stems_all_A))		
print('TF-IDF for each stem of each file from collection A has been calculated')
print('-----------------------------------------')
print('Characteristic vectors for all files of collection A have been created ')
print('-----------------------------------------')
#------------------COSINE SIMILARITY TO ADJUST A_FILES TO A CATEGORY------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
print('Initiating cosine coefficient calculation')
print('-----------------------------------------')
A_categorized_cosine = {}
n=0
for i in A_files_stems:
	temp_a = mat(i)
	cosine_sim = -500
	for j in E_files_stems:
		temp_e = mat(j)
		c = dot(temp_a,temp_e.T)/linalg.norm(temp_a)/linalg.norm(temp_e)
		if (c > cosine_sim):
			cosine_sim = c
			most_similar = E_files_stems.index(j)
	#categorizing the files of the collection A
	category = E_categorized[E_files[most_similar]]
	A_categorized_cosine[A_files[n]] = category
	if (n>10)&(n<17):
		if (n==11):
			print('Presenting some results of the categorization of the A files:')
			print('-----------------------------------------')
		print('File ID: ')+str(A_files[n])+' belongs to category: '+str(category)
		print('-----------------------------------------')
	n += 1
print('Completed cosine coefficient calculation')
print('-----------------------------------------')
#------------------TANIMOTO SIMILARITY TO ADJUST A_FILES TO A CATEGORY------------------------
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------	
'''A_categorized_tanimoto = {}
n=0
def tanimoto(a,b):
	return sum(abs(x-y) for x,y in zip(a,b))
	
for i in A_files_stems:
	temp_a = mat(i)
	tanimoto_sim = -500
	for j in E_files_stems:
			temp_e = mat(j)
			c = sum(abs(x-y) for x,y in zip(temp_a,temp_e))
			if (c > tanimoto_sim):
				tanimoto_sim = c
				most_similar = E_files_stems.index(j)
	#categorizing the files of the collection A
	category = E_categorized[E_files[most_similar]]
	A_categorized_tanimoto[A_files[n]] = category
	print A_categorized_tanimoto[A_files[n]]
	n += 1
'''