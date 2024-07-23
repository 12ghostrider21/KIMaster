import { mapActions, mapGetters } from "vuex";
import * as ENUMS from '../enums';
import click1 from '@/assets/Audio/Click1.mp3';
import click2 from '@/assets/Audio/Click2.mp3';
import click3 from '@/assets/Audio/Click3.mp3';
import click4 from '@/assets/Audio/Click4.mp3';
import click5 from '@/assets/Audio/Click5.mp3';
import click6 from '@/assets/Audio/Click6.mp3';
import click7 from '@/assets/Audio/Click7.mp3';
/**
 * Vue component logic for Playing the game
 * @module PlayPage
 * 
 * @vue-data {boolean} [isPlaying=false] - Indicates if a sound is currently playing.
 * @vue-data {Array} [sounds] - Array of sound files for click sounds.
 * @vue-data {?number} [mouseX=null] - Current X-coordinate of the mouse.
 * @vue-data {?number} [mouseY=null] - Current Y-coordinate of the mouse.
 * @vue-data {number} [boardWidth=0] - Width of the game Board.
 * @vue-data {number} [boardHeight=0] - Height of the game board.
 * @vue-data {boolean} [turnSelect=true] - Indicates if the player is merely selecting a Piece as opposed to moving it.
 * @vue-data {?number} [fromPos=null] - Starting position of a move.
 * @vue-data {?number} [toPos=null] - Ending position of a move.
 * @vue-data {number} [undoNum=1] - Number of undo moves available.
 * @vue-data {number} [timeLineNum=0] - Current timeline number for moves.
 * @vue-data {?number} [validMoveInsteadOfMakeMove=null] - Valid move position instead of make move.
 * @vue-data {?boolean} [twoTurnGame=null] - Indicates if the game requires two turns for a move.
 * @vue-data {?{x: number, y: number}} [hoveredCell=null] - Coordinates of the cell currently hovered by the mouse.
 * @vue-data {boolean} [isRulesVisible=false] - Indicates if the rules are currently visible.
 * @vue-data {number[]} [nimTest=[-1,0]] - Array for the Nim game.
 * @vue-data {?number} [savedPos=null] - Saved position for invalid move handling.
 * 
 *  @vue-computed {Object} ...mapGetters - Vuex getters mapped to component computed properties.
 * @vue-computed {Object} enums - Enumeration constants imported from the ENUMS module.
 * @vue-computed {string} currentRuleComponent - Determines the component to render based on the current game.
 */
