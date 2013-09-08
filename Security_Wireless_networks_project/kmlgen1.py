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
	count_WPA2 = 0
	count_OPENOTHERS = 0
	count_tigernet=0
	count_clemsonguest=0
	for d in dict2:
		#print dict2[d]	
		x = dict2[d][5]
		y = dict2[d][6]
		if 'WEP' in dict2[d][2]:
			pnt=kml.newpoint(description = dict2[d][0]+dict2[d][2],coords = [(y,x)])
			pnt.iconstyle.color = 'FF0000FF'  # Red"""
			count_WEP = count_WEP + 1
		elif 'WPA' in dict2[d][2] and 'WPA2' not in dict2[d][2]:
			count_WPA = count_WPA + 1
			pnt1=kml.newpoint(description = dict2[d][0]+dict2[d][2],coords = [(y,x)])
			pnt1.iconstyle.color = '#FF00FF00' #Green
			if("tigernet" in (dict2[d][0])):
				count_tigernet=count_tigernet+1		
		elif 'WPA2' in dict2[d][2]:
			count_WPA2=count_WPA2 + 1
			pnt1=kml.newpoint(description = dict2[d][0]+dict2[d][2],coords = [(y,x)])
			pnt1.iconstyle.color = '#FF00FF00' #Green		
		else:
			count_OPENOTHERS = count_OPENOTHERS + 1
			pnt2=kml.newpoint(description = dict2[d][0]+dict2[d][2],coords = [(y,x)])
			pnt2.iconstyle.color = '#FF00FFFF' #Purple
			if("clemsonguest" in (dict2[d][0])):
				count_clemsonguest=count_clemsonguest+1

	kml.save("FINAL_KML_all1.kml")
	final_count = count_WEP +count_WPA + count_OPENOTHERS
	print "  VVVVVVVVVV  The finalcounters !   VVVVVVVVV  "
	print "Total number of distinct wireless networks scanned ---> %i" %final_count
	print "Total number of WEP networks found ----->  %i " %count_WEP
	print "Total number of WPA networks found -----> %i " %count_WPA
	print "Total number of WPA/WPA2 networks found -----> %i " %count_WPA2
	print "Total number of WPA networks found without tigernet -----> %i " %(count_WPA-count_tigernet)
	print "Other networks either Open or others  -----> %i" %count_OPENOTHERS
	print "Other networks either Open or others  without clemsonguest -----> %i" %(count_OPENOTHERS-count_clemsonguest)

if __name__ =="__main__":
    main()
