from dataclasses import dataclass


@dataclass
class Entry:
    game_name: str = None
    game_class: callable = None
    nnet_class: callable = None
