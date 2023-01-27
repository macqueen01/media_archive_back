from django.test import TestCase
from django.utils import timezone

from sample_backend.models import *
from sample_backend.Documents.SearchEngine.main import search_users, search_cases

# Create your tests here.

class TestVideoCaseSearch(TestCase):

    def sanity_check(self):
        """
        Sanity Check
        """
        pass

    def mock_video_model_search(self):
        """
        This tests if fuzziness search works fine with all case model searches
        """

        person = Personel(title="강진욱2", created_at = timezone.now(), private=1)
        person.save()

        new_vid = VideoCase(
            title = '새로운 이름의 영상 기록물',
            created_at = timezone.now(),
            private = 1,
            produced = 1,
            associate = person,
            content = "새로운 이름의 영상 기록물의 새로운 내용입니다. 가나 다라마 김재우"
        )
        new_vid.save()

        

        new_media = VideoMedia(
            created_at = timezone.now(),
        )
        new_media.save()
        new_media.referenced_in.add(new_vid)
        new_media.save()

        search_result = search_cases('김재우', start=0, end=11)
        search_result2 = search_cases('새로우 이르 기로묵 ㄱ심재우')
        
        assert(new_vid.id in [hit['id'] for hit in search_result])
        assert(new_vid.id in [hit['id'] for hit in search_result2])
    



