import re
import operator
import matplotlib.pyplot as plt
from StringIO import StringIO


inspace = ["[","]","?","(",")","!","{","}","<",">", ";","=","|","^"]
others  = ["%", ":"]
doubles = [">>","<<","=="]
abbrevtn = ['Dr.' , 'Esq.', 'Hon.' , 'Jr.', 'Mr.' ,'Mrs.','Ms.','Messrs.','Mmes.','Msgr.','Prof.','Rev.','Rt.','Hon.','Sr.','St.',
			'A.D.','B.C.','C.V.', 'Ph.D.', 'LL.B.', 'R.I.P.', 'Gov.', 'Inc.', 'Ltd.', 'Co.']

unigrams_dict = {}
bigrams_dict = {}
doubles = []
#fractions
#a+b
#def Urlmatching():

def addtodict(token):
	if re.match('^(\s+|\t)$', token):
		return 
	if token is None:
		return 
	if token == '' or not token:
		return
	doubles.append(token)
	while len(doubles) > 1:
		unit = str(doubles[0] + doubles[1])
		#print unit
		try:
			if unit not in bigrams_dict:
				bigrams_dict[unit] = 1
			else:
				bigrams_dict[unit] +=1
		except Exception as e :
			print "error" , e
		doubles.pop(0)

def get_uni(token):
	#token = " (** in the beginning)  \\rho_ re.match("[^\x00-\x7F]+",a):"
	#print token
	start = 0
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


	if re.match("^[+-]?\d+[.,]?\d+[a-zA-Z]*$",token) and not re.match("\d+[+-]\d+",token):  #numbers with ,. and suffixes separated
		save  = ""
		if(token[-1] == '.' or token[-1] == ','):
			token = token[0:len(token)-1]
			save = token[-1]
		#print token + "->"

		first = ""
		second = ""
		for i in xrange(0,len(token)):
			#print token[i]
			if(token[i].isalpha()): 
				break
			else :
				first = first + token[i]
		#print i
		if i < len(token)-1:
			second = token[i:]
		#print first ,second
		addtodict(first)
		if second != '':
			addtodict(second)
		if save != '':
			addtodict(save)
		return
	
	if re.match("^(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})$",token): #URLs
		
		addtodict(token)
		return
	
	if re.match("^[a-zA-Z0-9:%._\+~#=]+@[\w]+.?[\w.]+$",token): #emailID
		
		addtodict(token)
		return
	
	if re.match("[\w]+'s", token) :  #for words like Hero's

		list1=token.split("'s")
		#print list1
		if len(list1) > 0 :
			for p in list1:
				addtodict(p) 
		addtodict("'s")
		return

	if re.match("^[\d]+\/[\d]+$",token): #fractions
		
		addtodict(token)
		return
	
	# multiple stars in the beginning 

	
	if re.match("^([A-Z][.]){1,}[A-Z]?[.]?$",token):
		if len(token) > 2:
			#print token
			addtodict(token)
			return
	


	else :  #For any other special characters |.|-|"|+
		#print token 
		#print token
		
		newlist = re.split(',|"|\-|\+|\/|\.',token) #to be added ',\^*
		prev = set(token)
		new_s = ""
		for x in newlist:
			new_s += x
		new = set(new_s)
		change  = prev - new
		#print newlist
		for x in change:
			addtodict(x)
		for x in newlist:
			if x.endswith(","):  #if endswith . separate
				addtodict(token[0:len(token)-1])
				addtodict(",")
			elif x.endswith("."):
				addtodict(token[0:len(token)-1])
				addtodict(".")
			elif x.endswith(":"):
				addtodict(token[0:len(token)-1])
				addtodict(":")
			else :
				addtodict(x)

def find_x_y_for_plotting(ranked_list, dicts):
    dict_plot={}
    f1 = open("output_bi_eng.txt", "w")
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
	op = open("../../Datasets/English.txt","r")
	#op = open("Datasets/test.txt","r")
	
	for i in op.readlines():
		for pun in inspace:
			if pun in i:
				i = i.replace(pun," " + pun + " ")
		i = re.sub(r'<  <','<<',i)
		i = re.sub(r'>  >','>>',i)
		i = re.sub(r'=  =','==',i)
		i = re.sub(' +',' ',i)
		i = re.sub("(\.\.+)",r' \1 ',i)
		i = re.sub('\s+',' ',i)
		tokenlist = i.split(" ")
		str_list = [x for x in tokenlist if x != '']
		
		#print i
		for word in str_list:
			get_uni(word)
	#print unigrams_dict	
	
	ranked_list = sort_list(bigrams_dict)  
	dict_plot=find_x_y_for_plotting(ranked_list, bigrams_dict)
	plot(dict_plot.keys()[:100],dict_plot.values()[:100]) 
    				
    	
