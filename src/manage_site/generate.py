"""
TODO: Doc
"""

import argparse
import jinja2
from pathlib import Path

from .model import Data


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>TODO</title>
  <link href="index.css" rel="stylesheet">
</head>
<body>
  <div id="main">

    <div id="header">
      <!-- TODO: Put something in the header? -->
    </div>

    <div id="row-container">

      {% for row in rows %}
      <div class="row {{ 'debug' if debug_css else '' }}">

        {% for photo in row.photos %}
        <a
          class="photo-container {{ 'debug' if debug_css else '' }}"
          href="{{ photo_link_prefix }}/{{ photo.identifier }}"
          target="_blank">

          <img
            class="photo"
            src="{{ photo_link_prefix }}/{{ photo.identifier }}"
            alt="{{ photo.text }}"
            title="{{ photo.text }}" />

        </a>
        {% endfor %}

      </div>
      {% endfor %}

    </div>
  </div>
</body>
</html>
"""


def render(data: Data, *, debug_css: bool, photo_link_prefix: str) -> str:
    """
    Use the Jinja2[1] templating enginer to interpolate <data> into <HTML_TEMPLATE>.

    [1] https://jinja.palletsprojects.com/en/3.0.x/
    """
    # Tell the engine to fail if any variables are undefined! The
    # default is to just write the empty string, which is probably
    # a bug in our case :^)
    env = jinja2.Environment(undefined=jinja2.StrictUndefined)

    # Turn the plain <str> we defined above into an object that we
    # can "render" with some **kwargs.
    template = env.from_string(HTML_TEMPLATE)
    return template.render(
        rows=data.rows,
        debug_css=debug_css,
        photo_link_prefix=photo_link_prefix,
    )


def main() -> None:
    # Define the command-line args that we know how to handle.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-i",
        "--input-data",
        type=Path,
        default="data.yml",
        help="Path to the *.yml file that defines which images to show.",
    )
    parser.add_argument(
        "--photo-link-prefix",
        default="photos",
        help="Path (or URL prefix) to directory containing photos.",
    )
    parser.add_argument(
        "--debug-css",
        action="store_true",
        help="If passed, display magenta borders around some elements.",
    )
    args = parser.parse_args()

    # Read in the data from disk that we were given.
    data = Data.load(args.input_data)

    # Take the values from that data and use them to generate
    # an HTML document (string).
    document = render(data, debug_css=args.debug_css, photo_link_prefix=args.photo_link_prefix,)

    # Print the document (to <stdout>) so other tools can decide
    # what to do with it (e.g., save it somewhere on disk).
    print(document)
