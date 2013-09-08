import android
import time
import datetime
droid = android.Android()
f = open('out.txt','a+')
flag = droid.checkWifiState()
scan_flag='y'
if(flag.result):
	while(True):
		flag1 = droid.wifiStartScan()
		lists=droid.wifiGetScanResults()
		droid.startLocating()
		time.sleep(25)
		loc = droid.readLocation()
		droid.stopLocating()
		lat = str(loc[1]['gps']['latitude'])
		long = str(loc[1]['gps']['longitude'])
		timenow = str(datetime.datetime.now())
		i=0
		scan_dict={}
		scan_ind_list=[]
		res = lists[1]

		for x in res:
			scan_ind_list=[]
			scan_ind_list.append(x['ssid'])
			scan_ind_list.append(x['bssid'])
			scan_ind_list.append(x['capabilities'])
			scan_ind_list.append(x['frequency'])
			scan_ind_list.append(x['level'])
			scan_ind_list.append(lat)
			scan_ind_list.append(long)
			scan_ind_list.append(timenow)
			print >>f,x['ssid'],";",x['bssid'],";",x['capabilities'],";",x['frequency'],";",x['level'],";",lat,";",long,";",timenow;
			scan_dict[x['bssid']]=(scan_ind_list)
			#print scan_ind_list
			"""print "Name:%s"%(x['ssid'])
			print "MAC:%s"%(x['bssid'])
			print "Encryption:%s"%(x['capabilities'])
			print "Frequency:%s"%(x['frequency'])
			print "Signal%s"%(x['level'])
			print ''	"""


		for i in scan_dict:
			print scan_dict[i]
			print ""
		#scan_flag=raw_input("Do u want to scan?(y/n)")	
		i=1
		if(scan_flag=='n'):
			f.close();
else:
	print "Wifi is switched off"
