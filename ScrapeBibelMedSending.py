import bs4 as bs
import urllib.request as r
import os
from random import randint

from pushbullet import Pushbullet

key = 'skriv pushbullet kode her'
#pb = Pushbullet(key)




def skrivBibelen ():

	url = "https://www.bibel.no/Nettbibelen"
	page = r.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	result = r.urlopen(page).read()
	soup = bs.BeautifulSoup(result, "lxml")

	teller = 0
	body = soup.body
	boolBok = False
	bok = ""

	for p in body.find_all("a"):
		#if (p.text == "1 Mos"):
		
		if (p.text == "Neh"):
			boolBok = True

		if (boolBok):
			teller += 1
			if (teller % 2 == 0):

				bok = "https://www.bibel.no" + p.get("href")
				print(p.text)
				
				try:
					os.makedirs("C:/Users/toft/Documents/BibelScraping/" + p.text)
				except:
					pass

				urlBok = bok
				pageBok = r.Request(urlBok, headers={'User-Agent': 'Mozilla/5.0'})
				resultBok = r.urlopen(pageBok).read()
				soupBok = bs.BeautifulSoup(resultBok, "lxml")
				soupBokBody = soupBok.body

				for kappittelUrl in soupBok.find_all(class_="versechapter"):
						print(kappittelUrl.text)
						
						f = open("C:/Users/toft/Documents/BibelScraping/" + p.text + "/"+  kappittelUrl.text+".txt", "w")

						urlKap = "https://www.bibel.no" + kappittelUrl.get("href")
						
						pageKap = r.Request(urlKap, headers={'User-Agent': 'Mozilla/5.0'})
						resultKap = r.urlopen(pageKap).read()
						soupKap = bs.BeautifulSoup(resultKap, "lxml")
						soupKapBody = soupKap.find_all('table')[3] 

						for vers in soupKapBody.find_all("span", class_="verse"):
							if(vers.find_all(class_="verseref") == [] and vers.find_all("b") == []):

								versText = vers.text
								versListe = versText.split("\xa0")

								for vers2 in versListe:
									if (vers2 != ""):
										try:
											f.write(vers2)
										except:
											for bokstav in vers2:
												try:
													f.write(bokstav)
												except:
													print(bokstav)
											
								f.write("\n")
						f.close()		

		if (p.text == "Malaki"):
			boolBok = False


#skrivBibelen()

def fiksMellomrommOgSont():
	directory = os.fsencode("C:/Users/toft/Documents/BibelScraping/")

	for mappa in os.listdir(directory):
	    mappeNavn = os.fsdecode(mappa)
	    print(mappeNavn)
	    directory2 = os.fsdecode("C:/Users/toft/Documents/BibelScraping/" +mappeNavn)
	    for fil in os.listdir(directory2):
	    	filNavn = os.fsdecode(fil)
	    	print(filNavn)
	    	f = open("C:/Users/toft/Documents/BibelScraping/" +mappeNavn+ "/" + filNavn, "r")

	    	s = ""

	    	for linge in f.readlines():
	    		#print (linge)
	    		if (linge != "\n"):
	    			
	    			listeMedOrd = linge.split(" ")
	    			#print(listeMedOrd)
	    			nyteller = 0
	    			for Ord in listeMedOrd:
	    				nyteller+=1
	    				if (Ord != ""):
	    					s+=Ord
	    					#print(len(listeMedOrd))
	    					#print(nyteller)
	    					#print(nyteller < len(listeMedOrd))
	    					if(nyteller < len(listeMedOrd)):
	    						s+=" "
	    						#print("hei")
	    			#s+=linge

	    	f.close()

	    	g = open("C:/Users/toft/Documents/BibelScraping/" +mappeNavn+ "/" + filNavn, "w")
	    	g.write(s)
	    	g.close()


	    	liste = [",", "!", ".", ":"]

	    	for tegn in liste:
	    		f = open("C:/Users/toft/Documents/BibelScraping/" +mappeNavn+ "/" + filNavn, "r")

		    	nyttKappittel = ""

		    	for linge in f.readlines():
		    		listeMedSetninger = linge.split(tegn)
		    		#print(listeMedSetninger)
		    		nyttKappittel += listeMedSetninger[0]
		    		for i in range(1, len(listeMedSetninger)):
		    			if (listeMedSetninger[i][0] == " "):
		    				nyttKappittel += tegn + listeMedSetninger[i]
		    			else:
		    				nyttKappittel += tegn + " " + listeMedSetninger[i]
		    			
		    	f.close()
		    	g = open("C:/Users/toft/Documents/BibelScraping/" +mappeNavn+ "/" + filNavn, "w")
		    	g.write(nyttKappittel)
		    	g.close()

	    	#break
	    #break


def finnRndMedTilfeldigBok():

	s = ""

	directory = os.fsencode("C:/Users/toft/Documents/BibelScraping/")
	tall = randint(0,len(os.listdir(directory))-1)
	#print(tall)

	mappeListe = os.listdir(directory)
	rndMappe = mappeListe[tall]
	#print(os.fsdecode(rndMappe))
	mappeNavn = os.fsdecode(rndMappe)
	s+=mappeNavn

	directory2 = os.fsencode("C:/Users/toft/Documents/BibelScraping/" +"/"+ mappeNavn)
	filListe = os.listdir(directory2)

	rndFilTall = randint(0, len(filListe)-1)
	#print(rndFilTall)
	rndFil = filListe[rndFilTall]
	#print(os.fsdecode(rndFil))
	filNavn = os.fsdecode(rndFil)
	til = len(filNavn) -4

	s += ", kappittel " + filNavn[0:til]

	f = open("C:/Users/toft/Documents/BibelScraping/" +"/"+ mappeNavn+ "/" + filNavn)
	versListe = f.readlines()
	rndVersTall = randint(0, len(versListe)-1)
	s+= ", vers " + str(rndVersTall +1)

	vers = versListe[rndVersTall]
	s+= "\n" + vers
	#print(vers)
	#print(s)
	f.close()

	return(s)

def sendSMS(s):
	#print(s)
	#print(pb.devices)
	lg = pb.devices[1]
	#push = pb.push_note("heisann", s)
	push = pb.push_sms(lg, 97661727, s)

#sendSMS("hei")

def main ():
	#pass
	#skrivBibelen()
	#fiksMellomrommOgSont()
	#for i in range (0,3):
	#	s = finnRndMedTilfeldigBok()
	#	print(s)
	#	sendSMS(s)
	pass


main()