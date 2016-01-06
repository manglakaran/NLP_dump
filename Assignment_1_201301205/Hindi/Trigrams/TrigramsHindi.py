import re
import operator
import matplotlib.pyplot as plt
from StringIO import StringIO


inspace = ["[","]","?","(",")","!","{","}","<",">", ";","=","|"]
others  = ["%","^", ":"]
doubles = [">>","<<","=="]

unigrams_dict = {}
trigrams_dict = {}
triples = []
#fractions
#a+b
#def Urlmatching():

def addtodict(token):
	triples.append(token)
	while len(triples) > 2:
		unit = str(triples[0] + ' ' + triples[1] + ' ' + triples[2])
		#print unit
		try:
			if unit not in trigrams_dict:
				trigrams_dict[unit] = 1
			else:
				trigrams_dict[unit] +=1
		except Exception as e :
			print "error" , e
		triples.pop(0)

def get_uni(token):
	#token = " (** in the beginning)  \\rho_ re.match("[^\x00-\x7F]+",a):"
	#print token
	if(len(token) == 1):
		addtodict(token)
		return
	
	token = token.strip()
	

	if re.match("\.\.+$", token):  #for mutiple .s, 
		#print token
		addtodict(token)
		return 

	
	if (token == ''):
		return

	if re.match('[0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4}',token):  #dates like 18[-/]12[-/]1990
		addtodict(token)    
		return


	elif re.match("[+-]?\d+[.,]?\d+[a-zA-Z]*",token) and not re.match("\d+[+-]\d+",token):  #numbers with ,. and suffixes separated
		#print token
		if(token[-1] == '.'):
			token = token[0:len(token)-1]
			addtodict(token)
			addtodict(".")
		else:
			addtodict(token)
		return
	
	elif re.match("[\d]+\/[\d]+",token): #fractions
		addtodict(token)
		return

	else :  
		addtodict(token)
		

def find_x_y_for_plotting(ranked_list, dicts):
    dict_plot={}
    f1 = open("output_tri_hi.txt", "w")
    for i in range(len(ranked_list)):
     #  print i
        word = ranked_list[i][0]                
     #   print word
        dict_plot[i+1] = dicts[word] 
        f1.write(word+"\t\t:\t"+str(dicts[word])+"\n")
    
    f1.close()
    return dict_plot

def sort_list(gram):
    return sorted(gram.items(), key=operator.itemgetter(1), reverse=True)
    
def plot(x,y):
    
    plt.plot(x, y)
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.show()


if __name__ == '__main__':
	op = open("../../Datasets/Hindi.txt","r")
	#op = open("Datasets/test.txt","r")
	
	for i in op.readlines():
		for pun in inspace:
			if pun in i:
				i = i.replace(pun," " + pun + " ")
		
		
		i = re.sub(' +',' ',i)
		i = re.sub("(\.\.+)",r' \1 ',i)
		i = re.sub('\s+',' ',i)
		tokenlist = i.split(" ")
		str_list = [x for x in tokenlist if x != '']
		
		#print i
		for word in str_list:
			get_uni(word)
	#print unigrams_dict	
	
	ranked_list = sort_list(trigrams_dict)  
	dict_plot=find_x_y_for_plotting(ranked_list, trigrams_dict)
	plot(dict_plot.keys()[:1500],dict_plot.values()[:1500]) 
    				
    	
