import ast
import importlib.util
import os
import sys
from Tools.Game_Config import Entry


class GameEnumMeta(type):
    def __str__(cls):
        # Rückgabe aller Attribute der Klasse außer speziellen Attributen und Methoden
        attributes = {k: v for k, v in cls.__dict__.items()
                      if not k.startswith('__')
                      and not isinstance(v, classmethod)
                      and not isinstance(v, staticmethod)}
        return str(attributes)

    def __repr__(cls):
        return cls.__str__()

    def __iter__(cls):
        # Iterieren über alle Attribute der Klasse außer speziellen Attributen und Methoden
        return (v for k, v in cls.__dict__.items()
                if not k.startswith('__')
                and not isinstance(v, classmethod)
                and not isinstance(v, staticmethod))

    def __get_classes(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read(), filename=file_path)
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        return classes

    def __dynamic_import_class(self, file_path, class_name):
        file_path = os.path.abspath(file_path)
        module_dir = os.path.dirname(file_path)
        if module_dir not in sys.path:
            sys.path.append(module_dir)
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, class_name, None)

    def __load_class(self, path: str, file_name: str, class_name: str):
        for dirpath, _, filenames in os.walk(path):
            for filename in filenames:
                if filename.lower() == file_name.lower():
                    for cl in self.__get_classes(os.path.join(dirpath, filename)):
                        if cl.lower() == class_name.lower():
                            return self.__dynamic_import_class(os.path.join(dirpath, filename), cl)
        return None

    def get_entries(self, directory: str) -> list[Entry]:
        games = next(os.walk(directory))
        entry_list = []
        for game in games[1]:
            game_path = os.path.join(games[0], game)
            game_path_keras = os.path.join(game_path, 'keras')
            game_path_pytorch = os.path.join(game_path, 'pytorch')
            game_class = self.__load_class(game_path, f"{game}Game.py", f"{game}Game")
            wrapper_class = None
            if os.path.exists(game_path_pytorch):
                wrapper_class = self.__load_class(game_path_pytorch, "NNet.py", "NNetWrapper")
            elif os.path.exists(game_path_keras):
                wrapper_class = self.__load_class(game_path_keras, "NNet.py", "NNetWrapper")
            if game_class and wrapper_class:
                entry_list.append(Entry(game, game_class, wrapper_class))
            else:
                raise FileNotFoundError(f"Game: {game} does not have a keras or pytorch module!")
        return entry_list


class GameEnum(metaclass=GameEnumMeta):
    @classmethod
    def add(cls, key: str, value: Entry) -> None:
        if not isinstance(value, Entry):
            raise TypeError(f"The value must be an instance of Entry, got {type(value).__name__}")
        setattr(cls, key.lower(), value)

    @classmethod
    def get(cls, game_name: str) -> Entry | None:
        for e in cls:
            if e.game_name.lower() == game_name.lower():
                return e
        return None

    @classmethod
    def update(cls, directory: str):
        for e in cls.get_entries(directory):
            cls.add(e.game_name, e)

