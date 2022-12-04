import json
import logging
import os

import click
import pandas as pd

from rap.generator import Generator
from rap.preprocessing import (
    Database_ops,
    Spider_preprocessing,
    Style_processing,
)
from rap.preprocessing.Tags import (
    DbTags,
)
from rap.scrapping import Scrapper
from rap.visualization import (
    ArtistVisualization,
    StyleVisualization,
)

# why is this needed?
STYLES = "Styles"


# to do: change to click.Choice (https://click.palletsprojects.com/en/8.1.x/options/#choice-options)
@click.command()
@click.option("--style", type=click.STRING, help="Style of the song to be generated")
@click.option("--artist", type=click.STRING, help="Artist of the song to be generated")
def generate(style: str, artist: str) -> None:
    """
    Generates a song given a style and an artist. Prints to stdout
    # TO DO: Split the function in generate and print, print by default but give the option to return the data
    :param style:
    :param artist:
    :return:
    """
    Generator.generar_cancion(style, artist)


@click.command()
@click.option(
    "--style",
    type=click.STRING,
    required=False,
    default=None,
    help="Style of the song to be written",
)
@click.option(
    "--artist",
    type=click.STRING,
    required=False,
    default=None,
    help="Artist of the song to be written",
)
@click.option(
    "--write-style",
    type=click.BOOL,
    is_flag=True,
    help="Whether or not to write a song based on the specified style",
)
@click.option(
    "--write-artist",
    type=click.BOOL,
    is_flag=True,
    help="Whether or not to write a song based on the specified artist",
)
def write(style: str, artist: str, write_style: bool, write_artist: bool) -> None:
    """
    Writes songs based on artist or style

    :param style:
    :param artist:
    :param write_style:
    :param write_artist:
    :return:
    """

    with open("resources/albums.json") as artist_files:
        n_albums = json.load(artist_files)[artist]

    # equivalent to checkpoint=cantante
    if write_style is None and write_artist is not None:

        songs_file = os.path.join(
            Scrapper.PATH_ARCHIVO_CANCIONES, style, artist, "_canciones.txt"
        )
        output_path = os.path.join(
            Scrapper.PATH_LETRA_CANCIONES, style, artist, Scrapper.TIPO_ARCHIVO
        )
        lista_url_de_canciones = Scrapper.get_urls_from_songs_file(songs_file)

        if os.path.exists(output_path):
            logging.info("Este archivo de letras ya existe")
            logging.info("Insertando letras de %s.txt" % artist)
        else:
            for cancion in lista_url_de_canciones:
                Scrapper.get_text_from_letras_com_soup(artist, cancion)

        Database_ops.file_to_mongo(
            os.path.join(Scrapper.PATH_LETRA_CANCIONES, style, artist, ".txt"),
            artist,
            style,
            n_albums,
        )

    # equivalent to checkpoint=estilo
    elif write_style is not None and write_artist is None:

        docs = Database_ops.set_style_collection(style)
        Style_processing.consolidate_style(docs, style, STYLES)

    # equivalent to checkpoint=todo
    # covers the cases of write_style=write_artist=[None | not None]
    else:
        docs = Database_ops.set_style_collection(STYLES)
        Style_processing.consolidate_style(docs, STYLES, STYLES)


@click.command()
@click.option(
    "--style",
    type=click.STRING,
    required=False,
    default=None,
    help="Style of the song to be read",
)
@click.option(
    "--artist",
    type=click.STRING,
    required=False,
    default=None,
    help="Artist of the song to be read",
)
def read(style: str, artist: str) -> None:
    """
    Reads an already written song

    :param style:
    :param artist:
    :return:
    """
    stats = Database_ops.set_style_collection(style).find()
    data = pd.DataFrame(list(stats))
    clean_data = Spider_preprocessing.df_cleaning(data)

    if style is None and artist is not None:

        # 1. Primera visualización: FreqDist

        statistics = Database_ops.read_artist_from_mongo(style, artist, "text_no_sw")
        ArtistVisualization.show_freqdist(statistics)

        # 2. Segunda visualización: SpiderPlot
        # maybe use clean_data instead of data?
        data_spider = clean_data[clean_data["_id"] == artist][
            [DbTags.id, DbTags.text_raw, DbTags.text_no_sw, DbTags.unique_words]
        ]
        ArtistVisualization.show_spider_graph(data_spider)

    elif style is not None and artist is None:
        # 1. Primera visualización: WordCloud
        data_cloud = clean_data[clean_data[DbTags.id] == style][
            DbTags.text_no_sw
        ].values
        StyleVisualization.show_wordcloud(data_cloud)

        # 2. Segunda visualización: Graficos comparativos
        # data_no_cloud = data[data[DbTags.id] != style]
        StyleVisualization.compare_artists(data, style)

        # 3. Tercera visualización: Queso de discos
        n_albums_artistas = data[data[DbTags.id] != style][
            DbTags.number_of_albums
        ].values
        nombres_artistas = data[data[DbTags.id] != style][DbTags.id].values

        StyleVisualization.piechart(n_albums_artistas, nombres_artistas)


@click.command()
@click.option(
    "--feature-tag", type=click.STRING, required=True, help="Tag to visualize"
)
def project_visualization(feature_tag: str) -> None:
    """
    Visualizes an existing project

    :param feature_tag:
    :return:
    """
    StyleVisualization.swarmplot(feature_tag)
