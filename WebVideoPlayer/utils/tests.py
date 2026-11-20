from django.test import SimpleTestCase
from unittest.mock import Mock, patch
import json
import os
import tempfile
from io import BytesIO
from unittest import skipUnless
from urllib.error import HTTPError

from utils import path_walker
from utils import tvmaze


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

    def test_description_from_different_source_is_retrieved_again(self):
        cached_value = {"descr_html": "IMDb description", "source": "imdb"}
        retrieved = {"descr_html": "TVMaze description", "source": "tvmaze"}
        retrieve = Mock(return_value=retrieved)

        with tempfile.TemporaryDirectory() as temp_dir:
            desc_path = os.path.join(temp_dir, "descr.json")
            with open(desc_path, "w", encoding="utf-8") as desc_file:
                json.dump(cached_value, desc_file)

            result = path_walker.load_or_retrieve_description(
                desc_path, retrieve, expected_source="tvmaze")

        self.assertEqual(result, retrieved)
        retrieve.assert_called_once_with()


class TVMazeEpisodeDescriptionTests(SimpleTestCase):
    def test_episode_description_uses_tvmaze_summary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            desc_path = os.path.join(temp_dir, "descr.json")
            with patch.object(
                    path_walker.tvmaze, "get_episode_summaries",
                    return_value=[{
                        "title": "Pilot",
                        "summary": "Episode plot <br/>",
                    }]) as get_summaries:
                description = path_walker.create_description_episode(
                    desc_path, "Example Show", ["1"], ["2"])

            get_summaries.assert_called_once_with("Example Show", ["1"], ["2"])
            self.assertEqual(description["movie_title"], "Pilot <br/>")
            self.assertEqual(description["descr_html"], "Episode plot <br/>")
            self.assertEqual(description["source"], "tvmaze")
            with open(desc_path, encoding="utf-8") as desc_file:
                self.assertEqual(json.load(desc_file), description)


class TVMazeClientTests(SimpleTestCase):
    def setUp(self):
        tvmaze._get_show_episodes.cache_clear()
        self.addCleanup(tvmaze._get_show_episodes.cache_clear)

    def test_episode_search_returns_matching_summary_as_safe_html(self):
        response_data = {
            "name": "Example Show",
            "_embedded": {
                "episodes": [
                    {
                        "season": 1,
                        "number": 2,
                        "name": "Pilot",
                        "summary": (
                            "<p>Example <strong>plot</strong> &amp; "
                            "<em>friends</em>.</p>"
                        ),
                    },
                    {
                        "season": 1,
                        "number": 3,
                        "name": "Other Episode",
                        "summary": "<p>Not requested.</p>",
                    },
                ],
            },
        }
        response = BytesIO(json.dumps(response_data).encode("utf-8"))

        with patch.object(tvmaze, "urlopen", return_value=response) as open_url:
            result = tvmaze.get_episode_summaries("Example Show", ["1"], ["2"])

        self.assertEqual(result, [{
            "title": "Pilot",
            "summary": "Example plot &amp; friends. <br/>",
        }])
        request = open_url.call_args[0][0]
        self.assertIn("api.tvmaze.com/singlesearch/shows?", request.full_url)
        self.assertIn("q=Example+Show", request.full_url)
        self.assertEqual(open_url.call_args[1]["timeout"], tvmaze.REQUEST_TIMEOUT)

    def test_episode_search_reuses_show_response(self):
        response_data = {
            "_embedded": {
                "episodes": [
                    {"season": 1, "number": 1, "name": "Pilot", "summary": "<p>One</p>"},
                    {"season": 1, "number": 2, "name": "Second", "summary": "<p>Two</p>"},
                ],
            },
        }
        response = BytesIO(json.dumps(response_data).encode("utf-8"))

        with patch.object(tvmaze, "urlopen", return_value=response) as open_url:
            first = tvmaze.get_episode_summaries("Cached Example", ["1"], ["1"])
            second = tvmaze.get_episode_summaries("Cached Example", ["1"], ["2"])

        open_url.assert_called_once()
        self.assertEqual(first[0]["title"], "Pilot")
        self.assertEqual(second[0]["title"], "Second")

    def test_unknown_show_returns_no_episode_descriptions(self):
        error = HTTPError(
            "https://api.tvmaze.com/singlesearch/shows?q=unknown",
            404, "Not Found", None, None)
        with patch.object(tvmaze, "urlopen", side_effect=error):
            result = tvmaze.get_episode_summaries("Unknown Show", ["1"], ["1"])

        self.assertEqual(result, [])


@skipUnless(
    os.environ.get("RUN_LIVE_TVMAZE_TESTS") == "1",
    "Set RUN_LIVE_TVMAZE_TESTS=1 to run live TVMaze tests.",
)
class LiveTVMazeEpisodeDescriptionTests(SimpleTestCase):
    def test_breaking_bad_episode_synopsis_is_retrieved_from_tvmaze(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            desc_path = os.path.join(temp_dir, "descr.json")
            description = path_walker.create_description_episode(
                desc_path, "Breaking Bad", ["1"], ["1"])

        self.assertTrue(description["movie_title"].strip())
        self.assertTrue(description["descr_html"].strip())
        self.assertEqual(description["source"], "tvmaze")
