import simplekml
def main():
	file1 = open("final.txt",'r')
	kml = simplekml.Kml()
	dict1 = {}
	finallist = []
	for line in file1:
		l = []
		l = line.split(";",8)
		#dict1[l[1]] = l
		#print "hi"
		finallist.append(l)		
	dict2 = {}
	count = 1
	for i in range(0,len(finallist)):
		mac = finallist[i][1]
		count = count + 1
		if mac not in dict2:
			dict2[mac] =finallist[i]
		else:
			if (finallist[i][4] < dict2[mac][4]):
				dict2[mac] =finallist[i]

	count_WEP = 0
	count_WPA = 0
	count_OPENOTHERS = 0
	count_tigernet=0
	count_clemsonguest=0
	ch1=0;
	ch2=0;
	ch3=0;
	ch4=0;
	ch5=0;
	ch6=0;
	ch7=0;
	ch8=0;
	ch9=0;
	ch10=0;
	ch11=0;
	ch12=0;
	for d in dict2:
		#print dict2[d]	
		x = dict2[d][5]
		y = dict2[d][6]
		z = dict2[d][3]
		#print x,y
		if '2412' in z:
			ch1=ch1+1
		elif '2417' in z:
			ch2=ch2+1
		elif '2422' in z:
			ch3=ch3+1
		elif '2427' in z:
			ch4=ch4+1
		elif '2432' in z:
			ch5=ch5+1
		elif '2437' in z:
			ch6=ch6+1
		elif '2442' in z:
			ch7=ch7+1
		elif '2447' in z:
			ch8=ch8+1
		elif '2452' in z:
			ch9=ch9+1
		elif '2457' in z:
			ch10=ch10+1
		else:
			ch11=ch11+1
	print "Channel 1 -- %i" %(ch1)
	print "Channel 2 -- %i" %ch2
	print "Channel 3 -- %i" %ch3
	print "Channel 4 -- %i" %ch4
	print "Channel 5 -- %i" %ch5
	print "Channel 6 -- %i" %ch6
	print "Channel 7 -- %i" %ch7
	print "Channel 8 -- %i" %ch8
	print "Channel 9 -- %i" %ch9
	print "Channel 10 -- %i"%ch10
	print "Channel 11 -- %i"%ch11

if __name__ =="__main__":
    main()
