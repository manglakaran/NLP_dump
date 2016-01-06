import re,sys
import operator
import matplotlib.pyplot as plt
from StringIO import StringIO
import numpy
from numpy import array
from random import randint
import math

inspace = ["[","]","?","(",")","!","{","}","<",">", ";","=","|","^"]
others  = ["%", ":"]
doubles = [">>","<<","=="]
abbrevtn = ['Dr.' , 'Esq.', 'Hon.' , 'Jr.', 'Mr.' ,'Mrs.','Ms.','Messrs.','Mmes.','Msgr.','Prof.','Rev.','Rt.','Hon.','Sr.','St.',
			'A.D.', 'B.C.', 'C.V.', 'Ph.D.', 'LL.B.', 'R.I.P.', 'Gov.', 'Inc.', 'Ltd.', 'Co.']
eng_stop = ['a','about','above','after','again','against','all','am','an','and','any','are',"aren't",'as','at','be','because','been','before','being','below','between','both','but','by',"can't",'cannot','could',"couldn't",'did',"didn't",'do','does',"doesn't",'doing',"don't",'down','during','each','few','for','from','further','had',"hadn't",'has',"hasn't",'have',"haven't",'having','he',"he'd","he'll","he's",'her','here',"here's",'hers','herself','him','himself','his','how',"how's",'i',"i'd","i'll","i'm","i've",'if','in','into','is',"isn't",'it',"it's",'its','itself',"let's",'me','more','most',"mustn't",'my','myself','no','nor','not','of','off','on','once','only','or','other','ought','our','ours  ourselves','out','over','own','same',"shan't",'she',"she'd","she'll","she's",'should',"shouldn't",'so','some','such','than','that',"that's",'the','their','theirs','them','themselves','then','there',"there's",'these','they',"they'd","they'll","they're","they've",'this','those','through','to','too','under','until','up','very','was',"wasn't",'we',"we'd","we'll","we're","we've",'were',"weren't",'what',"what's",'when',"when's",'where',"where's",'which','while','who',"who's",'whom','why',"why's",'with',"won't",'would',"wouldn't",'you',"you'd","you'll","you're","you've",'your','yours','yourself','yourselves']
puctuation = ["[","]","?","(",")","!","{","}","<",">", ";","=","|","^","%",":", '*' ,',', '.',"'","`","\"","\\","/","+","-","''" ,'``','-',"*"]

unigrams_dict = {}
ordered_list = []
num_end = [ "th","st","nd", "rd"]
cooccur = []
features_list = []
unigrams_list = []
#fractions
#a+b
#def Urlmatching():
def finddistance(vec1,vec2):
	dist=0.0
	for j in xrange(0,len(vec1)):
		dist+=pow(float(vec1[j])-float(vec2[j]),2)
	dist=math.sqrt(dist)
	return dist

def addtodict(token):
	if re.match('^(\s+|\t)$', token):
		return 
	if token is None:
		return 
	if token == '' or not token:
		return
	if token not in puctuation :
		ordered_list.append(token.lower())	
	if token not in unigrams_dict:
		unigrams_dict[token.lower()] = 1
	else : 
		unigrams_dict[token.lower()] +=1

def get_uni(token):
	#token = " (** in the beginning)  \\rho_ re.match("[^\x00-\x7F]+",a):"
	#print token
	if (token == ''):
		return

	if(len(token) == 1):
		addtodict(token)
		return
	
	token = token.strip()
	
	if token in abbrevtn:
		addtodict(token) 
		return

	if re.match("\.\.+$", token):  #for mutiple .s, 
		
		addtodict(token)
		return 

	if re.match('^([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})$',token):  #dates like 18[-/]12[-/]1990
		
		addtodict(token)    
		return
	if  token[-2:] in num_end and re.match("^\d+[a-z]{2}", token): 
		addtodict(token)
		return
	if re.match("^\d+[.,]?\d+[.,]$",token):
		addtodict(token[0:len(token)-1])
		return

	if re.match("^[+-]?\d+[.,]?\d+[a-zA-Z]*$",token) and not re.match("\d+[+-]\d+",token):  #numbers with ,. and suffixes separated
		#print token
		if(token[-1] == '.' or token[-1] == ','):
			token = token[0:len(token)-1]
			#addtodict(token[-1])
		#print token + "->"

		first = ""
		second = ""
		for i in xrange(0,len(token)):
			#print token[i]
			if(token[i].isalpha()): 
				break
			else :
				first = first + token[i]
		
		if i < len(token)-1:
			second = token[i:]
		#print first ,second
		addtodict(first)
		if second != '':
			addtodict(second)
		return
	
	if re.match("^(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})$",token): #URLs
		
		addtodict(token)
		return
	
	if re.match("^[a-zA-Z0-9:%._\+~#=]+@[\w]+.?[\w.]+$",token): #emailID
		addtodict(token)
		return
	
	if re.match("^[\d]+\/[\d]+$",token): #fractions
		
		addtodict(token)
		return
	 
	if re.match("^([A-Z][.]){1,}[A-Z]?[.]?$",token):
		if len(token) > 2:
			addtodict(token)
			return
	
	else :  #For any other special characters |.|-|"|+
		newlist = re.split(',|"|\+|\/|\.',token) #to be added ',\^*

		for x in newlist:
			if x.endswith(","):  #if endswith . separate
				addtodict(token[0:len(token)-1])
				#addtodict(",")
			elif x.endswith("."):
				addtodict(token[0:len(token)-1])
				#addtodict(".")
			else :
				addtodict(x)



