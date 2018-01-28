import urllib
from nltk import pos_tag, word_tokenize
from bs4 import BeautifulSoup
import os.path
import xml.etree.ElementTree as etree
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from collections import Counter
import operator
import math
import time


def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i


def search_in_index(token1, doc_index) :
	sorted_token = sorted(doc_index[token1], key=operator.itemgetter(1),reverse=True)
	print "You searched for documents related to the term:'"+str(token1)+"'. Results in descending order based on weight:"
	for y in sorted_token:
		print "document ID: " + str(y[0]) +"  ---->  weight: "+str(y[1])


def inverted_index_add(Counted, filename_plain, doc_index,list2):
    for word, occurences in Counted.iteritems():
		#getting the number of files containing the word
		files_containing_word = sum(1 for j in list2 if word in j)
		idf = math.log(len(list2) / (1 + files_containing_word))
		tf_idf = occurences * idf
		temp_dict = [filename_plain,tf_idf]
		if word in doc_index:
			# append the new occurences of the file to the existing array at this slot
			doc_index[word].append(temp_dict)
		else:
			# create a new array in this slot
			doc_index[word] = [temp_dict]

    return Counted

url = "C:/Users/panos/Desktop/Ceid/Glwssiki/Project 2016-2017/5496_Ling_Tech_Project_2016-2017/PartA/Some_Crawler_files_and_Tagged_files/ScrapedFiles/"
doc_index = dict()
root = etree.Element("inverted_index")
all_tokens = []
for filename in os.listdir(url):
	file = open((url+filename), 'r')
	reader = file.read()
	soup = BeautifulSoup(reader, "html.parser")
	filename_plain = filename[:-5]
	# kill all script and style elements
	for script in soup(["script", "style", "a"]):
		script.extract()    # rip it out

	#finding the title of the article based on the specific tag it has 
	strongTag = soup.strong
	
	#clearing the character encodings as much as posible
	article_title = strongTag.contents[0].replace(u"6\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", '"')
	
	#finding the text data in the html code (in paragraphs <p> in a specific <div>)
	text_data = [td.find('p') for td in soup.findAll("div", { "class" : "pn_body_content_fbia" })]
	
	#clearing the tags from the text
	soup = BeautifulSoup(str(text_data), "html.parser")
	article_text = soup.get_text()
	article_text.encode("ascii", "ignore")
	
	#tokenizing the text
	tok = word_tokenize(article_text)
	
	#need to save all of the tokens of each file in order to calculate each term's idf
	all_tokens.extend(tok)
	
	#POS tagging the tokens
	tok_tagged = pos_tag(tok)
	
	#saving the POS tagged tokens in a .txt file
	filename2 = filename[:-5]+'.txt'
	with open(os.path.join('C:/Users/panos/Desktop/Ceid/Glwssiki/Project 2016-2017/5496_Ling_Tech_Project_2016-2017/PartA/Some_Crawler_files_and_Tagged_files/TaggedFiles/', filename2), 'wb') as f:
		f.write(str(tok_tagged))
	
	#keeping only the open tagged words
	temp_list = ["test","NN"]
	for i, (word,tag) in enumerate(tok_tagged):
		wntag = tag[0].lower()
		wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
		if wntag != None:		
			temp_list.append(tok_tagged[i])
	
	#lemmatization
	wnl = WordNetLemmatizer()	
	lemma_list = []	
	for j in enumerate(temp_list):
		wntag = j[1][1][0].lower()

		wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
		if not wntag:
			lemma = j[1][0]
		else:
			lemma = wnl.lemmatize(str(j[1][0]), wntag)
		lemma_list.append(lemma)
	
	#counting occurence of every term
	Counted = Counter(lemma_list)
	
	#add the words of this document to the general inverted index
	inverted_index_add(Counted, filename_plain, doc_index,all_tokens)
start_time = time.time()


#simple search of a word in the general inverted index	
search_in_index('find', doc_index)
print("--- %s seconds ---" % (time.time() - start_time))



#creating the XML representation of the index
for word, tf_idf in doc_index.iteritems():
	lemma = etree.SubElement(root, "lemma", name=word)
	
	for j in range(len(tf_idf)):
		document = etree.SubElement(lemma, "document", id=str(tf_idf[j][0]), weight=str(tf_idf[j][1]))

#calling the function that "prettyfies" the xml structure to make it more readable
indent(root)

#writing the XML tree into a file named "inv_file.xml"
tree = etree.ElementTree(root)
tree.write("inv_file.xml", xml_declaration=True, encoding='utf-8', method="xml")

#leaving the XML parsing method commented as we dont know for sure that an index is already created
#if it needs to be used, then simply "uncomment" it.
'''
tree = etree.parse('inv_file.xml')
root = tree.getroot()
doc_index = {}
k=0
for element in root.iter():
	if (element.get("name")!= None):
		lemma_name = element.get("name")
		doc_index[lemma_name]=[]
	else:
		if k!=0 :
			if doc_index[lemma_name]==[]:
				doc_index[lemma_name].append([element.get("id"),float(element.get("weight"))])
			else:
				doc_index[lemma_name].append([element.get("id"),float(element.get("weight"))])
	k=1
'''

