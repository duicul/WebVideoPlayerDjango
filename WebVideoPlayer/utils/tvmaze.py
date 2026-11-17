import html
from html.parser import HTMLParser
import json
import logging
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


logger = logging.getLogger("django")
TVMAZE_API_URL = "https://api.tvmaze.com"
REQUEST_TIMEOUT = 15


class _SummaryTextParser(HTMLParser):
    BLOCK_TAGS = {"br", "li", "p"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)


def _summary_as_html(summary):
    parser = _SummaryTextParser()
    parser.feed(summary or "")
    lines = [" ".join(line.split()) for line in "".join(parser.parts).splitlines()]
    text = " ".join(line for line in lines if line)
    return html.escape(text) + (" <br/>" if text else "")


def get_episode_summaries(show, seasons, episodes):
    query = urlencode({"q": show, "embed": "episodes"})
    request = Request(
        "{}/singlesearch/shows?{}".format(TVMAZE_API_URL, query),
        headers={"User-Agent": "WebVideoPlayerDjango/1.0"},
    )
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            show_data = json.load(response)
    except HTTPError as error:
        if error.code == 404:
            logger.info("TVMaze did not find a show matching %s", show)
            return []
        raise

    embedded = show_data.get("_embedded", {})
    show_episodes = embedded.get("episodes", [])
    requested = {
        (int(season), int(episode))
        for season in seasons
        for episode in episodes
    }

    descriptions = []
    for episode_data in show_episodes:
        key = (episode_data.get("season"), episode_data.get("number"))
        if key not in requested:
            continue
        descriptions.append({
            "title": episode_data.get("name", ""),
            "summary": _summary_as_html(episode_data.get("summary")),
        })
    return descriptions
