# Copyright (c) 2020, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Define the CLI for enriching BiGG reaction information."""


import json
import logging
from pathlib import Path

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ...api.reaction import bigg as bigg_api
from ..helpers import JSON_SEPARATORS


logger = logging.getLogger(__name__)


Session = sessionmaker()


@click.group()
@click.help_option("--help", "-h")
def bigg():
    """Subcommand for processing BiGG information."""
    pass


@bigg.command()
@click.help_option("--help", "-h")
@click.option(
    "--filename",
    "-f",
    type=click.Path(dir_okay=False, writable=True),
    default="bigg_universal_reactions.json",
    show_default=True,
    help="The output path for the BiGG universal bigg JSON response.",
)
def extract(filename: click.Path):
    """Fetch all BiGG universal reactions."""
    logger.info("Downloading BiGG universal reactions.")
    with Path(filename).open("w") as handle:
        handle.write(bigg_api.extract())


@bigg.command()
@click.help_option("--help", "-h")
@click.argument(
    "response", metavar="<RESPONSE>", type=click.Path(dir_okay=False, exists=True)
)
@click.option(
    "--filename",
    "-f",
    type=click.Path(dir_okay=False, writable=True),
    default="bigg_reaction_names.json",
    show_default=True,
    help="The output path for the BiGG reaction identifier to name mapping JSON file.",
)
def transform(response: click.Path, filename: click.Path):
    """
    Generate a mapping of BiGG reaction identifiers to names.

    \b
    RESPONSE is the JSON response containing BiGG universal reactions.

    """
    logger.info("Generating BiGG universal reactions identifier to name mapping.")
    with Path(response).open() as handle:
        id2name = bigg_api.transform(handle.read())
    with Path(filename).open("w") as handle:
        json.dump(id2name, handle, separators=JSON_SEPARATORS)


@bigg.command()
@click.help_option("--help", "-h")
@click.argument("db-uri", metavar="<URI>")
@click.argument(
    "filename", metavar="<FILENAME>", type=click.Path(dir_okay=False, exists=True)
)
def load(db_uri: str, filename: click.Path):
    """
    Load BiGG reaction names into a database.

    \b
    URI is a string interpreted as an rfc1738 compatible database URI.
    FILENAME is the BiGG reaction identifier to name mapping JSON file.

    """
    engine = create_engine(db_uri)
    session = Session(bind=engine)
    with Path(filename).open() as handle:
        id2name = json.load(handle)
    logger.info("Adding BiGG universal reaction names to database.")
    try:
        bigg_api.load(session, id2name)
    finally:
        session.close()
