


About Distant Reader Study Carrels
==================================

tl;dnr - Distant Reader study carrels are data sets, and they are designed to be read by computers as well as people. The purposes of study carrels are to: 1) address the problem of information overload, and 2) faciliate reading at scale. See the Distant Reader home page (https://distantreader.org) for more detail.


Introduction
------------

The Distant Reader and the Distant Reader Toolbox take collections of files as input, and they output data sets called "study carrels". Through the use of study carrels, students, researchers, and scholars can analyze, use, and understand -- read -- large corpora of narrative text, where "large" is anything from a dozen journal articles to hundreds of books. Through this process you can quickly and easily address research questions ranging from the mundane to the sublime:

  * How many items are in this carrel; is the size of this corpus
    big or small?
  
  * What are the things mentioned in this carrel, what do they do,
    and how do they do it?
  
  * In more than a few sentences, what is the content of this
    carrel about and provide specific examples.
  
  * What are the over-arching themes in the carrel, and how have
    they ebbed and flowed over time?
  
  * What is St. Augustine's definition of love, and how does it
    compare to Rousseau's?

  * How do the sum of writings by Plato and Aristotle compare?
  
The balance of this document outlines the structure of every study carrel and introduces you on how to use them.


Layout
------

Study carrels are directories made up of many subdirectories and files. Each study carrel contains these two directories:

  1. cache - original documents used to create the carrel

  2. txt - plain text versions of the cached content; almost all
     analysis is done against the files in this directory
  
There are additional subdirectories filled with tab-delimited files of extracted features:

  1. adr - email addresses
  2. bib - bibliographics (authors, titles, dates, etc.)
  2. ent - named-entities (people, organizations, places, etc.)
  3. pos - parts-of-speech (nouns, verbs, adjectives, etc.)
  4. urls - URLs and their domains
  5. wrd - statistically signficant keywords
  
Even though none of the files in the subdirectories have extensions of .tsv or .tab, they are all tab-delimited files, and therefore they can be imported into any spreadsheet, database, or programming language.

Each study carrel includes two more subdirectories:

  1. figures - where images are saved

  2. etc - everything else, and of greatest importance is the
     carrel's stop word list, bag-of-word representation of the
     carrel, and the carrel's SQLite database file
  
Depending on how the carrel was computed against (modeled), there may be a number of files at the root of each study carrel, and these files are readable by a wide variety of desktop applications and programming languages:

  * index.csv - if the study carrel creation process was augmented
    with a metadata values file (authors, titles, dates, etc.), then
    that file is echoed here

  * index.gml - a Graph Modeling Language file of the carrel's
    author(s), titles, and computed keywords, and useful for
    visualizing their relationships

  * index.htm - an HTML file summarizing the characteristics of the
    extracted features; start here

  * index.json - same as the index.txt file, but in a JSON form

  * index.rdf - bibliographic characteristics encoded in the form
    of the Resource Description Framework, and intended for the
    purposes of supporting the Semantic Web

  * index.tsv - a very very rudimentary list of characateristics
    denoting whence the carrel came and when

  * index.txt - a bibliographic report in the form of a plain text
    file

  * index.xml - a browsable interface to the study carrel; renders
    much easier on the Web than on your local computer

  * index.zip - the whole study carrel compressed into a single
    file for the purposes of collaborating, sharing, and downloading


Desktop Applications
--------------------

Study carrels are designed to be platform- and network-independent. What does this mean? It means two things: 1) no special software is needed to read study carrel data, and 2) if the study carrel is saved on your local computer, then no Internet connection is needed to analyze it. That said, you will want to employ the use of a variety of desktop applications (or programming languages) in order to get the most out of a study carrel.


Text Editors

Text editors are not word processors. While text editors and word processors both work with text, the former are more about the manipulation of the text, and the later are more about graphic design. The overwhelming majority of data found in study carrels is in the form of plain text, and you will find the use of a descent text editor indispensible. Using a text editor, you can open and read just about any file found in a study carrel. That's very important!

