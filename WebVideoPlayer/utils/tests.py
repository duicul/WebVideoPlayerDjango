import os
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase

from utils import path_walker


class CreateDescriptionEpisodeTests(SimpleTestCase):
    def test_fetches_episode_plot_when_episodes_list_does_not_include_it(self):
        episode = {"title": "The Episode"}
        series = {"episodes": {1: {2: episode}}}
        imdb_client = SimpleNamespace(
            search_movie=lambda show: [SimpleNamespace(movieID="123")],
            get_movie=lambda movie_id: series,
        )

        def update(movie, info):
            if info == "plot":
                movie["plot"] = ["The episode plot"]

        imdb_client.update = update

        with patch.object(path_walker, "ia", imdb_client), \
                patch.dict(path_walker.imdb_cache["show"], {}, clear=True), \
                patch.dict(path_walker.imdb_cache_id["show"], {}, clear=True):
            result = path_walker.create_description_episode(
                self.make_desc_path(), "Example Show", ["01"], ["02"]
            )

        self.assertIn("The episode plot", result["descr_html"])
        self.assertIn("The Episode", result["movie_title"])

    def make_desc_path(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        return os.path.join(directory.name, "descr.json")
