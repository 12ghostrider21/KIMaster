class Path:
    @staticmethod
    def get_path(game: str):
        match game:
            case "connect4":
                return "./pretrained_models/connect4max/", "best.h5"
            case "ttt":
                pass
            case "othello":
                pass
            case "nim":
                pass
            case "checkers":
                pass
            case "go":
                pass
            case "waldmeister":
                pass