export default {
  computed: {
    /**
     * Vuex getters mapped to component computed properties.
     */
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
      "playSound",
    ]),

    /**
     * Enumeration constants imported from the ENUMS module.
     * @type {Object}
     */
    enums() {
      return ENUMS;
    },

    /**
     * Determines the component to render based on the current game.
     * @type {string}
     */
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
          return 'NimRules';
        case 'checkers':
          return 'CheckersRules';
        default:
          return null;
      }
    }
  },

  data() {
    return {
      isPlaying: false,
      sounds: [click1, click2, click3, click4, click5, click6, click7],
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
      nimTest: [-1, 0],
      savedPos: null,
  };
  
  },

  mounted() {
    /**
     * Initializes game board dimensions and settings based on the current game.
     */
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
    /**
     * Vuex actions mapped to component methods.
     */
    ...mapActions([
      "sendWebSocketMessage",
      "setNotif",
      "setPopup",
    ]),

    /**
     * Handles a move in the Nim game.
     * @param {number} pos - The position of the move.
     */
    nimMove(pos) {
      if (this.nimTest[0] == -1) this.nimTest[0] = pos;
      if (this.nimTest[0] == pos) {
        this.nimTest[1] += 1;
        this.nimTest[1] %= (this.nimTest[0] + 1) * 2;
        if (this.nimTest[1] == 0) this.nimTest[1] = 1;
      }
    },

    /**
     * Automatically plays valid move from the saved Position when an invalid move was made.
     * Ensures smooth User Experience
     */
    invalidMoveHandling() {
      if (this.savedPos != null) {
        this.playValidMoves(this.savedPos);
        this.fromPos = this.savedPos;
        this.turnSelect = false;
      }
      this.savedPos = null;
    },

    /**
     * Sends the current Nim move.
     */
    sendNimMove() {
      const data = {
        command: 'play',
        command_key: 'make_move',
        move: this.nimTest,
      };
      this.sendMessage(data);
      this.nimTest = [-1, 0];
    },

    /**
     * Sends a message through the WebSocket.
     * @param {Object} data - The data to send.
     */
    sendMessage(data) {
      console.log(data);
      this.sendWebSocketMessage(JSON.stringify(data));
    },

    /**
     * Highlights a cell on the game board based on mouse hover.
     * @param {MouseEvent} event - The mouse event.
     */
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

    /**
     * Requests the blundered Moves from Backend.
     */
    blunder() {
      const data = {
        command: "play",
        command_key: "blunder",
        isFrontend: true,
      };
      this.sendMessage(data);
    },

    /**
     * Requests to undo the last move.
     */
    undoMove() {
      const data = {
        command: "play",
        command_key: "undo_move",
        num: 1
      };
      this.sendMessage(data);
    },

    /**
     * Starts a new game with the same set up.
     */
    newGame() {
      const data = {
        command: "play",
        command_key: "new_game"
      };
      this.sendMessage(data);
    },

    /**
     * Requests valid moves for the current game state.
     * @param {?number} fromPos - Selected Piece for which to call Valid Moves.
     */
    playValidMoves(fromPos) {
      const data = {
        command: "play",
        command_key: "valid_moves",
        fromPos: fromPos,
        isFrontend: true,
      };
      this.sendMessage(data);
    },

    /**
     * Executes the move depending on wether it's a two turn game or a one turn game.
     */
    playMakeMove() {
      let data;
      if (!this.twoTurnGame) {
        data = {
          command: "play",
          command_key: "make_move",
          move: this.toPos,
          isFrontend: true,
        };
      } else {
        data = {
          command: "play",
          command_key: "make_move",
          move: [this.fromPos, this.toPos],
          isFrontend: true
        };
      }
      this.sendMessage(data);
    },

    /**
     * Closes the current popup.
     */
    closePopup() {
      this.setPopup(null);
    },

    /**
     * Tracks the mouse position on the game board.
     * @param {MouseEvent} event - The mouse event.
     */
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
          this.savedPos = this.toPos;
          this.turnSelect = true;
          if (this.toPos != this.fromPos) {
            this.playMakeMove();
          }
        }
      } else {
        switch (this.game) {
          case ENUMS.games.NIM:
            this.nimMove(this.mouseY - 1);
            break;
          case ENUMS.games.CONNECT4:
            this.toPos = this.mouseX - 1;
            this.playMakeMove();
            break;
          default:
            this.toPos = this.mouseX + (this.boardHeight * this.mouseY - this.boardHeight - 1);
            this.playMakeMove();
            break;
        }
      }
    },

    /**
     * Sends a surrender command for the game.
     */
    surrenderGame() {
      const data = {
        command: "play",
        command_key: "surrender"
      };
      this.sendMessage(data);
    },

    /**
     * Quits the current game or returns to the home page.
     */
    quitGame() {
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

    /**
     * Leaves the game and returns to the home page.
     */
    leaveGame() {
      const data2 = {
        command: "lobby",
        command_key: "leave"
      };
      this.sendMessage(data2);
      this.$router.push({
        name: "home"
      });
    },

    /**
     * Moves to the first state in the timeline.
     */
    first() {
      const data = {
        command: 'play',
        command_key: 'timeline',
        num: 0,
      };
      this.sendMessage(data);
    },

    /**
     * Moves to the next state in the timeline.
     */
    step() {
      const data = {
        command: 'play',
        command_key: 'step',
      };
      this.sendMessage(data);
    },

    /**
     * Moves to the previous state in the timeline.
     */
    unstep() {
      const data = {
        command: 'play',
        command_key: 'unstep',
      };
      this.sendMessage(data);
    },

    /**
     * Moves to the last state in the timeline.
     */
    last() {
      const data = {
        command: 'play',
        command_key: 'timeline',
        num: this.turn,
      };
      this.sendMessage(data);
    },

    /**
     * Jumps to a specific state in the timeline.
     * @param {number} it - The timeline number to jump to.
     */
    jumpTimeLine(it) {
      const data = {
        command: 'play',
        command_key: 'timeline',
        num: it,
      };
      this.sendMessage(data);
    },

    /**
     * Navigates back to the lobby.
     */
    returnLobby() {
      this.$router.push({
        name: 'lobby',
      });
    },

    /**
     * Plays a random sound effect.
     */
    playRandomSound() {
      if (this.game === 'Nim') {
        return; // Disabling sound when playing Nim
      }
      this.isPlaying = true;
      const randomIndex = Math.floor(Math.random() * this.sounds.length);
      const audio = new Audio(this.sounds[randomIndex]);
      audio.play();

      setTimeout(() => {
        this.isPlaying = false;
      }, 100); // 100 milliseconds delay so sounds don't overlap too strongly
    },
  },

  watch: {
    /**
     * Watches for changes in the invalidMoveObserver property.
     * Automatically handles invalid moves if necessary.
     */
    invalidMoveObserver() {
      if (this.twoTurnGame) this.invalidMoveHandling();
    },

    /**
     *Plays a Sound at the correct time.
     */
    playSound() {
      this.playRandomSound();
    },

    /**
     * Watches for changes in the skipMove property.
     * Handles special cases to skip a move if required.
     * @param {boolean} newval - The new value of skipMove.
     */
    skipMove(newval) {
      if (newval) {
        const data = {
          command: "play",
          command_key: "make_move",
          move: 64,
        };
        this.sendMessage(data);
      }
    },
  },
}
