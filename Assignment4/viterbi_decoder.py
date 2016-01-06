import os
import sys
import cPickle as pickle
import math


def viterbi_decoder(sentence,emit,trans,list_tags):
  V=[{}]
  path={}

  for y in list_tags:
    V[0][y]=trans['START'][y]*emit[sentence[0]][1][y]
    path[y] = [y]

  (prob, state) = max((V[0][y], y) for y in list_tags)

  for t in xrange(1,len(sentence)):
    V.append({})
    newpath = {}

    for y in list_tags:
      (prob,state)=max(( V[t-1][y_prime] * trans[y_prime][y] * emit[sentence[t]][1][y] , y_prime) for y_prime in list_tags)
      V[t][y]=prob
      newpath[y] = path[state] + [y]

    path=newpath

  (prob, state) = max((V[t][y], y) for y in list_tags)
  statement = ""
  total_count = len(sentence)
  output=" ".join(map(lambda x:"_".join(x),zip(sentence,path[state])))
  print output

def main():
  cwd=os.getcwd()
  smoothed_dir=cwd+"/Smoothed/"+sys.argv[1]


  os.chdir(smoothed_dir)

  #Unpickling emission matrix
  emit=pickle.load(open("emit.p","rb"))

  #Unpickling transition matrix
  trans=pickle.load(open("trans.p","rb"))

  #Unpickling dict tags
  dict_tags=pickle.load(open("dict_tags.p","rb"))

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
  file_lines = test_file.readlines()
  testing_lines=[j.strip() for j in file_lines if len(j.strip())>0]
  test_file.close()
  test_output=[]
  #Viterbi Algorithm Code
  for i in testing_lines:
    temp=i.split()
    sentence=temp
    viterbi_decoder(sentence,emit,trans,dict_tags.keys())

if __name__=="__main__":
  main()
