#!/usr/bin/env python

# server.py - a Distant Reader MCP server

# Eric Lease Morgan <eric_morgan@infomotions.com>
# (c) Infomotions, LLC; distributed under a GNU Public License

# April 27, 2026 - first cut
# April 28, 2026 - added unigrams; this is working!
# April 29, 2026 - added sentences and keywords
# May    3, 2026 - added a few more tools and associated prompts; I don't think resources work
# May    7, 2026 - added even more tool; this is really working very well
# May    8, 2026 - added get full path to original items
# May   11, 2026 - cleaned up naming conventions; works the same though
# May   15, 2026 - refined inline to expose interesting, POS, and entity words; limite results to segments of lists
# May   24, 2026 - refined the documentation regarding items; works better
# May   25, 2026 - added getAuthors, getTitles, and getDates
# May   28, 2026 - refined getSentencesWord


# configure
NAME	= 'Distant Reader MCP Server'
LIBRARY = 'localLibrary'
TXT	 = 'txt'

# require
from json			    import loads
from mcp.server.fastmcp import FastMCP
from struct			    import pack
from typing			    import List, Literal
import rdr

# serializes a list of floats into a compact "raw bytes" format; makes things more efficient?
def serialize( vector: List[float]) -> bytes : return pack( "%sf" % len( vector ), *vector )

# initailize
server  = FastMCP( NAME, json_response=True, stateless_http=True )
library = rdr.configuration( LIBRARY )


############## pos: pronouns ##############

