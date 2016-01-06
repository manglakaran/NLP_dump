f1 = open("HINDI.test")
f2 = open("final_output_HINDI")
t1 = f1.readlines()
t2 = f2.readlines()
average_accuracy = 0
total_count = len(t1)
for i in xrange(len(t1)):
    line1 = t1[i].split(" ")
    tmp1 = map(lambda x : x.split("_")[0], line1)
    line2 = t2[i].split(" ")
    tmp2 = map(lambda x : x.split("_")[0], line2)
    accuracy = 0
    count = len(line1)
    for j in xrange(len(line1)):
        if line1[j] == line2[j]:
            accuracy += 1
    average_accuracy += accuracy * 100 / count
print average_accuracy / total_count
