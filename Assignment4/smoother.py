import os
import sys
import cPickle as pickle
import string

def main():
  cwd=os.getcwd()
  pickles_dir=cwd+"/Pickles/"+sys.argv[1]
  out_dir=cwd+"/Smoothed/"+sys.argv[1]

  if not os.path.exists(out_dir):
    os.makedirs(out_dir)

  os.chdir(pickles_dir)

  print "Unpickling dictionaries"

  dict_tags=pickle.load(open("dict_tags.p","rb"))
  dict_unigrams=pickle.load(open("dict_unigrams.p","rb"))
  dict_trans=pickle.load(open("dict_trans.p","rb"))


  list_tags=dict_tags.keys()
  print len(list_tags)

  #Handling Unknown words
  os.chdir(cwd)
  test_file=open(sys.argv[1] + ".test","r")
  temp_file=open(sys.argv[1] + ".new", "w")
  count = 0
  for line in test_file.readlines():
    templine = line.split(" ")
    templine = map(lambda x:x.split("_")[0], templine)
    templine = " ".join(templine)
    temp_file.write(templine)
    temp_file.write('\n')
    count += 1
  test_file.close()
  temp_file.close()

  test_file=open(sys.argv[1]+".new","r")
  test_lines=[j.strip() for j in test_file.readlines() if len(j.strip())>0]
  test_file.close()

  for i in test_lines:
    sentence=i.split()
    for j in sentence:
      if j not in dict_unigrams:
        if j.isdigit()==True:
          dict_unigrams[j]=[1.0,dict(zip(list_tags,[0.0]*len(list_tags)))]
          dict_unigrams[j][1]['QC']+=1.0
        elif j in set(string.punctuation):
          dict_unigrams[j]=[1.0,dict(zip(list_tags,[0.0]*len(list_tags)))]
          dict_unigrams[j][1]['SYM']+=1.0

        else :
          dict_unigrams[j]=dict_unigrams['UNSEEN']

  #Creating Emission Matrix
  lambda_value_emission=float(sys.argv[2])

  total_tokens=sum(dict_unigrams[j][0] for j in dict_unigrams)
  print "Total number of tokens\t",total_tokens

  emission_matrix={}

  print "Creating Emission Matrix"
  for i in dict_unigrams:
    if i.isdigit()==True:
      emission_matrix[i]=[dict_unigrams[i][0],dict(zip(list_tags,[0.0]*len(list_tags)))]
      emission_matrix[i][1]['QC']=1.0
    elif i in set(string.punctuation):
      emission_matrix[i]=[dict_unigrams[i][0],dict(zip(list_tags,[0.0]*len(list_tags)))]
      emission_matrix[i][1]['SYM']=1.0
    else :
      emission_matrix[i]=[dict_unigrams[i][0],dict(zip(list_tags,[0.0]*len(list_tags)))]
      for j in dict_unigrams[i][1]:
        emission_matrix[i][1][j]=dict_unigrams[i][1][j]+lambda_value_emission
        emission_matrix[i][1][j]/=(dict_unigrams[i][0] + lambda_value_emission*len(dict_tags))

  #Creating Transition Matrix
  print "Creating Transition matrix"

  lambda_value_transition=float(sys.argv[3])
  trans={}

  for i in list_tags:
    trans[i]=dict(zip(list_tags,[0.0]*len(list_tags)))
    for j in list_tags:
      trans[i][j]=dict_trans[i][1][j]+lambda_value_transition
      try:
        trans[i][j]/=(dict_tags[i] + lambda_value_transition*len(dict_tags))
      except:
        trans[i][j]=0.0

  os.chdir(out_dir)
  print "Pickling smoothed transition matrix"
  pickle.dump(trans,open("trans.p","wb"))

  print "Pickling smoothed emission matrix"
  pickle.dump(emission_matrix,open("emit.p","wb"))

  print "Pickling dict tags"
  pickle.dump(dict_tags,open("dict_tags.p","wb"))

if __name__=="__main__":
  main()
