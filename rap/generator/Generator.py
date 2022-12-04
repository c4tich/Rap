import os
import markovify

from rap import BASE_PATH


def print_song(path):

    with open(path) as f:
        text = f.read()
    # Build the model.
    text_model = markovify.Text(text)

    # Print five randomly-generated sentences
    for i in range(5):
        print(text_model.make_sentence())


def generar_cancion(estilo, cantante=""):

    base_path = os.path.join(BASE_PATH, "resources/letra_canciones", estilo)
    singer_path = os.path.join(base_path, f"{cantante}.txt")

    if cantante == "":
        temp_path = os.path.join(base_path, estilo, "temp.txt")
        with open(temp_path, "a") as fileEnd:
            for file in os.listdir(base_path):
                with open(os.path.join(base_path, file), "r") as fileRead:
                    illo = fileRead.read()
                    fileEnd.write(illo)

        print_song(temp_path)
    else:
        print_song(singer_path)
