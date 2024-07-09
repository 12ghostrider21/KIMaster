import { mapActions, mapGetters } from "vuex";
import * as ENUMS from '../enums';

export default {
  computed: {
    ...mapGetters([
      "imageSrc",
      "position",
      "game",
      "playerWon",
      "gameOver",
      "gameActive",
      "notif",
      "popup",
      "images",
      "turn",
      "invalidMoveObserver",
      "skipMove",
      "turn",
      "blunders",
      "yourTurn",
      "playerTurn",
     
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
        case 'tictactoe':
          return 'TicTacToeRules';
        case 'othello':
          return 'OthelloRules';
          case 'nim':
            return'NimRules';
          case 'checkers':
            return 'CheckersRules'
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
      savedPos:null,


    };
  },
  mounted() {
    switch (this.game) {
      case "chess":
        this.boardWidth = 8;
        this.boardHeight = 8;
        this.twoTurnGame = true;
        break;
      case "checkers":
        this.boardWidth = 8;
        this.boardHeight = 8;
        this.twoTurnGame = true;
        break;
      case "connect4":
        this.boardWidth = 7;
        this.boardHeight = 7;
        this.twoTurnGame = false;
        break;
      case "tictactoe":
        this.boardWidth = 3;
        this.boardHeight = 3;
        this.twoTurnGame = false;
        break;
      case "othello":
        this.boardWidth = 8;
        this.boardHeight = 8;
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

    ]),
    nimMove(pos){
      if (this.nimTest[0]==-1) this.nimTest[0]=pos;
       if (this.nimTest[0]==pos) {
        this.nimTest[1]+=1;
        this.nimTest[1]%=(this.nimTest[0]+1)*2;
        if (this.nimTest[1]==0) this.nimTest[1]=1
      }
     
      
    },
    invalidMoveHandling() { 
      if (this.savedPos!=null) { 
      this.playValidMoves(this.savedPos);
      this.fromPos=this.savedPos;
      this.turnSelect=false;}
      this.savedPos=null;

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

    blunder() {
      const data = {
        command: "play",
        command_key: "blunder",
        isFrontend: true,
      };
      this.sendMessage(data);
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
        command_key: "valid_moves",
        isFrontend:true,
      };
      this.sendMessage(data);
    },

    playValidMoves(fromPos) {
      const data = {
        command: "play",
        command_key: "valid_moves",
        fromPos: fromPos,
        isFrontend:true,
      };
      this.sendMessage(data);
    },

    playMakeMove() {
       
        let data;
        if (!this.twoTurnGame) {
          data = {
            command: "play",
            command_key: "make_move",
            move: this.toPos,
            isFrontend:true,
          };
        } else {
          data = {
            command: "play",
            command_key: "make_move",
            move: [this.fromPos, this.toPos],
            isFrontend:true
          };
        }
        this.sendMessage(data);
      
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
          this.savedPos=this.toPos;
          this.turnSelect = true;
          if(this.toPos!=this.fromPos){
          this.playMakeMove();}
        }
      } else {
        
          switch (this.game) {
           case ENUMS.games.NIM:
           this.nimMove(this.mouseY-1)
           break;
           case ENUMS.games.CONNECT4:
           this.toPos= this.mouseX-1;
           this.playMakeMove();
           
           break;
           default:
            this.toPos =this.mouseX + (this.boardHeight * this.mouseY - this.boardHeight - 1); 
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

    leaveGame() {
    const data2 = {
      command: "lobby",
      command_key: "leave"
          };
    this.sendMessage(data2);
    this.$router.push({
      name: "home"
    });},

    first(){    const data = {
        command: 'play',
        command_key: 'timeline',
        num: 0,
      };
      this.sendMessage(data);
    },
    step(){  const data = {
      command: 'play',
      command_key: 'step',
    };
    this.sendMessage(data);},
    unstep(){  const data = {
      command: 'play',
      command_key: 'unstep',
    };
    this.sendMessage(data);},

    last(){const data = {
      command: 'play',
      command_key: 'timeline',
      num: this.turn,
    };
    this.sendMessage(data);},

    jumpTimeLine(it){const data = {
      command: 'play',
      command_key: 'timeline',
      num: it,
    };
    this.sendMessage(data);},
    /*firstImage() {
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
    }*/
  },
  watch: {
    invalidMoveObserver(){
      if(this.twoTurnGame)this.invalidMoveHandling();
    },
    skipMove(newval){
      if(newval){
      const data = {
        command: "play",
        command_key: "make_move",
        move: 36,
      };
    
    this.sendMessage(data);}
  },
  },
}
