#coding: utf8
import requests
import bs4
import csv
import os
from multiprocessing import Pool


rootUrl        = 'http://bulbapedia.bulbagarden.net' 
indexUrl       = rootUrl + '/wiki/List_of_Pokémon_by_National_Pokédex_number'
allPokemonData = [] #array which will have all the data after running allPokemonStats()
currentPath    = os.getcwd() #current write directory
csv_file       = currentPath + "/csv/Pokemon.csv" #where the csv will be written

#column titles in db/csv of data - uncomment this line and one more line in WriteToCSV function if you want the csv columns to appear as values in db
csv_columns    = [ 'id', 'name', 'type', 'abilities', 'hp', 'attack', 'defense', 'sp_atk', 'sp_def', 'speed', 'BST', 'weight', 'height']

#get urls of all the pokemon in the list of pokemon 
def getPokemonUrls(): 
	listOfUrls = requests.get( indexUrl )
	soup       = bs4.BeautifulSoup( listOfUrls.text, "html.parser" )
	return [a.attrs.get( 'href' ) for a in soup.select( 'table[align="center"] td a[title*="Pok"]' ) ]

#for each url, get the data of a pokemon
def getPokemonData( inputUrl ):   
	
	pokemonData = [0]*13 #start with 13 0s. Better than using append method each time to add new value
	htmlData    = requests.get( rootUrl + inputUrl )
	soup        = bs4.BeautifulSoup( htmlData.text, "html.parser" )


	#get national pokedex id of pokemon
	pokemonData[ 0 ] = (int) ((soup.select( 'th big a[href*="mon_by_National_Pok"] span' )[ 0 ].get_text()).replace( '#', ''))


	#get name of pokemon
	pokemonData[ 1 ] = (soup.select( 'h1#firstHeading')[ 0 ].get_text())[ :-10 ]
	

	#get abilities of pokemon (including hidden abilities)
	pokemonData[ 3 ] = soup.select( 'td a[href*=(Ability)] span' )[ 0 ].get_text()
	
	if soup.select( 'td a[href*=(Ability)] span' )[ 1 ].get_text() != 'Cacophony':
		pokemonData[ 3 ] +='/' + soup.select( 'td a[href*=(Ability)] span' )[ 1 ].get_text()
		if soup.select( 'td a[href*=(Ability)] span' )[ 4 ].get_text() != 'Cacophony':
			pokemonData[ 3 ] += '/' + soup.select( 'td a[href*=(Ability)] span' )[ 4 ].get_text()
	elif soup.select( 'td a[href*=(Ability)] span' )[ 3 ].get_text() != 'Cacophony':	
		pokemonData[ 3 ] += '/' + soup.select( 'td a[href*=(Ability)] span' )[ 3 ].get_text()
	

	#get types of pokemon
	pokemonData[ 2 ] = soup.select( 'td a[href*="(type)"] span b' )[ 0 ].get_text() 
	
	if soup.select( 'a[href*="(type)"] span b' )[ 1 ].get_text() != 'Unknown':
	 	pokemonData[ 2 ] += '/' + soup.select( 'td[width="45px"] a[href*="(type)"] span b' )[ 1 ].get_text()


	#get base stats of pokemon
	#no for loop because easier to put in db + can't index items with variable with bs4
	pokemonData[ 4 ]  = (int) (soup.select( 'td table[cellspacing="0"] tr th' )[ 1 ].get_text())
	pokemonData[ 5 ]  = (int) (soup.select( 'td table[cellspacing="0"] tr th' )[ 3 ].get_text())
	pokemonData[ 6 ]  = (int) (soup.select( 'td table[cellspacing="0"] tr th' )[ 5 ].get_text())
	pokemonData[ 7 ]  = (int) (soup.select( 'td table[cellspacing="0"] tr th' )[ 7 ].get_text())
	pokemonData[ 8 ]  = (int) (soup.select( 'td table[cellspacing="0"] tr th' )[ 9 ].get_text())
	pokemonData[ 9 ]  = (int) (soup.select( 'td table[cellspacing="0"] tr th' )[ 11 ].get_text())
	pokemonData[ 10 ] = (int) (soup.select( 'td table[cellspacing="0"] tr th' )[ 13 ].get_text())
	

	#get weight of pokemon in kg
	weightTd          = soup.select( 'table.roundy tr td.roundy b a[href*="weight"]' )[ 0 ].parent.parent
	pokemonData[ 11 ] = (float) ((weightTd.select( 'table tr td' )[ 1 ].get_text())[ :-4 ])


	#get height of pokemon in m
	heightTd          = soup.select( 'table.roundy tr td.roundy b a[href*="height"]' )[ 0 ].parent.parent
	pokemonData[ 12 ] = (float) ((heightTd.select( 'table tr td' )[ 1 ].get_text())[ :-3 ])

	#add to the list of pokemon data already formed
	allPokemonData.append( pokemonData )
	print (allPokemonData)

#get stats by going through every url and getting the info
def allPokemonStats():
	pokemonUrls = getPokemonUrls()
	counter = 0
	percentage = 0
	for pokemonUrl in pokemonUrls: 
		getPokemonData( pokemonUrl )
		counter+=1
		percentage = (counter/721)*100
		print ("Percent complete is: %d" % percentage)

	print ("HEY IS ANYONE THERE, I\'M DONE GOING THROUGH ALL THESE POKEMON!")

errno=0
strerror=0
#pretty self explanatory
def WriteListToCSV( csv_file,csv_columns,data_list ):
#    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(csv_columns) #include if you want to have the csv column names too
            for data in data_list:
                writer.writerow(data)
    #print error
#    except (errno, strerror) as IOError:
#             print("I/O error({0}): {1}".format(errno, strerror))    
#    return              



#Use allPokemonStats() instead of these 5 lines to write CSV of all pokemon
#getPokemonData( '/wiki/Bulbasaur_(Pokémon)' )
#getPokemonData( '/wiki/Ivysaur_(Pokémon)' )
# getPokemonData( '/wiki/Venusaur_(Pokémon)' )
# getPokemonData( '/wiki/Charmander_(Pokémon)' )
# getPokemonData( '/wiki/Dragonite_(Pokémon)' )
allPokemonStats()
WriteListToCSV( csv_file, csv_columns, allPokemonData )