A good text editor supports powerful find and replace functionality, supports regular expressions, has the ability to open multi-megabyte files with ease, can turn on and off line wrapping, and reads text files created on different computer platforms. The following two text editors are recommended. Don't rely on Microsoft Word nor Google Docs, they are word processors.

  * BBEdit (https://www.barebones.com/products/bbedit/)
  * NotePad++ (https://notepad-plus-plus.org/)


Word Cloud Applications

The use of words clouds is often viewed as sophmoric. This is true because they are to often used to illustrate the frequency of all words in a text. On the other hand, if word clouds illustrate the frequencies of specific things -- keywords, parts-of-speech, or named entities -- then word clouds become much more complelling. After all, "A picture is worth a thousand words."

A program called Wordle is an excellent word cloud program. It takes raw text as input. It also accepts delimited data as input. The resulting images are colorful, configurable, and exportable. Unfortunately, it is no longer supported; while it will run on most Macintosh comuters, it will no longer run (easily) on Windows computers. (I would pay a fee to have Wordle come back to life and brought up-to-date.) If Wordle does not work for you, then there are an abundance of Web-based word cloud applications.

  * Wordle (https://web.archive.org/web/20191115162244/http://www.wordle.net/)
  

Concordances

Developed in the 13th Century, concordances are all but the oldest of text mining tools. They function like the rudimentary find function you see in many applications. Think control-f on steroids.

Concordances locate a given word in a text, display the text surrounding the word, and help you understand what other words are used in the same context. After all, to paraphrase a linguist named John Firth, "One shall know a word by the company it keeps." The following is a link to a concordance application that is worth way more than what you pay for it, which is nothing.

  * AntConc (https://www.laurenceanthony.net/software/antconc/)
  

Spreadsheet-Like Applications

The overwhelming majority of the content found in study carrels is in the form of plain text, and most of this plain text is structured in the form of tab-delimited text files -- matrixes or sometimes called "data frames". These files are readable by any spreadsheet, database, or programming language. Microsoft Excel, Google Sheets, or Macintosh Numbers can import Reader study carrel delimited data, but these programs are more about numerical analysis and less about analyzing text.

Thus, if you want to do analysis against Reader study carrel data, and if you do not want to write your own software, then the use of an analysis program called OpenRefine is highly recommended. OpenRefine eats delimited data for lunch. Once data is imported, OpenRefine supports powerful find and replace functions, counting and tabulating functions, faceting, sorting, exporting, etc. While text editors and concordances supplement traditional reading functions, OpenRefine supplements the process of understanding study carrels as data.

  * OpenRefine (https://openrefine.org/)


Topic Modeling Applications

Topic modeling is a type of machine learning process called "clustering". Given an integer (I), a topic modeler will divide a corpus into I clusters, and each cluster is akin to a theme. Thus, after practicing with a topic modeler, you can address questions like: what are the things this corpus is about, to what degee are themes manifested across the corpus, and which documents are best represented by the themes. After supplementing the corpus with metadata (authors, titles, dates, keywords, geners, etc.) Topic modeling becomes even more useful because you can address additional questions, such as: how did these themes ebb and flow over time, who wrote about what, and how is this style of writting different from that style. 

A venerable MALLET application is the grand-daddy of topic modeling tools, but is a command-line driven thing. On the other hand, a program called Topic Modeling Tool, which is rooted in MALLET, brings topic modeling to the desktop. Like all the applications listed here, it's use requires practice, but it works well, it works quickly, and the data it outputs can be used in a variety of ways.

  * MALLET (https://mimno.github.io/Mallet/)
  * Topic Modeling Tool (https://github.com/senderle/topic-modeling-tool)
  

Network Analysis Applications

Texts can be modeled in the form of networks -- nodes and edges. For example, there are authors (nodes), there are written works (additional nodes), and specific authors write specific works (edges). Similarly, there are works (nodes), there are keywords (additional nodes), and specific works are described with keywords (edges). Given these sorts of networks you can address -- and visualize -- all sorts of questions: who wrote what, what author wrote the most, what keywords dominate the collection, or what keywords are highly significant (central) to many works and therefore authors? 

Network analysis is rooted in graph theory, and it is not a trivial process. On the other hand, a program called Gephi makes the process easier. Import one of any number of different graph formats or specifically shaped matrixes, apply any number layout options to visualize the graph, filter the graph, visualize again, apply clustering or calcuate graph characteristics, and visualize a third time. The process requires practice, some knowledge of graph theory, and an aesthetic sensibility. In the end, you will garnder a greater understanding of the content in your carrel.

  * Gephi (https://gephi.org)


Command-Line (Shell) Interface
------------------------------

The Distant Reader and its companion, the Distant Reader Toolbox, are implemented as a set of Python modules. If you have Python installed, then from the command line you can install the modules -- the Toolbox:

  pip install reader-toolbox

If you are a developer, then you may want to use GitHub to install from source:

  git clone https://github.com/ericleasemorgan/reader-toolbox.git
  cd reader-toolbox
  pip install -e .

Once installed, you can run variations of the rdr ("reader") command. For example, running rdr without any arguments returns a menu:
  
  Usage: rdr [OPTIONS] COMMAND [ARGS]...

  Options:
    --help  Show this message and exit.
  
  Commands:
    about          Output a brief description and version number of the...
    adr            Filter email addresses from <carrel>
    bib            Output rudimentary bibliographics from <carrel>
    browse         Peruse <carrel> as a file system
    build          Create <carrel> from files in <directory>
    catalog        List study carrels
    cluster        Apply dimension reduction to <carrel> and visualize the...
    collocations   Output network graph based on bigram collocations in...
    concordance    A poor man's search engine
    documentation  Use your Web browser to read the Toolbox (rdr) online...
    download       Cache <carrel> from the public library of study carrels
    edit           Modify the stop word list of <carrel>
    ent            Filter named entities and types of entities found in...
    get            Echo the values denoted by the set subcommand
    grammars       Extract sentence fragments from <carrel> as in:
    info           Output metadata describing <carrel>
    ngrams         Output and list words or phrases found in <carrel>
    notebooks      Download, list, and run Toolbox-specific Jupyter Notebooks
    play           Play the word game called hangman
    pos            Filter parts-of-speech, words, and lemmas found in <carrel>
    rdfgraph       Create RDF (Linked Data) file against <carrel>
    read           Open <carrel> in your Web browser
    readability    Report on the readability (Flesch score) of items in...
    search         Perform a full text query against <carrel>
    semantics      Apply semantic indexing against <carrel>
    sentences      Given <carrel> save, output, and process sentences
    set            Configure the location of study carrels, the subsystem...
    sizes          Report on the sizes (in words) of items in <carrel>
    sql            Use SQL queries against the database of <carrel>
    summarize      Summarize <carrel>
    tm             Apply topic modeling against <carrel>
    url            Filter URLs and domains from <carrel>
    web            Experimental Web interface to your Distant Reader study...
    wrd            Filter statistically computed keywords from <carrel>
    zip            Create an archive (index.zip) file of <carrel>

Use the rdr command to build study carrels and do analysis against them. For example: 1) create a directory on your desktop and call it "practice", 2) copy a few PDF files into the directory, 3) open your terminal, 4) change directories to the desktop, and 5) run the following command to create your a carrel named "my-first-carrel":

  rdr build my-first-carrel practice -s

Once you get this far, you can run many other rdr commands:

  * rdr info my-first-carrel
  * rdr bib my-first-carrel
  * rdr concordance my-first-carrel
  * rdr tm my-first-carrel
  
For more detail, run the rdr command with the --help flag. See also the documentation: https://reader-toolbox.readthedocs.io/

Power-user hints: The output of many rdr commands are designed to be post-processed by the command line shell. For example, suppose you have a study carrel named "homer", then the following command will display the results of the bib command one screen at a time:

  rdr bib homer | more

A carrel's bibliographics can also be output as a JSON stream, and by piping the output to many additional commands, you can create a prettier bibliography:

  rdr bib homer -f json              | \
  jq -r '.[]|[.title,.summary]|@tsv' | \
  sed "s/\t/ -- /"                   | \
  sed "s/$/\n/"                      | \
  fold -s                            | \
  less

Suppose you wanted to extract rudimentary definitions of the word "whales" from a carrel named "moby", then the following is a quick and dirty way to get the job done:

  Q='whales are'; rdr concordance moby -q "$Q" -w 60 | sed "s/^.*$Q/$Q/"
  
Creating a nice list of sentences is similar:

  Q='whales are'; rdr sentences moby -p filter -q "$Q" | \
  sed "s/$/\n/"                                        | \
  fold -s                                              | \
  less -i --pattern="$Q"
  

Write your own software
-----------------------

The Reader Toolbox can also be imported into Python scripts, and consequently you can combine its functionality with other Python modules. For example the power-user concordance command, above, can be written as a Python script:

  # configure
  CARREL = 'moby'
  QUERY  = 'whales are'
  WIDTH  = 60
  
  # require
  from rdr import concordance
  from re  import sub
  
  # do the work, output, and done
  lines = concordance(CARREL, query=QUERY, width=WIDTH)
  [print(sub('^.*{}'.format(QUERY), QUERY, line)) for line in lines]
  exit()

Use pydoc to learn more: pydoc rdr


Summary
-------

Distant Reader and the Distant Reader Toolbox take sets of narrative text as input, and they output data sets called study carrels. The content of study carrels are intended to be read by computers as well as people. Study carrels are platform- as well as network-independent, and therefore they are designed to stand the test of time.

Use desktop software and/or the Reader Toolbox to build, download, search, browse, peruse, investigate, and report on the content of study carrels. Use the extracted features as if they were items found in a back-of-the-book index, and use them as input to concordances for the purpose of closer reading. Topic model study carrels to enumerate latent themes and address the question, "How do themes ebb and flow over time?" Import the index.gml files into Gephi (or any other network graph application) to visualize how authors, titles, and dates are related. All of this is just the tip of the iceberg; study carrels can do much more.

Study carrels are intended to address the problem of information overload. They make it easier to use and understand large volumes of text -- dozens of books or hundreds of journal articles. Through the process you can address all sorts of research questions, and in the end you will have supplemented your traditional reading process and you will have been both more thorough and more comprehensive in your research.

--
Eric Lease Morgan <emorgan@nd.edu>
Navari Family Center for Digital Scholarship
Hesburgh Libraries
University of Notre Dame

October 9, 2024

