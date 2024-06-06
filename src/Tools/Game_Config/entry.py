from dataclasses import dataclass


@dataclass
class Entry:
    game_name: str = None
    game_class: callable = None
    nnet_class: callable = None
    h5_folder: str = None
    h5_file_name: str = None
