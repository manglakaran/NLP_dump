import os
import sys
import cPickle as pickle

def create_unigrams_dict(list_sentences,list_tags,dict_unigrams,dict_tags):
  for i in list_sentences:
    for j in xrange(len(i[0])):
      unigram=i[0][j]
      tag=i[1][j]

      dict_tags[tag]+=1.0

      if unigram in dict_unigrams:
        dict_unigrams[unigram][0]+=1.0
        dict_unigrams[unigram][1][tag]+=1.0
      else :
        temp_dict=dict(zip(list_tags,[0.0]*len(list_tags)))
        dict_unigrams[unigram]=[1.0,temp_dict]
        dict_unigrams[unigram][1][tag]=1.0

  return dict_unigrams,dict_tags

def create_transition_dict(list_sentences,list_tags,trans):
  for i in list_sentences:
    for j in xrange(1,len(i[1])):
      prior_tag=i[1][j-1]
      current_tag=i[1][j]
      trans[prior_tag][0]+=1.0
      trans[prior_tag][1][current_tag]+=1.0

  return trans

def create_tagset(sentences):
    all_tags = {}
    for i in sentences:
        for tag in i[1]:
            if all_tags.has_key(tag):
                all_tags[tag] += 1
            else:
                all_tags[tag] = 1

    tags_file = open("TagSet.txt", "w")
    for tag in all_tags.keys():
        tags_file.write(tag)
        tags_file.write('\n')

def main():
  cwd=os.getcwd()
  pickles_dir=cwd+"/Pickles/"+sys.argv[1]

  if not os.path.exists(pickles_dir):
    os.makedirs(pickles_dir)


  in_file=open(sys.argv[1]+".train","r")
  unprocessed_list_sentences=[map(list,zip(*[word.split("_") for word in a.split()])) for a in in_file.readlines()]
  in_file.close()

  print "Number of train sentences\t",len(unprocessed_list_sentences)

  #Removing Spurious Cases
  list_sentences=[]
  spurious_cases=[]
  for i in unprocessed_list_sentences:
    if len(i)==2:
      temp1=['START']+i[0]
      temp2=['START']+i[1]
      augmented=[temp1,temp2]
      list_sentences.append(augmented)
    else:
      spurious_cases.append(i)

  print "Number of spurious cases\t",len(spurious_cases)
  print "Length of viable training data\t",len(list_sentences)

  try:
    tags_file=open("TagSet.txt","r")
  except IOError:
    print "Tagset.txt not found. Creating from training data..."
    # If the file is not already created
    # create it from the training data
    create_tagset(list_sentences)
    tags_file=open("TagSet.txt","r")

  tag_set_provided=[j.strip() for j in tags_file.readlines() if len(j.strip())>0]
  tags_file.close()
  print "Tagset provided:", tag_set_provided

  tag_set_used=['START']+tag_set_provided

  #Printing tags appearing in tags but not in tag set provided
  print
  print "Tags appearing in training data but not in tag set provided:",
  spurious_tags=[]
  tag_appearing=[j for i in list_sentences for j in i[1]]
  for i in tag_appearing:
    if i not in tag_set_used:
      spurious_tags.append(i)
  spurious_tags=list(set(spurious_tags))
  if len(spurious_tags)>0:
    print spurious_tags
  else:
    print "NONE"
  print

  tag_set=tag_set_used+spurious_tags
  print "Length of Tagset:", len(tag_set)


  #Creating Emission Dict
  dict_unigrams={}
  dict_tags=dict(zip(tag_set,[0.0]*len(tag_set)))
  dict_unigrams,dict_tags=create_unigrams_dict(list_sentences,tag_set,dict_unigrams,dict_tags)

  #Single occurring words
  dict_unigrams['UNSEEN']=[0.0,dict(zip(tag_set,[0.0]*len(tag_set)))]
  for i in dict_unigrams:
    if dict_unigrams[i][0]==1.0:
      dict_unigrams['UNSEEN'][0]+=1.0
      for j in tag_set:
        if dict_unigrams[i][1][j]==1.0:
          dict_unigrams['UNSEEN'][1][j]+=1.0
          break

  print "For unseen words taking words of frequency 1"
  print dict_unigrams['UNSEEN']


  #Creating Transition dict
  dict_transition_counts={}
  for i in tag_set:
    dict_transition_counts[i]=[0.0,dict(zip(tag_set,[0.0]*len(tag_set)))]

  dict_transition_counts=create_transition_dict(list_sentences,tag_set,dict_transition_counts)

  os.chdir(pickles_dir)

  print "Pickling dict tags"
  pickle.dump(dict_tags,open("dict_tags.p","wb"))

  print "Pickling dict unigrams"
  pickle.dump(dict_unigrams,open("dict_unigrams.p","wb"))

  print "Pickling dict transition"
  pickle.dump(dict_transition_counts,open("dict_trans.p","wb"))


if __name__=="__main__":
  main()