def sort_list(gram):
    return sorted(gram.items(), key=operator.itemgetter(1), reverse=True)

if __name__ == '__main__':
	op = open("Data/English.txt","r")
	#check for numerals 3rd 4th

	for i in op.readlines():
		for pun in inspace:
			if pun in i:
				i = i.replace(pun," ")
		
		i = re.sub(' +',' ',i)
		i = re.sub("(\.\.+)",r' \1 ',i)
		i = re.sub('\s+',' ',i)
		tokenlist = i.split(" ")
		str_list = [x for x in tokenlist if x != '']
		
		for word in str_list:
			get_uni(word)
	for i in puctuation :	
		try:
			del unigrams_dict[i]
		except Exception as e : 
			pass

	print len(unigrams_dict) 
	#the punctuations removed from unigrams_dict

	ranked_list = sort_list(unigrams_dict)
	#print ranked_list
	#sys.exit() 
	ProcessD =  ranked_list[50:300]
	print ProcessD

	for i in ProcessD : 
		features_list.append(i[0])
	print features_list
	#print features_list	
	
	for i in unigrams_dict:
		unigrams_list.append(i)
	print len(unigrams_list)
	
	temp = []
	window = 1

	for i in xrange(0,500):
		temp.append(0.0)																																																																															
	for i in xrange(0,len(unigrams_list)):
		cooccur.append(temp[:])
	print len(cooccur)
	
	uni_ind_dict = {}
	rdic = {}
	for i in xrange(0,len(ranked_list)):
		uni_ind_dict[ranked_list[i][0]] = i
		rdic[i] = ranked_list[i][0]
	#for i in xrange(0,len(unigrams_list)):
	for k in xrange(0,len(ordered_list)):
		
		index = uni_ind_dict[ordered_list[k]]
		if k > 0 and ordered_list[k-1] in features_list: 
			cooccur[index][features_list.index(ordered_list[k-1])] +=1
		if k < len(ordered_list) -1 and ordered_list[k+1] in features_list:
			cooccur[index][features_list.index(ordered_list[k+1]) + 250] +=1
	
	for i in xrange(0,10) :  		
		print cooccur[i] , '\n'

	centroid=[]
	centers=[]

	while len(centroid)!=50:
		x=randint(0,len(unigrams_list)-1)
		if x not in centroid:
			centroid.append(x)
			centers.append(cooccur[x])

	for num in xrange(0,5):
		classlist = []
		classnames = []
		dummy = []
		for l in xrange(0,50):
			classlist.append(dummy[:])
			classnames.append(dummy[:])
		for i in xrange(0, len(cooccur)):
			inmin = 0
			indexreq = 0
			dis = 0
			for k in xrange(0,50):
				d = finddistance(cooccur[i], centers[k])
				if d == 0:
					indexreq = k
					dis = 0
					break
				else:
					if 1/d > inmin:
						indexreq = k
						inmin = 1/d
						dis = d
			classlist[indexreq].append(i)
			classnames[indexreq].append((ranked_list[i][0], dis))
		for i in xrange(0,50):
			temp = []
			for j in xrange(0,len(centers[0])):
				temp.append(0.0)
			for k in classlist[i]:
				vec = cooccur[k]
				for p in xrange(0,len(centers[0])):
					temp[p] += vec[p]
			for k in xrange(0,len(centers[0])):
				if len(classlist[i])!=0:
					temp[k]/=len(classlist[i])
			centers[i] = temp


	for j in xrange(0,len(classnames)):
		print "Cluster ", j
		print "-------------------------------------------------------------------------------"
		print "\n"
		new_one = []
		new_one = sorted(classnames[j] ,key = lambda t : t[1])[0:25]
		for i in new_one : 
			print i[0]
	