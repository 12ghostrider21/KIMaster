import { mapActions, mapGetters } from "vuex";
import * as ENUMS from '../enums';

export default {
  props: ["game"],
  computed: {
    ...mapGetters([
      "imageSrc",
      "position",
      "playerWon",
      "gameOver",
      "gameActive",
      "notif",
      "popup",
      "images",
      "currentImageIndex",
      "turn",
     
    ]),
    enums() {
      return ENUMS;
    },
    currentRuleComponent() {
      switch (this.game) {
        case 'chess':
          return 'ChessRules';
        case 'connect4':
          return 'Connect4Rules';
        case 'tic_tac_toe':
          return 'TicTacToeRules';
        case 'othello':
          return 'OthelloRules';
        default:
          return null;
      }
    }
  },
  data() {
    return {
      mouseX: null,
      mouseY: null,
      boardWidth: 0,
      boardHeight: 0,
      turnSelect: true,
      fromPos: null,
      toPos: null,
      undoNum: 1,
      timeLineNum: 0,
      validMoveInsteadOfMakeMove: null,
      twoTurnGame: null,
      hoveredCell: null,
      isRulesVisible: false,
      nimTest:[-1,0],
    };
  },
  mounted() {
    switch (this.game) {
      case "chess":
        this.boardWidth = 8;
        this.boardHeight = 8;
        this.twoTurnGame = true;
        break;
      case "connect4":
        this.boardWidth = 7;
        this.boardHeight = 7;
        this.twoTurnGame = false;
        break;
      case "tic_tac_toe":
        this.boardWidth = 3;
        this.boardHeight = 3;
        this.twoTurnGame = false;
        break;
      case "othello":
        this.boardWidth = 6;
        this.boardHeight = 6;
        this.twoTurnGame = false;
        break;
        case "nim":
          this.boardWidth = 1;
          this.boardHeight = 4;
          this.twoTurnGame = false;
          break;
    }
  },
  methods: {
    ...mapActions([
      "sendWebSocketMessage",
      "setNotif",
      "setPopup",
      "changePrevImage",
      "changeNextImage",
      "changeFirstImage",
      "changeLastImage"
    ]),
    nimMove(pos){
      if (this.nimTest[0]==-1) this.nimTest[0]=pos;
      if (this.nimTest[0]==pos) this.nimTest[1]+=1;
     
      
    },
    sendNimMove(){
      const data = { 
        command: 'play',
        command_key: 'make_move',
        move: this.nimTest,
      };
        this.sendMessage(data);
        this.nimTest=[-1,0];
        },
    sendMessage(data) {
      console.log(data);
      this.sendWebSocketMessage(JSON.stringify(data));
    },
    highlightCellOnHover(event) {
      const imageRect = this.$refs.imageRef.getBoundingClientRect();
      const mouseX = event.clientX - imageRect.left;
      const mouseY = event.clientY - imageRect.top;
      const cellX = Math.ceil(
        mouseX / (this.$refs.imageRef.offsetWidth / this.boardWidth)
      );
      const cellY = Math.ceil(
        mouseY / (this.$refs.imageRef.offsetHeight / this.boardHeight)
      );

      // Set the hovered cell coordinates
      this.hoveredCell = { x: cellX, y: cellY };
    },
    undoMove() {
      const data = {
        command: "play",
        command_key: "undo_move",
        num: 1
      };
      this.sendMessage(data);
    },
    newGame() {
      const data = {
        command: "play",
        command_key: "new_game"
      };
      this.sendMessage(data);
    },
    playValidMoves() {
      const data = {
        command: "play",
        command_key: "valid_moves"
      };
      this.sendMessage(data);
    },
    playValidMoves(fromPos) {
      const data = {
        command: "play",
        command_key: "valid_moves",
        fromPos: fromPos
      };
      this.sendMessage(data);
    },
    playMakeMove() {
      if (this.currentImageIndex === this.images.length - 1) {
        let data;
        if (!this.twoTurnGame) {
          data = {
            command: "play",
            command_key: "make_move",
            move: this.toPos
          };
        } else {
          data = {
            command: "play",
            command_key: "make_move",
            move: [this.fromPos, this.toPos]
          };
        }
        this.sendMessage(data);
      }
    },
    closePopup() {
      this.setPopup(null);
    },
    trackMousePosition(event) {
      this.mouseX = event.clientX;
      this.mouseY = event.clientY;
      const imageRect = this.$refs.imageRef.getBoundingClientRect();
      this.mouseX = this.mouseX - imageRect.left;
      this.mouseY = this.mouseY - imageRect.top;
      this.mouseX = Math.ceil(
        this.mouseX / (this.$refs.imageRef.offsetWidth / this.boardWidth)
      );
      this.mouseY = Math.ceil(
        this.mouseY / (this.$refs.imageRef.offsetHeight / this.boardHeight)
      );
      if (this.twoTurnGame) {
        if (this.turnSelect) {
          this.fromPos =
            this.mouseX +
            (this.boardHeight * this.mouseY - this.boardHeight - 1);
          this.turnSelect = false;
          this.playValidMoves(this.fromPos);
        } else {
          this.toPos =
            this.mouseX +
            (this.boardHeight * this.mouseY - this.boardHeight - 1);
          this.turnSelect = true;
          this.playMakeMove();
        }
      } else {
        this.toPos =
          this.mouseX + (this.boardHeight * this.mouseY - this.boardHeight - 1);
          switch (this.game) {
           case "nim":
           this.nimMove(this.mouseY-1)
           break;
           default: 
           this.playMakeMove();
           break;}
       
      }
    },
    surrenderGame() {
      const data = {
        command: "play",
        command_key: "surrender"
      };
      this.sendMessage(data);
    },
    quitGame() {
      console.log("VUE COMPONENT" + this.gameActive);
      if (this.gameActive !== true) {
        // Debug, real guard must be implemented
        const data = {
          command: "play",
          command_key: "quit"
        };
        this.sendMessage(data);
        const data2 = {
          command: "lobby",
          command_key: "leave"
        };
        this.sendMessage(data2);
        this.$router.push({
          name: "home"
        });
      } else {
        this.setNotif === ENUMS.notifStatus.SURRENDERFIRST;
      }
    },
    firstImage() {
      this.changeFirstImage();
    },
    prevImage() {
      this.changePrevImage();
    },
    nextImage() {
      this.changeNextImage();
    },
    lastImage() {
      this.changeLastImage();
    }
  }
};
