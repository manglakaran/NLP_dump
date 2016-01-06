import re
import operator
import matplotlib.pyplot as plt
from StringIO import StringIO


inspace = ["[","]","?","(",")","!","{","}","<",">", ";","=","|"]
others  = ["%","^", ":"]
doubles = [">>","<<","=="]

unigrams_dict = {}
bigrams_dict = {}
doubles = []
#fractions
#a+b
#def Urlmatching():

def addtodict(token):
	#if token not in unigrams_dict:
	#	unigrams_dict[token] = 1
	#else : 
	#	unigrams_dict[token] +=1
	doubles.append(token)
	while len(doubles) > 1:
		unit = str(doubles[0] + ' ' + doubles[1])
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
	if (token == ''):
		return
	addtodict(token)
	return

	
	

def find_x_y_for_plotting(ranked_list, dicts):
    dict_plot={}
    f1 = open("output_bi_tel.txt", "w")
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
	op = open("../../Datasets/Telugu.txt","r")
	#op = open("Datasets/test.txt","r")
	
	for i in op.readlines():
		for pun in inspace:
			if pun in i:
				i = i.replace(pun," " + pun + " ")
		#i = re.sub(r'<  <','<<',i)
		#i = re.sub(r'>  >','>>',i)
		#i = re.sub(r'=  =','==',i)
		i = re.sub(' +',' ',i)
		i = re.sub("(\.\.+)",r' \1 ',i)
		i = re.sub('\s+',' ',i)
		tokenlist = i.strip().split(" ")
		str_list = [x for x in tokenlist if x != '']
		
		#print i
		for word in str_list:
			get_uni(word)
			#print word
	#print unigrams_dict	
	
	ranked_list = sort_list(bigrams_dict) 
	dict_plot=find_x_y_for_plotting(ranked_list, bigrams_dict)
	plot(dict_plot.keys()[:250],dict_plot.values()[:250]) 
    				
    	
