from elasticsearch_dsl import Search, Q

from sample_backend.Documents import CaseDocument, UserDocument
from sample_backend.models import *

from sample_backend import client


def main(query):
    pass


if __name__ == '__main__':
    main()

# These are engine body implementations


def search_users(query):
    """
    Searches users with the query matching following  fields:

    @username
    @name
    @position
    @standing
    @client_ip
    @affiliation

    This search uses fuzziness and multimatch
    """

    s = Search(using=client, index='users')
    s = s.query('multi_match', query=query, fields=['username', 'name', 'position', 'standing', 'client_ip'], fuzziness=2)
    response = s.execute()
    return response

def search_cases(kw, start=0, end=11):
    if not (start < end):
        return False
    
    s = Search(using=client)

    query = Q("multi_match", query=kw, fields=['title', 'content'], fuzziness=2) & Q('terms', form = [0,1,2])

    # perform the search
    response = s.query(query)[start:end]

    return [{'form': hit.form, 'id': hit.id} for hit in response.execute()]

def search_personel(kw, start=0, end=11):
    if not (start < end):
        return False

    s = Search(using=client)

    query = Q("multi_match", query=kw, fields=['title', 'content'], fuzziness=2) & Q('terms', form = 3)

    # perform the search
    response = s.query(query)[start:end]

    return [{'form': hit.form, 'id': hit.id} for hit in response.execute()]

def search_location(kw, start=0, end=11):
    if not (start < end):
        return False

    s = Search(using=client)

    query = Q("multi_match", query=kw, fields=['title', 'content'], fuzziness=2) & Q('terms', form = 4)

    # perform the search
    response = s.query(query)[start:end]

    return [{'form': hit.form, 'id': hit.id} for hit in response.execute()]


def page_num_to_tuple(page_number, max=12):
    return ((page_number - 1) * max, page_number * max - 1)

