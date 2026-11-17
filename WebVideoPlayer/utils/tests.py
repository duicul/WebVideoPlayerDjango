from django.test import SimpleTestCase
from unittest.mock import Mock, patch
import json
import os
import tempfile
from unittest import skipUnless

from utils import path_walker


class DescriptionCacheTests(SimpleTestCase):
    def test_missing_or_empty_description_is_retrieved_again(self):
        cached_values = ({}, {"movie_title": "Cached title"}, {"descr_html": "  "})
        retrieved = {"descr_html": "IMDb description", "movie_title": "IMDb title"}

        with tempfile.TemporaryDirectory() as temp_dir:
            desc_path = os.path.join(temp_dir, "descr.json")
            for cached_value in cached_values:
                with self.subTest(cached_value=cached_value):
                    with open(desc_path, "w", encoding="utf-8") as desc_file:
                        json.dump(cached_value, desc_file)
                    retrieve = Mock(return_value=retrieved)

                    with patch.object(path_walker, "FORCE_RETRIEVE_IMDB", False):
                        result = path_walker.load_or_retrieve_description(
                            desc_path, retrieve)

                    self.assertEqual(result, retrieved)
                    retrieve.assert_called_once_with()

    def test_nonempty_description_uses_cache(self):
        cached_value = {"descr_html": "Cached description"}
        retrieve = Mock()

        with tempfile.TemporaryDirectory() as temp_dir:
            desc_path = os.path.join(temp_dir, "descr.json")
            with open(desc_path, "w", encoding="utf-8") as desc_file:
                json.dump(cached_value, desc_file)

            with patch.object(path_walker, "FORCE_RETRIEVE_IMDB", False):
                result = path_walker.load_or_retrieve_description(desc_path, retrieve)

        self.assertEqual(result, cached_value)
        retrieve.assert_not_called()


class IMDbEpisodeDescriptionTests(SimpleTestCase):
    def test_episode_plot_is_loaded_before_description_is_read(self):
        class IMDbObject(dict):
            def __init__(self, movie_id, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.movieID = movie_id

        episode = IMDbObject("episode-id", {"title": "Pilot"})
        episode_details = IMDbObject(
            "episode-id", {"title": "Pilot", "plot": ["Episode plot"]})
        show = IMDbObject("show-id")

        class FakeIMDb:
            def search_movie(self, title):
                return [IMDbObject("show-id", {"title": title})]

            def get_movie(self, movie_id):
                if movie_id == "show-id":
                    return show
                if movie_id == "episode-id":
                    return episode_details
                raise AssertionError("Unexpected IMDb movie ID: %s" % movie_id)

            def update(self, movie, info):
                if info == "episodes":
                    movie["episodes"] = {1: {2: episode}}
                else:
                    raise AssertionError("Unexpected IMDb info request: %s" % info)

        with tempfile.TemporaryDirectory() as temp_dir:
            desc_path = os.path.join(temp_dir, "descr.json")
            with patch.object(path_walker, "ia", FakeIMDb()), \
                    patch.object(path_walker, "imdb_cache", {"show": {}, "movie": {}}), \
                    patch.object(path_walker, "imdb_cache_id", {"show": {}, "movie": {}}):
                description = path_walker.create_description_episode(
                    desc_path, "Example Show", ["1"], ["2"])

            self.assertEqual(description["movie_title"], "Pilot <br/>")
            self.assertEqual(description["descr_html"], "Episode plot <br/>")
            with open(desc_path, encoding="utf-8") as desc_file:
                self.assertEqual(json.load(desc_file), description)


@skipUnless(
    os.environ.get("RUN_LIVE_IMDB_TESTS") == "1",
    "Set RUN_LIVE_IMDB_TESTS=1 to run live Cinemagoer tests.",
)
class LiveIMDbEpisodeDescriptionTests(SimpleTestCase):
    def test_breaking_bad_episode_synopsis_is_retrieved_from_imdb(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            desc_path = os.path.join(temp_dir, "descr.json")
            with patch.object(path_walker, "ia", path_walker.imdb.Cinemagoer()), \
                    patch.object(path_walker, "imdb_cache", {"show": {}, "movie": {}}), \
                    patch.object(path_walker, "imdb_cache_id", {"show": {}, "movie": {}}):
                description = path_walker.create_description_episode(
                    desc_path, "Breaking Bad", ["1"], ["1"])

        self.assertTrue(description["movie_title"].strip())
        self.assertTrue(description["descr_html"].strip())
