#!/usr/bin/env python

# server.py - a Distant Reader MCP server

# Eric Lease Morgan <eric_morgan@infomotions.com>
# (c) Infomotions, LLC; distributed under a GNU Public License

# April 27, 2026 - first cut
# April 28, 2026 - added unigrams; this is working!
# April 29, 2026 - added sentences and keywords
# May    3, 2026 - added a few more tools and associated prompts; I don't thing resources work
# May    7, 2026 - added even more tool; this is really working very well
# May    8, 2026 - added get full path to original items


# configure
NAME    = 'Distant Reader MCP Server'
LIBRARY = 'localLibrary'
TXT     = 'txt'
DROPS   = [ 'browse', 'download', 'read', 'bibliography (JSON)', 'bibliography (plain text)', 'provenance', 'gml (Graph Modeling Language)', 'metadata', 'RDF/XML' ]

# require
from collections        import Counter
from contextlib         import redirect_stdout
from io                 import StringIO
from json               import loads
from mcp.server.fastmcp import FastMCP
from pandas             import read_csv
import rdr

# initailize
server  = FastMCP( NAME, json_response=True, stateless_http=True )
library = rdr.configuration( LIBRARY )


############## pos: adjectives ##############

@server.tool()
def get_carrel_adjectives( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of of all the adjectives identified as a part-of-speech value. This process helps identify how the things in this carrel are described.
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of adjectives form the given carrel
	'''
	return( str( rdr.pos(carrel, select='lemma', like='ADJ', count=True ) ) )

@server.prompt()
def p_get_carrel_adjectives( carrel:str ) :
    '''Get all adjectives from the given carrel and extracted from the parts-of-speech process'''
    return( f'''Given the carrel named '{carrel}', return a frequency list of all the adjectives.''' )


############## full path to origial document ##############

@server.tool()
def get_fullpath_to_original_item( carrel: str, item:str ) -> str:
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
def p_fullpath_to_original_item( carrel:str, item: str ) :
    '''The the full path to the original version of the given item in the given carrel'''
    return( f'''Given the carrel named '{carrel}', return the full path to the original version of '{item}'.''' )


############## pos: verbs ##############

@server.tool()
def get_carrel_verbs( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of of all the lemmatized version of verbs identified as a part-of-speech value. This process helps identify what the things in this carrel do; what actions do they take.
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of lemmatized verbs form the given carrel
	'''
	return( str( rdr.pos(carrel, select='lemma', like='VERB', count=True ) ) )

@server.prompt()
def p_get_carrel_verbs( carrel:str ) :
    '''Get all lemmatized verbs from the given carrel and extracted from the parts-of-speech process'''
    return( f'''Given the carrel named '{carrel}', return the lemmatized part-of-speech value of VERB.''' )


############## pos: nouns ##############

@server.tool()
def get_carrel_nouns( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of of all the nouns identified as a part-of-speech value
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of nouns form the given carrel
	'''
	LIMIT = 1024
	#return( str( rdr.ngrams( carrel, size=1, count=True ).splitlines()[ :LIMIT ] ) )
	return( str( rdr.pos(carrel, select='words', like='NOUN', count=True ).splitlines()[ :LIMIT ] ) )

@server.prompt()
def p_get_carrel_nouns( carrel:str ) :
    '''Get all nouns from the given carrel and extracted from the parts-of-speech process'''
    return( f'''Given the carrel named '{carrel}', return part-of-speech of type NOUN.''' )


############## named-entitites: people ##############

@server.tool()
def get_carrel_people( carrel: str ) -> str:
	'''
		Given the name of a carrel output a frequency list of of all the people identified as a named entity
		Args:
			carrel (str): the name of a study carrel
		Returns: 
			str: a tab-delinmited list of people form the given carrel
	'''
	return( str( rdr.entities (carrel, select='entity', like='PERSON', count=True ) ) )

@server.prompt()
def p_get_carrel_people( carrel:str ) :
    '''Get all names of people from the given carrel and extracted from the named entity process'''
    return( f'''Given the carrel named '{carrel}', return named entities of type PERSON.''' )


############## item identifiers ##############

@server.tool()
def get_item_identifiers( carrel: str ) -> str:
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
def p_get_item_identifiers( carrel:str ) :
    '''Get all item identifiers from a given carrel'''
    return( f'''Given the carrel named '{carrel}', return all item identifiers it contains.''' )


############## plain text ##############

@server.tool()
def get_plaintext( carrel: str, id:str ) -> str:
	'''
		Given the name of a carrel and an identifier in the carrel, return the plain text of the item
		Args:
			carrel (str): the name of a study carrel
			id (str): an identifier pointing to an specific item in the carrel
		Returns: 
			str: the plain text of the given item
	'''
	id = id.replace( '‑', '-' )
	with open( library /carrel/TXT/(id + '.txt' ) ) as handle : plaintext = handle.read()
	return( plaintext )

@server.prompt()
def p_get_plaintext( carrel:str, id:str ) :
    '''Retrieve the plain text version of an item'''
    return( f'''Given the carrel named '{carrel}' and the identifier '{id}', get the plain text version of the item.''' )


############## words in sentences ##############

@server.tool()
def get_sentences_word( carrel:str, word:str ) -> str :
	"""
		Output all sentences from the given carrel which contain the given word or phrase
		Args:
			carrel (str): The name of a carrel.
			word (str): An individual word or phase
		Returns:
			str: a new-line delimited list of sentences
	"""
	sentences = StringIO()
	with redirect_stdout( sentences ): rdr.sentences( carrel, process='filter', query=word )	
	return( sentences.getvalue() )

@server.prompt()
def p_get_sentences_word( carrel:str, word:str ) :
    '''
    	Retrieve the plain text version of an item
    '''
    return( f'''Given the carrel named '{carrel}' list all of the sentences including the word '{word}'.''' )


############## keywords from carrel ##############

@server.tool()
def get_keywords( carrel:str ) -> str :
    """Count and tabulate the keywords associated with the given study carrel. This process addresses the question "What sorts of things are discussed in this carrel?"
	Args:
		carrel (str): The name of a carrel.
    Returns:
        str: a tab-delimited list of carrel keywords and their associated frequencies"""
    return( rdr.keywords( carrel, count=True ) )

@server.prompt()
def p_get_keywords( carrel:str, size:int ) :
    """Count and tabulate the keywords associated with the given study carrel"""
    return f"""
    Given the carrel named '{carrel}', count and tabulate the most frequent '{size}' keywords.  
    """

############## semantically similar words ##############

@server.tool()
def get_word2vec( carrel:str, word:str, depth:int=8 ) -> str :
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
def p_get_word2vec( carrel:str, word:str, depth:int ) :
    """From the given carrel, word, and depth, count and tabulate the semantically simlar words"""
    return f"""
    Given the carrel named '{carrel}', count and tabulate the semantically simlar to '{word}' and limitd the output to '{depth}' words.  
    """


############## ungrams ##############

@server.tool()
def get_unigrams( carrel:str ) -> str :
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
def p_get_unigrams( carrel:str, size:int ) :
    """Count & tabulate individual words (unigrams) in the given carrel"""
    return f"""Given the carrel named '{carrel}', count and tabulate the most frequent individual words (unigrams)."""

############## ungrams ##############

@server.tool()
def get_bigrams( carrel:str ) -> str :
    """
    	Outputs the counts and tabulations of the most two-word phrases (bigrams) from the given carrel. The output will be limited to approximately 1000 items to prevent exceeding prompt lengths. This process addresses the question "What sorts of things are discussed in this carrel?"
		Args:
			carrel (str): The name of a carrel.
    	Returns:
        	str: a list of the carrel's most frequent bigrams
    """
    LIMIT = 1024
    return( str( rdr.ngrams( carrel, size=2, count=True ).splitlines()[ :LIMIT ] ) )

@server.prompt()
def p_get_unigrams( carrel:str ) :
    """Count & tabulate two-word phrases (bigrams) in the given carrel"""
    return f"""Given the carrel named '{carrel}', count and tabulate the most frequent two-word phrases (bigrams)."""


############## unigram counts with filter ##############

@server.tool()
def get_count_unigrams_like( carrel:str, filter:str, size:int=32 ) -> str :
    """
    	Outputs the counts and tabulations of 32 most frequent individual words in the given carrel and matching the given query
			Args:
				carrel (str): The name of a carrel.
				filter (str): A regular expression used to filter the results
				size (int): Limit the output to this many words
    		Returns:
        		str: a list of the carrels accessible fron this system
    """
    return( str( rdr.ngrams( carrel, size=1, count=True, query=filter ).splitlines()[:size] ) )

@server.prompt()
def p_get_count_unigrams_like( carrel:str, filter:str, size:int, ) :
    """Count & tabulate individual words from the given carrel matching a regular expression filter"""
    return( f"""Given the carrel named '{carrel}', count and tabulate the most frequent '{size}' individual words matching a '{filter}'.""" )


############## catalog ##############

@server.tool()
def get_catalog() -> str :
    """
		Output the list of study carrels available from the local library.
    	Returns:
        	str: a list of the carrels accessible from the local library
    """
    return( rdr.catalog() )

@server.prompt()
def p_get_catalog() :
    """Get a list of the carrels available in the local library"""
    return( f"""In the form of a paragraph, list the carrels available from the local library.""" )


############## bibliography ##############

@server.tool()
def get_bibliography( carrel: str ) -> str:
	"""
		Output the bibliographic (author, title, date, summary, keywords, flesch score, number of words) information for the given carrel.
		Args:
			carrel (str): The name of a carrel.
		Returns:
			str: a JSON stream including an identifier, author, title, date, summary, keywords, Flesch (readability) score, and number of words.
	"""
	return( rdr.bibliography( carrel, format='json' ) )

@server.prompt()
def p_get_bibliography( carrel:str ) :
    """Given the name of a carrel, output the bibliographic elements of each item in the carrel"""
    return( f"""Given the carrel named '{carrel}', output the identifier, author, title, date, summary, keywords, Flesch (readability) score, and size measure in words for each item in the carrel.""" )


############## extents ##############

@server.tool()
def get_extents( carrel:str, type:str ) -> int:
    """
    Given the name of a study carrel and type of extent (items, words, or flesch) return the size of the carrel.
    Args:
        carrel (str): The name of a local Distant Reader study carrel.
        type (str): One of three values: 1) items, 2) words, 3) flesch score
    Returns:
        int: a number denoting the quanity of the given type
    """
    return( rdr.extents( carrel, type ) )

@server.prompt()
def p_get_extents( carrel:str, type:str ) :
    """Get extents (size measured in words, flesch (readability), size measured in items)."""
    return f"""Return the extent '{type}' from the carrel named '{carrel}'."""

############## catalog, remote ##############
#
#@server.tool()
#def get_remote_catalog( word:str='love' ) -> str :
#	"""
#		Output a list of the study carrels available from remote catalog at http://carrels.distantreader.org
#		Args:
#			word (str) : a regular expression used to limit the results
#		Returns:
#			str: a list of bibliographics (identifiers, authors, titles, dates, keyword, and extents for each item in the remote library.
#	"""
#	catalog = read_csv( StringIO( rdr.catalog( location='remote', human=False ) ) )
#	catalog = catalog.drop( DROPS, axis=1 )
#	catalog = catalog.fillna('')
#	catalog = catalog[ catalog[ 'keywords' ].str.contains( word ) ]
#	catalog = catalog.rename(columns={ 'id': 'identifier' } )
#	return( catalog.to_csv( index=False ) )
#
#@server.prompt()
#def p_get_remote_catalog( word:str ) :
#    """Get a list of carrels in the remote libraray as well as their bibliiographics"""
#    return f"""Get a list of carrels from the remote library and for each item list identifiers, authors, titles, extents, and keywords. Filter the result with the the word '{word}'"""
#
#
############## keywords, remote ##############
#
#@server.tool()
#def get_remote_catalog_keywords() -> dict :
#	"""
#		Output a frequency list of keywords from the remote library of study carrels
#		Returns:
#			str: a frequency list of keywords
#	"""
#	catalog  = read_csv( StringIO( rdr.catalog( location='remote', human=False ) ) )
#	return( dict( Counter( catalog[ 'keywords' ].str.cat().replace( ';', '' ).split() ) ) )
#
#@server.prompt()
#def get_remote_catalog_keywords( word:str ) :
#    """Get a frequency list of keywords from the remote library of study carrels """
#    return f"""Count and tabulate the keywords in the remote library of study carrels.'"""


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

	#server.run(transport="stdio")
	server.run(transport="streamable-http")