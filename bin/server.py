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


# configure
NAME    = 'Distant Reader MCP Server'
LIBRARY = 'localLibrary'
TXT     = 'txt'

# require
from json               import loads
from mcp.server.fastmcp import FastMCP
from struct             import pack
from typing             import List
import rdr

# serializes a list of floats into a compact "raw bytes" format; makes things more efficient?
def serialize( vector: List[float]) -> bytes : return pack( "%sf" % len( vector ), *vector )

# initailize
server  = FastMCP( NAME, json_response=True, stateless_http=True )
library = rdr.configuration( LIBRARY )


############## pos: adjectives ##############

@server.tool()
def getCarrelAdjectives( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of of all the adjectives identified as a part-of-speech value. This process helps identify how the things in the carrel are described.
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of adjectives from the given carrel
	'''
	return( str( rdr.pos(carrel, select='lemma', like='ADJ', count=True ) ) )

@server.prompt()
def p_getCarrelAdjectives( carrel:str ) :
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
	found = False 
	for record in loads( rdr.bibliography( carrel, format='json' ) ) :
		if record[ 'id' ] == item :
			fullpath = 'file://' + str( library/carrel/(rdr.CACHE)/( item + record[ 'extension' ] ) )
			found    = True
			break
	
	if found : return( fullpath )
	else     : return( "That item was not found, are you sure the identifier's value is correct?" )

@server.prompt()
def p_getFullPathToOriginalItem( carrel:str, item: str ) :
    '''The the full path to the original version of the given item in the given carrel'''
    return( f'''Given the carrel named '{carrel}', return the full path to the original version of '{item}'.''' )


############## pos: verbs ##############

@server.tool()
def getCarrelVerbs( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of of all the lemmatized verbs identified as a part-of-speech value. This process helps identify what the things in this carrel do; what actions do they take.
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of lemmatized verbs form the given carrel
	'''
	return( str( rdr.pos(carrel, select='lemma', like='VERB', count=True ) ) )

@server.prompt()
def p_getCarrelVerbs( carrel:str ) :
    '''Get all lemmatized verbs from the given carrel as extracted from the parts-of-speech process'''
    return( f'''Given the carrel named '{carrel}', return the lemmatized part-of-speech value of VERB.''' )


############## pos: nouns ##############

@server.tool()
def getCarrelNouns( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of of all the nouns identified as a part-of-speech value. This helps identify what it mentioned in the given carrel.
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of nouns from the given carrel
	'''
	LIMIT = 1024
	#return( str( rdr.ngrams( carrel, size=1, count=True ).splitlines()[ :LIMIT ] ) )
	return( str( rdr.pos(carrel, select='words', like='NOUN', count=True ).splitlines()[ :LIMIT ] ) )

@server.prompt()
def p_getCarrelNouns( carrel:str ) :
    '''Get all nouns from the given carrel and extracted from the parts-of-speech process'''
    return( f'''Given the carrel named '{carrel}', return part-of-speech of type NOUN.''' )


############## named-entitites: people ##############

@server.tool()
def getCarrelPeople( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of of all the people identified as a named entity. This helps identify who is mentioned in teh carrel.
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of people form the given carrel
	'''
	return( str( rdr.entities (carrel, select='entity', like='PERSON', count=True ) ) )

@server.prompt()
def p_getCarrelPeople( carrel:str ) :
    '''Get all names of people from the given carrel and extracted from the named entity process'''
    return( f'''Given the carrel named '{carrel}', return named entities of type PERSON.''' )


############## item identifiers ##############

@server.tool()
def getItemIdentifiers( carrel: str ) -> str:
	'''
		Given the name of a carrel output a list of all the item identifiers
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a list of all the items's identifiers
	'''
	bibliography = loads( rdr.bibliography( carrel, format='json' ) )
	return( str( [ item[ 'id' ] for item in bibliography ] ) )

@server.prompt()
def p_getItemIdentifiers( carrel:str ) :
    '''Get all item identifiers from a given carrel'''
    return( f'''Given the carrel named '{carrel}', return all item identifiers it contains.''' )


############## plain text ##############

@server.tool()
def getPlaintext( carrel: str, identifier:str ) -> str:
	'''
		Given the name of a carrel and an identifier, return the plain text of the item. The result is useful for analysis of the resulting text.
		Args:
			carrel (str): the name of a study carrel
			identifier (str): an identifier pointing to an specific item in the carrel
		Returns: 
			str: the plain text of the given item
	'''
	identifier = identifier.replace( '‑', '-' )
	with open( library /carrel/TXT/(identifier + '.txt' ) ) as handle : plaintext = handle.read()
	return( plaintext )

@server.prompt()
def p_getPlaintext( carrel:str, identifier:str ) :
    '''Retrieve the plain text version of an item from a carrel'''
    return( f'''Given the carrel named '{carrel}' and the identifier '{identifier}', get the plain text version of the item.''' )


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

	DATABASE = 'sentences.db'
	DEPTH    = 1024
	COLUMNS  = [ 'item', 'index', 'sentence' ]
	SELECT   = "SELECT title AS 'item', item AS 'index', sentence, VEC_DISTANCE_L2(embedding, ?) AS distance FROM sentences ORDER BY distance LIMIT ?"
	MODEL    = 'locusai/multi-qa-minilm-l6-cos-v1'
	
	from sqlite_vec import load
	from sqlite3    import connect
	from ollama     import embed
	from pandas     import DataFrame

	database = connect( rdr.configuration( LIBRARY )/carrel/(rdr.ETC)/DATABASE )
	database.enable_load_extension( True )
	load( database )

	# vectorize query and search; get a set of matching records
	query   = embed( model=MODEL, input=query ).model_dump( mode='json' )[ 'embeddings' ][ 0 ]
	records = database.execute( SELECT, [ serialize( query ), DEPTH ] ).fetchall()

	sentences = []
	for record in records :
	
		# parse
		title    = record[ 0 ]
		item     = record[ 1 ]
		sentence = record[ 2 ]
		distance = record[ 3 ]
		
		# short-circuit
		if distance > 1 : break
		
		# update
		sentences.append( [ title, item, sentence ] )
	
	# create a dataframe of the sentences and sort by title
	sentences = DataFrame( sentences, columns=COLUMNS )
	return( sentences.to_json( orient='index' ) )

@server.prompt()
def p_getSentencesWord( carrel:str, query:str ) :
    '''Return the sentences including or semantically similar to the given word or phrase from the given carrel'''
    return( f'''Given the carrel named '{carrel}' list all of the sentences including or are semantically similar to the word or phrase '{query}'.''' )


############## keywords from carrel ##############

@server.tool()
def getKeywords( carrel:str ) -> str :
    """Count and tabulate the keywords associated with the given study carrel. This process addresses the questions, "What sorts of things are discussed in this carrel?" or "What is the carrel about?"
	Args:
		carrel (str): The name of a carrel.
    Returns:
        str: a tab-delimited list of carrel keywords and their associated frequencies"""
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
    return( rdr.word2vec( carrel, type='similarity', query=word, topn=depth ) )

@server.prompt()
def p_getSemanticallySimilarWords( carrel:str, word:str, depth:int ) :
    """From the given carrel, word, and depth, count and tabulate the semantically simlar words"""
    return f"""Given the carrel named '{carrel}', count and tabulate the semantically simlar to '{word}' and limit the output to '{depth}' words."""


############## ungrams ##############

@server.tool()
def getUnigrams( carrel:str ) -> str :
    """
    	Outputs the counts and tabulations of the most frequent individual words (unigrams) in the given carrel. The output will be limited to approximately 1000 items to prevent exceeding prompt lengths. This process addresses the question "What sorts of things are discussed in this carrel?"
		Args:
			carrel (str): The name of a carrel.
    	Returns:
        	str: a list of the carrel's most frequent unigrams
    """
    LIMIT = 1024
    return( str( rdr.ngrams( carrel, size=1, count=True ).splitlines()[ :LIMIT ] ) )

@server.prompt()
def p_getUnigrams( carrel:str, size:int ) :
    """Count & tabulate individual words (unigrams) in the given carrel"""
    return f"""Given the carrel named '{carrel}', count and tabulate the most frequent individual words (unigrams)."""

############## ungrams ##############

@server.tool()
def getBigrams( carrel:str ) -> str :
    """
    	Outputs the counts and tabulations of the two-word phrases (bigrams) from the given carrel. The output will be limited to approximately 1000 items to prevent exceeding prompt lengths. This process addresses the question "What sorts of things are discussed in this carrel?"
		Args:
			carrel (str): The name of a carrel.
    	Returns:
        	str: a list of the carrel's most frequent bigrams
    """
    LIMIT = 1024
    return( str( rdr.ngrams( carrel, size=2, count=True ).splitlines()[ :LIMIT ] ) )

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
		Output the bibliographic metadata (author, title, date, summary, keywords, flesch score, and number of words) for the given carrel.
		Args:
			carrel (str): The name of a carrel.
		Returns:
			str: a JSON stream including an identifier, author, title, date, summary, keywords, Flesch (readability) score, and number of words.
	"""
	return( rdr.bibliography( carrel, format='json' ) )

@server.prompt()
def p_getBibliography( carrel:str ) :
    """Given the name of a carrel, output the bibliographic elements of each item in the carrel"""
    return( f"""Given the carrel named '{carrel}', output the identifier, author, title, date, summary, keywords, Flesch (readability) score, and size measure in words for each item in the carrel.""" )


############## extents ##############

@server.tool()
def getExtents( carrel:str, type:str ) -> int:
    """
		Given the name of a study carrel and the type of an extent (items, words, or flesch) return the size of the carrel.
		Args:
			carrel (str): The name of a local Distant Reader study carrel.
			type (str): One of three values: 1) items, 2) words, 3) flesch score
		Returns:
			int: a number denoting the quanity of the given type
    """
    return( rdr.extents( carrel, type ) )

@server.prompt()
def p_getExtents( carrel:str, type:str ) :
    """Get extents (size measured in words, flesch (readability), size measured in items)."""
    return f"""Return the extent '{type}' from the carrel named '{carrel}'."""


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
if __name__ == "__main__" : server.run( transport="streamable-http" )

