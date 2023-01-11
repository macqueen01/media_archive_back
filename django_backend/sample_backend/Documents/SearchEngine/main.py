from elasticsearch_dsl import Search

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
    s = s.query('multi_match', query=query, fields=['username', 'name', 'position', 'standing', 'client_ip', 'affiliation'], fuzziness=2)
    response = s.execute()
    return response

def search_video_cases(query):
    s = Search(using=client, index='video_cases')
    s = s.query('multi_match', query=query, fields=['title', 'content', 'associate', 'attendee', 'location', 'affiliation'], fuzziness=2)
    response = s.execute()
    return response