@server.tool()
def getPronouns( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of of all the pronouns identified as a part-of-speech value. These are POS words. This process helps identify who and what is included in the text.
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of pronouns from the given carrel
	'''
	carrel     = carrel.replace( '‑', '-' )
	adjectives = rdr.pos(carrel, select='lemma', like='PRON', count=True ).splitlines()
	segment    = len( adjectives ) // 4
	return( str( adjectives[ :segment ] ) )

@server.prompt()
def p_getPronouns( carrel:str ) :
	'''Get all pronouns from the given carrel and extracted from the parts-of-speech process'''
	return( f'''Given the carrel named '{carrel}', return a frequency list of all the pronous.''' )


############## pos: adjectives ##############

@server.tool()
def getAdjectives( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of of all the adjectives identified as a part-of-speech value. These are POS words. This process helps identify how the things in the carrel are described.
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of adjectives from the given carrel
	'''
	carrel     = carrel.replace( '‑', '-' )
	adjectives = rdr.pos(carrel, select='lemma', like='ADJ', count=True ).splitlines()
	segment    = len( adjectives ) // 4
	return( str( adjectives[ :segment ] ) )

@server.prompt()
def p_getAdjectives( carrel:str ) :
	'''Get all adjectives from the given carrel and extracted from the parts-of-speech process'''
	return( f'''Given the carrel named '{carrel}', return a frequency list of all the adjectives.''' )


############## full path to origial document ##############

@server.tool()
def getFullPathToOriginalItem( carrel: str, item:str ) -> str:
	'''
		Given the name of a carrel and an identifier in the carrel, output the full path to the item in its original form
		Args:
			carrel (str): the name of a study carrel
			item (str): an identifier
		Returns: 
			str: the full path to the original item in the given study carrel
	'''
	carrel = carrel.replace( '‑', '-' )
	item   = item.replace( '‑', '-' )
	found  = False 
	for record in loads( rdr.bibliography( carrel, format='json' ) ) :
		if record[ 'id' ] == item :
			fullpath = 'file://' + str( library/carrel/(rdr.CACHE)/( item + record[ 'extension' ] ) )
			found	= True
			break
	
	if found : return( fullpath )
	else	 : return( "That item was not found, are you sure the identifier's value is correct?" )

@server.prompt()
def p_getFullPathToOriginalItem( carrel:str, item: str ) :
	'''The the full path to the original version of the given item in the given carrel'''
	return( f'''Given the carrel named '{carrel}', return the full path to the original version of '{item}'.''' )


############## pos: verbs ##############

@server.tool()
def getVerbs( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of of all the lemmatized verbs identified as a part-of-speech value.  These are POS words. This process helps identify what the things in this carrel do; what actions do they take.
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of lemmatized verbs form the given carrel
	'''
	carrel  = carrel.replace( '‑', '-' )
	verbs   = rdr.pos(carrel, select='lemma', like='VERB', count=True )
	segment = len( verbs ) // 4
	return( str( verbs[ :segment ] ) )

@server.prompt()
def p_getVerbs( carrel:str ) :
	'''Get all lemmatized verbs from the given carrel as extracted from the parts-of-speech process'''
	return( f'''Given the carrel named '{carrel}', return the lemmatized part-of-speech value of VERB.''' )


############## bibliographics: titles ##############

@server.tool()
def getTitles( carrel: str ) -> str:
	'''
		Given the name of a carrel output a list of all the titles of items in the given carrel. This is a bibliographic. This addresses the question, "What are the titles of the items in this carrel?"
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a list of titles and the item identifiers from the given carrel
	'''
	KEYS   = [ 'id', 'title' ]
	carrel = carrel.replace( '‑', '-' )
	titles = []
	for item in loads( rdr.bibliography( carrel, format='json' ) ) : titles.append( { key: item[ key ] for key in KEYS if key in item } )
	return( str( titles ) )

@server.prompt()
def p_getTitles( carrel:str ) :
	'''Get all the titles and the associated item identifiers from the given carrel'''
	return( f'''Given the carrel named '{carrel}', return the titles and the item identifiers pointing to the titles of things written  in given carrel.''' )


############## bibliographics: titles ##############

@server.tool()
def getAbstracts( carrel: str ) -> str:
	'''
		Given the name of a carrel output a list of all items' abstracts as well as their item identifiers. This is a bibliographic. This addresses the question, "What are the items in the carrel about?"
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a list of abstracts and the item identifiers from the given carrel
	'''
	KEYS      = [ 'id', 'summary' ]
	carrel    = carrel.replace( '‑', '-' )
	abstracts = []
	for item in loads( rdr.bibliography( carrel, format='json' ) ) : abstracts.append( { 'abstract': item[ key ] for key in KEYS if key in item } )
	return( str( abstracts ) )

@server.prompt()
def p_getAbstracts( carrel:str ) :
	'''Get all the abstracts and the associated item identifiers from the given carrel'''
	return( f'''Given the carrel named '{carrel}', return the summaries and the item identifiers pointing to the titles of things written  in given carrel.''' )


############## bibliographics: authors ##############

@server.tool()
def getAuthors( carrel: str ) -> str:
	'''
		Given the name of a carrel output a list of all the authors of items in the given carrel. These are creators, and this is a bibliographic. This addresses the question, "Who wrote the items in the given carrel?"
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a list of author names and the item identifiers from the given carrel
	'''
	KEYS    = [ 'id', 'author' ]
	carrel  = carrel.replace( '‑', '-' )
	authors = []
	for item in loads( rdr.bibliography( carrel, format='json' ) ) : authors.append( { key: item[ key ] for key in KEYS if key in item } )
	return( str( authors ) )

@server.prompt()
def p_getAuthors( carrel:str ) :
	'''Get all the authors and the associated item identifiers from the given carrel'''
	return( f'''Given the carrel named '{carrel}', return the authors and the item identifiers pointing to the things they wrote in the carrel.''' )


############## bibliographics: dates ##############

@server.tool()
def getDates( carrel: str ) -> str:
	'''
		Given the name of a carrel output a list of all the dates of items in the given carrel. These are dates, and this is a bibliographic. This addresses the question, "When were the thing in this carrel written?"
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a list of date and the item identifiers from the given carrel
	'''
	KEYS   = [ 'id', 'date' ]
	carrel = carrel.replace( '‑', '-' )
	dates  = []
	for item in loads( rdr.bibliography( carrel, format='json' ) ) : dates.append( { key: item[ key ] for key in KEYS if key in item } )
	return( str( dates ) )

@server.prompt()
def p_getDates( carrel:str ) :
	'''Get all the dates of the items written and the associated item identifiers from the given carrel'''
	return( f'''Given the carrel named '{carrel}', return the dates and the item identifiers pointing to the things in the carrel.''' )


############## pos: nouns ##############

@server.tool()
def getNouns( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of of all the nouns identified as a part-of-speech value. These are POS words. This helps identify what it mentioned in the given carrel.
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of nouns from the given carrel
	'''
	carrel  = carrel.replace( '‑', '-' )
	nouns   = rdr.pos(carrel, select='words', like='NOUN', count=True ).splitlines()
	segment = len( nouns ) // 16
	return( str( nouns[ :segment ] ) )

@server.prompt()
def p_getNouns( carrel:str ) :
	'''Get all nouns from the given carrel and extracted from the parts-of-speech process'''
	return( f'''Given the carrel named '{carrel}', return part-of-speech of type NOUN.''' )


############## named-entitites: people ##############

@server.tool()
def getPeople( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of people identified as a named entity. This helps identify who is mentioned in the carrel. These are ENTITY words.
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of people form the given carrel
	'''
	carrel  = carrel.replace( '‑', '-' )
	people  = rdr.entities (carrel, select='entity', like='PERSON', count=True ).splitlines()
	segment = len( people ) // 8
	return( str( people[ :segment ] ) )

@server.prompt()
def p_getPeople( carrel:str ) :
	'''Get all names of people from the given carrel and extracted from the named entity process'''
	return( f'''Given the carrel named '{carrel}', return named entities of type PERSON.''' )


############## named-entitites: ORG ##############

@server.tool()
def getOrganizations( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of organizations identified as a named entity. This helps identify what groups of people are mentioned in the carrel. These are ENTITY words.
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of organizations form the given carrel
	'''
	carrel        = carrel.replace( '‑', '-' )
	organizations = rdr.entities (carrel, select='entity', like='ORG', count=True ).splitlines()
	segment       = len( organizations ) // 2
	return( str( organizations[ :segment ] ) )

@server.prompt()
def p_getOrganizations( carrel:str ) :
	'''Get all names of organizations from the given carrel and extracted from the named entity process'''
	return( f'''Given the carrel named '{carrel}', return named entities of type ORG.''' )


############## named-entitites: GPE ##############

@server.tool()
def getPlaces( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of places (geo-political entities) identified as a named entity. This helps identify what places are mentioned in the carrel. These are ENTITY words.
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of places form the given carrel
	'''
	carrel  = carrel.replace( '‑', '-' )
	places  = rdr.entities (carrel, select='entity', like='GPE', count=True ).splitlines()
	segment = len( places ) // 2
	return( str( places[ :segment ] ) )

@server.prompt()
def p_getPlaces( carrel:str ) :
	'''Get all names of geo-political entities (places) from the given carrel and extracted from the named entity process'''
	return( f'''Given the carrel named '{carrel}', return named entities of type GPE.''' )


############## item identifiers ##############

@server.tool()
def getItems( carrel: str ) -> str:
	'''
		Given the name of a carrel output a list of all the item identifiers
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a list of all the items's identifiers
	'''
	carrel = carrel.replace( '‑', '-' )
	bibliography = loads( rdr.bibliography( carrel, format='json' ) )
	return( str( [ item[ 'id' ] for item in bibliography ] ) )

@server.prompt()
def p_getItems( carrel:str ) :
	'''Get all item identifiers from a given carrel'''
	return( f'''Given the carrel named '{carrel}', return all item identifiers it contains.''' )


############## plain text ##############

@server.tool()
def getPlaintext( carrel: str, item:str ) -> str:
	'''
		Given the name of a carrel and an item identifier, return the plain text of the item. The result is useful for analysis of the resulting text.
		Args:
			carrel (str): the name of a study carrel
			item (str): an item identifier pointing to an specific item in the carrel
		Returns: 
			str: the plain text of the given item
	'''
	carrel = carrel.replace( '‑', '-' )
	item = item.replace( '‑', '-' )
	with open( library /carrel/TXT/(item + '.txt' ) ) as handle : plaintext = handle.read()
	return( plaintext )

@server.prompt()
def p_getPlaintext( carrel:str, item:str ) :
	'''Retrieve the plain text version of an item from a carrel'''
	return( f'''Given the carrel named '{carrel}' and the identifier '{item}', get the plain text version of the item.''' )


############## words in sentences ##############

@server.tool()
def getSentencesWord( carrel:str, query:str ) -> str :
	"""
		Output all sentences from the given carrel which contains or are semantically simlar to the given word or phrase. The resulting sentences are usefu for further analysis.
		Args:
			carrel (str): The name of a carrel.
			query (str): An individual word or phase
		Returns:
			str: a new-line delimited list of sentences
	"""

	carrel = carrel.replace( '‑', '-' )
	depth = len( rdr.concordance(carrel, localLibrary=None, query=query.lower()) )
	
	DATABASE = 'sentences.db'
	MAXIMUM  = 2048
	COLUMNS  = [ 'item', 'index', 'sentence' ]
	SELECT   = "SELECT title AS 'item', item AS 'index', sentence, VEC_DISTANCE_L2(embedding, ?) AS distance FROM sentences ORDER BY distance LIMIT ?"
	MODEL	= 'locusai/multi-qa-minilm-l6-cos-v1'
	
	from sqlite_vec import load
	from sqlite3	import connect
	from ollama	 import embed
	from pandas	 import DataFrame

	database = connect( rdr.configuration( LIBRARY )/carrel/(rdr.ETC)/DATABASE )
	database.enable_load_extension( True )
	load( database )

	# vectorize query and search; get a set of matching records
	query   = embed( model=MODEL, input=query ).model_dump( mode='json' )[ 'embeddings' ][ 0 ]
	records = database.execute( SELECT, [ serialize( query ), depth ] ).fetchall()

	sentences = []
	for index, record in enumerate( records ) :
	
		# parse
		title	= record[ 0 ]
		item	 = record[ 1 ]
		sentence = record[ 2 ]
		distance = record[ 3 ]
		
		# short-circuit
		if index > MAXIMUM : break
		
		# update
		sentences.append( [ title, item, sentence ] )
	
	# create a dataframe of the sentences and sort by title
	sentences = DataFrame( sentences, columns=COLUMNS )
	return( sentences.to_json( orient='index' ) )
	#return( str( type( depth ) ) )

@server.prompt()
def p_getSentencesWord( carrel:str, query:str ) :
	'''Return the sentences including or semantically similar to the given word or phrase from the given carrel'''
	return( f'''Given the carrel named '{carrel}' list all of the sentences including or are semantically similar to the word or phrase '{query}'.''' )


############## keywords from carrel ##############

@server.tool()
def getKeywords( carrel:str ) -> str :
	"""
		Count and tabulate the keywords associated with the given study carrel. This process addresses the questions, "What sorts of things are discussed in this carrel?" or "What is the carrel about?"
		Args:
			carrel (str): The name of a carrel.
		Returns:
			str: a tab-delimited list of carrel keywords and their associated frequencies
	"""
	carrel = carrel.replace( '‑', '-' )
	return( rdr.keywords( carrel, count=True ) )

@server.prompt()
def p_getKeywords( carrel:str ) :
	"""Count and tabulate the keywords associated with the given study carrel"""
	return f"""Given the carrel named '{carrel}', count and tabulate the keywords."""

############## semantically similar words ##############

@server.tool()
def getSemanticallySimilarWords( carrel:str, word:str, depth:int=16 ) -> str :
	"""
		Given the name of a study carrel and a word, outut the depth number of semantically similar words as well as their associated scores.
		Args:
			carrel (str): The name of a carrel.
			word (str): A word use to find similarity on
			depth (int): The number of words to return
		Returns:
			str: a tab-delimited list of semantically similar words and their associated distance scores
	"""
	carrel = carrel.replace( '‑', '-' )
	return( rdr.word2vec( carrel, type='similarity', query=word, topn=depth ) )

@server.prompt()
def p_getSemanticallySimilarWords( carrel:str, word:str, depth:int ) :
	"""From the given carrel, word, and depth, count and tabulate the semantically simlar words"""
	return f"""Given the carrel named '{carrel}', count and tabulate the semantically simlar to '{word}' and limit the output to '{depth}' words."""


############## ungrams ##############

@server.tool()
def getUnigrams( carrel:str ) -> str :
	"""
		Outputs the counts and tabulations of individual words (unigrams) in the given carrel. This process addresses the question "What sorts of things are discussed in this carrel?"
		Args:
			carrel (str): The name of a carrel.
		Returns:
			str: a list of the carrel's most frequent unigrams
	"""
	carrel   = carrel.replace( '‑', '-' )
	unigrams = rdr.ngrams( carrel, size=1, count=True ).splitlines()
	segment  = len( unigrams ) // 16
	return( str( unigrams[ :segment ] ) )

@server.prompt()
def p_getUnigrams( carrel:str, size:int ) :
	"""Count & tabulate individual words (unigrams) in the given carrel"""
	return f"""Given the carrel named '{carrel}', count and tabulate the most frequent individual words (unigrams)."""


############## bigrams ##############

@server.tool()
def getBigrams( carrel:str ) -> str :
	"""
		Outputs the counts and tabulations of the two-word phrases (bigrams) from the given carrel. This process addresses the question "What sorts of things are discussed in this carrel?"
		Args:
			carrel (str): The name of a carrel.
		Returns:
		str: a list of the carrel's most frequent bigrams
	"""
	carrel  = carrel.replace( '‑', '-' )
	bigrams = rdr.ngrams( carrel, size=2, count=True ).splitlines()
	segment = len( bigrams ) // 32
	return( str( bigrams[ :segment ] ) )

@server.prompt()
def p_getBigrams( carrel:str ) :
	"""Count & tabulate two-word phrases (bigrams) in the given carrel"""
	return f"""Given the carrel named '{carrel}', count and tabulate the most frequent two-word phrases (bigrams)."""


############## catalog ##############

@server.tool()
def getCatalog() -> str :
	"""
		Output the list of study carrels available from the local library.
		Returns:
			str: a list of the carrels accessible from the local library
	"""
	return( rdr.catalog() )

@server.prompt()
def p_getCatalog() :
	"""Get a list of the carrels available in the local library"""
	return( f"""In the form of a paragraph, list the carrels available from the local library.""" )


############## bibliography ##############

@server.tool()
def getBibliography( carrel: str ) -> str:
	"""
		Output the bibliographic metadata elements (author, title, date, summary, keywords, flesch score, and number of words) for the given carrel.
		Args:
			carrel (str): The name of a carrel.
		Returns:
			str: a JSON stream including an identifier, author, title, date, summary, keywords, Flesch (readability) score, and number of words.
	"""
	carrel = carrel.replace( '‑', '-' )
	return( rdr.bibliography( carrel, format='json' ) )

@server.prompt()
def p_getBibliography( carrel:str ) :
	"""Given the name of a carrel, output the bibliographic elements of each item in the carrel"""
	return( f"""Given the carrel named '{carrel}', output the identifier, author, title, date, summary, keywords, Flesch (readability) score, and size measure in words for each item in the carrel.""" )


############## extent of carrel in words ##############

@server.tool()
def getSizeInWords( carrel:str ) -> int:
	"""
		Given the name of a study carrel return the size of the carrel measured in number of words. This is an extent.
		Args:
			carrel (str): The name of a local Distant Reader study carrel.
		Returns:
			int: a number denoting the size of the carrel measured in words
	"""
	carrel = carrel.replace( '‑', '-' )
	return( rdr.extents( carrel, 'words' ) )

@server.prompt()
def p_getSizeInWords( carrel:str ) :
	"""Get the size of the given carrel measured in total number of words"""
	return f"""Return the size of '{carrel}' measured in total number of words."""


############## extent of carrel in items ##############

@server.tool()
def getSizeInItems( carrel:str ) -> int:
	"""
		Given the name of a study carrel return number of items in the carrel. This is an extent.
		Args:
			carrel (str): The name of a local Distant Reader study carrel.
		Returns:
			int: a number denoting the size of the carrel measured in number of items
	"""
	carrel = carrel.replace( '‑', '-' )
	return( rdr.extents( carrel, 'items' ) )

@server.prompt()
def p_getSizeInItems( carrel:str ) :
	"""Get the size (extent) of the given carrel measured in total number of items"""
	return f"""Return the size of '{carrel}' measured in total number of items."""


############## extent of carrel in items ##############

@server.tool()
def getSizeInFlesch( carrel:str ) -> int:
	"""
		Given the name of a study carrel return the overall Flesch Readability score of the carrel. This is an extent.
		Args:
			carrel (str): The name of a local Distant Reader study carrel.
		Returns:
			int: the Flesch Readability Score for the given carrel
	"""
	carrel = carrel.replace( '‑', '-' )
	return( rdr.extents( carrel, 'flesch' ) )

@server.prompt()
def p_getSizeInFlesch( carrel:str ) :
	"""Get the Flesh Readability score of the given carrel."""
	return f"""Return the overall Flesch Readability Score (extent) of '{carrel}'."""


############## extents ##############
#
#@server.tool()
#def getExtents( carrel:str, type:Literal[ "items", "words", "flesch" ] ) -> int:
#	"""
#		Given the name of a study carrel and the type of an extent (items, words, or flesch) return the size of the carrel.
#		Args:
#			carrel (str): The name of a local Distant Reader study carrel.
#			type (str): One of three values: 1) items, 2) words, 3) flesch score
#		Returns:
#			int: a number denoting the quanity of the given type
#	"""
#	return( rdr.extents( carrel, type ) )
#
#@server.prompt()
#def p_getExtents( carrel:str, type:str ) :
#	"""Get extents (size measured in words, flesch (readability), size measured in items)."""
#	return f"""Return the extent '{type}' from the carrel named '{carrel}'."""
#
#
############## resources, but I don't think they work ##############

@server.resource(
		uri = "carrel://{carrel}/index.csv",
		name="CSVMetadata",
		description="If the study carrel was created using a supplemental metadata file, then this is that file",
		mime_type="text/csv"
	)
def get_index_csv( carrel: str ) -> str:
	'''
		Given the name of a carrel output the metadata used to create the carrel in the first place, if it exists.
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a comma-separated values (CSV) stream of metadata
	'''
	with open( Path( LIBRARY )/carrel/( 'index.csv' ) ) as handle : csv = handle.read()
	return( csv )


@server.resource("foobar://readme.txt")
def file_readme() -> str:
	"""Use this resource to get a README file what the Distant Reader and study carrels are."""
	with open ( './etc/readme.txt' ) as handle : data = handle.read()
	return( data )


# go
if __name__ == "__main__" :

	server.run( transport="streamable-http" )
	#server.run( transport="stdio" )

