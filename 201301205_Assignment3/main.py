from get_tokens import add_uni,add_bi,add_tri
from english_unigrams import unigram_len,unigram_dict
from english_bigrams import bigram_len,bigram_dict
from english_trigrams import trigram_len,trigram_dict



def laplace_smoothing():
	op = open('English.txt','r')
	#print tokendictionary_tri
	for line in op.readlines():
		prob = 1
		[new_token, tokendictionary1] = add_tri(line)
		#print new_token ,'\n'
		for tokens_tri in new_token:
			token_parts = tokens_tri.split(' ')
			eq_bi = token_parts[0] + ' ' + token_parts[1]
			try:
				prob = prob * float((trigram_dict[tokens_tri])/(float(bigram_dict[eq_bi]) + float(unigram_len)))
			except KeyError:
				try:
					prob = prob * float((1)/(float(bigram_dict[eq_bi]) + float(unigram_len)))
				except KeyError:
					prob = prob * float((1)/float(unigram_len))
		print prob	

def laplace_interpolation():
	op = open('English.txt','r')
	#print tokendictionary_tri
	for line in op.readlines():
		prob = 1
		prob_add = 0
		[new_token, tokendictionary1] = add_tri(line)
		#print new_token ,'\n'
		for tokens_tri in new_token:
			token_parts = tokens_tri.split(' ')
			eq_bi = token_parts[0] + ' ' + token_parts[1]
			try:
				prob = prob * float((trigram_dict[tokens_tri])/(float(bigram_dict[eq_bi]) + float(unigram_len)))
			except KeyError:
				try:
					prob = prob * float((1)/(float(bigram_dict[eq_bi]) + float(unigram_len)))
				except KeyError:
					prob = prob * float((1)/float(unigram_len))
		#print prob
		prob_add += 0.5*prob
		prob =1
		[new_token, tokendictionary1] = add_bi(line)
		#print new_token ,'\n'
		#break
		for tokens_bi in new_token:
			token_parts = tokens_bi.split(' ')
			eq_uni = token_parts[0] 
			try:
				prob = prob * float((bigram_dict[tokens_bi])/(float(unigram_dict[eq_uni]) + float(unigram_len)))
			except KeyError:
				try:
					prob = prob * float((1)/(float(unigram_dict[eq_uni]) + float(unigram_len)))
				except KeyError:
					prob = prob * float((1)/float(unigram_len))
		#print prob
		prob_add += 0.3*prob
		prob =1
		[new_token, tokendictionary1] = add_uni(line)
		#print new_token ,'\n'
		#break
		for tokens_uni in new_token:
			#token_parts = tokens_bi.split(' ')
			#eq_uni = token_parts[0] 
			try:
				prob = prob * float((unigram_dict[tokens_uni])/(2*float(unigram_len)))
			except KeyError:
				prob = prob * float((1)/(2*float(unigram_len)))

		prob_add += 0.2*prob
		prob =1
		print prob_add

def calculate_good_next(bins_tri, tokens_tri, tokens_length, tokendictionary_req):
	
	try:
		count = tokendictionary_req[tokens_tri]
		if count == max(bins_tri.iterkeys()):
			return float(float(count)/float(tokens_length))
		else:
			count1 = count +1
			flag = 0
			while(flag == 0):
				if count1 in bins_tri:
					flag = 1
				else:
					count1 = count1 + 1
			return float(((count+1)*float(float(bins_tri[count1])/float(bins_tri[count])))/float(tokens_length))
	except KeyError:
		return float(float(bins_tri[1])/(tokens_length))

def good_turing_smoothing():
	bins_tri = {}
	for key, value in sorted(trigram_dict.iteritems()):
		if value in bins_tri : 
			bins_tri[value] += 1
		else:
			bins_tri[value] = 1
	#print bins_tri
	op = open('English.txt','r')
	for line in op.readlines():
		prob = 1
		[new_token, tokendictionary1] = add_tri(line)
		for tokens_tri in new_token:
			prob = prob * float(calculate_good_next(bins_tri, tokens_tri, trigram_len, trigram_dict))
		print prob

def good_turing_interpolation():
	bins_tri = {}
	bins_bi = {}
	bins_uni = {}
	for key, value in sorted(trigram_dict.iteritems()):
		if value in bins_tri : 
			bins_tri[value] += 1
		else:
			bins_tri[value] = 1
	#print bins_tri
	for key, value in sorted(bigram_dict.iteritems()):
		if value in bins_bi : 
			bins_bi[value] += 1
		else:
			bins_bi[value] = 1
	
	for key, value in sorted(unigram_dict.iteritems()):
		if value in bins_uni : 
			bins_uni[value] += 1
		else:
			bins_uni[value] = 1

	op = open('English.txt','r')
	for line in op.readlines():
		prob = 1
		prob_add = 0
		[new_token, tokendictionary1] = add_tri(line)
		for tokens_tri in new_token:
			prob = prob * float(calculate_good_next(bins_tri, tokens_tri, trigram_len, trigram_dict))
		#print prob
		prob_add = 0.5*prob
		prob = 1 
		[new_token, tokendictionary1] = add_bi(line)
		for tokens_bi in new_token:
			prob = prob * float(calculate_good_next(bins_bi, tokens_bi, bigram_len, bigram_dict))
		#print prob
		prob_add += 0.3*prob
		prob = 1 
		[new_token, tokendictionary1] = add_uni(line)
		for tokens_uni in new_token:
			prob = prob * float(calculate_good_next(bins_uni, tokens_uni, unigram_len, unigram_dict))
		prob_add += 0.2*prob
		print prob_add

if __name__ == '__main__':
	print "LAPLACE SMOOTHING"
	laplace_smoothing()
	print "LAPLACE INTERPOLATION"
	laplace_interpolation()
	print "GOOD TURING SMOOTHING"
	good_turing_smoothing()
	print "GOOD TURING INTERPOLATION"
	good_turing_interpolation()																																											