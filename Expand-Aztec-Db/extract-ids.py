import os
from urllib import urlopen
from urllib import quote
from urllib import urlencode
import simplejson
# from Bio import Entrez

""" Get list of DOIs
This file is responsible for retrieving a list of DOIs, PMIDs, and PMCIDs
for publications that have a source code repository (Github, Bitbucket,
Bioconductor, and Sourceforge).
"""

def get_ids(query_url, database):
    """get ids for github/Sourceforge
    return: map of ids from key-word to list of ids
    """
    ids = dict.fromkeys(["github", "bitbucket", "sourceforge"])
    search_query= {'db': database,
                   'retmode': 'json',
                   'retmax' : '1000',
                   'retstart': '0',
                   'term': 'github',}
    for search_term in ids:
        retstart, count = 0, 1000
        results_for_search_term = []
        search_query['term'] = search_term
        print search_query
        while retstart < count:
            print retstart, count, search_term
            search_query['retstart'] = str(retstart)
            query_string = urlencode(search_query)
            connection_pubmed = urlopen(query_url+query_string)
            response_pubmed = simplejson.load(connection_pubmed)
            count = int(response_pubmed['esearchresult']['count'])
            results_for_search_term.extend(response_pubmed['esearchresult']['idlist'])
            retstart+=1000
        ids[search_term] = results_for_search_term
    return ids

pubmed_db  = get_ids('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?', 'pubmed')

#get_ids('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%22Bioinformatics%20&retmode=json&retmax=1000&retstart=')
