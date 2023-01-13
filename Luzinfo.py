infohead='='*20
infoname='Luz'
def printLuzinfo(info,date):
	infobody=infohead+infoname+infohead
	print(infobody)
	infobodylen=len(infobody)
	infolen=len(info)
	infotaillen1=int((infobodylen-infolen)/2)
	infotaillen2=infobodylen-infolen-infotaillen1
	infotail=infotaillen1*'='+info+infotaillen2*'='
	print(infotail)	
	infolen=len(date)
	infotaillen1=int((infobodylen-infolen)/2)
	infotaillen2=infobodylen-infolen-infotaillen1
	infotail=infotaillen1*'='+date+infotaillen2*'='
	print(infotail)	