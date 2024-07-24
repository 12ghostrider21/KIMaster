import { mapActions, mapGetters } from "vuex";
import * as ENUMS from '../enums';
import QRCode from 'qrcode';
import { nextTick } from 'vue';
/**
 * Vue component for managing the Lobby.
 * @module LobbyPage 
 * @vue-data {String} [mode=player_vs_kim] - Mode of the game, which can be "player_vs_player", "player_vs_kim", "playerai_vs_kim", or "playerai_vs_player".
 * @vue-data {String} [difficulty=easy] - Difficulty level of the game, which can be "easy", "medium", or "hard".
 * @vue-data {String} selectedGame - Identifier of the selected game
 * 
 * @vue-computed {Object} enums - Provides enums imported from '../enums.js'.
 * @vue-computed {String} positionSelect - Current position in the lobby, with a getter and setter for updating the position.
 *  * @vue-computed {Object} ...mapGetters - Vuex getters mapped to component computed properties.
 * 
 * @vue-methods {Function} transformGameName - Transforms the game name for display using a translation function.
 * @vue-methods {Function} generateQrCode - Generates a QR code for the lobby key.
 * @vue-methods {Function} lobbyPos - Requests the current lobby positions.
 * 
 * @vue-event {String} game - Updates the selected game when the game is changed via Vuex.
 * @vue-event {Object} callPos - Automatically updates the lobby status if there are potential changes.
 * @vue-event {Boolean} gameActive - Redirects to the play page once a game has started.
 */

export default {
  /**
   * Component data.
   * @returns {Object} The component's data object.
   */
  data() {
    return {

      mode: "player_vs_kim",

      difficulty: "easy",

      selectedGame: '',
    };
  },

  computed: {
    /**
     * Vuex getters required for the Lobby
     * @type {Object}
     */
    ...mapGetters(["notif","lobbyKey", "position", "gameActive", "positionsInLobby", "callPos", "game", "socketConnected", "popup", "gameReady"]),

    /**
     * Enums imported from '../enums.js'.
     * @type {Object}
     */
    enums() { return ENUMS; },

    /**
     * Current position in the lobby.
     * @type {"p1"|"p2"|"sp"}
     */
    positionSelect: {
      get() {
        return this.position;
      },
      set(value) {
        this.updatePosition(value);
      },
    },
  },

  mounted() {
    /**
     * Lifecycle hook called after the component is mounted.
     * If `lobbyKey` is null, creates a new lobby and sets the selected game.
     */
    if (this.lobbyKey === null) {
      this.createLobby();
      this.selectedGame = this.game;
    }
  },

  methods: {
    /**
     * Vuex actions mapped to component methods.
     * @type {Object}
     */
    ...mapActions(["initWebSocket", "sendWebSocketMessage", "setGame", "updatePosition", "setPopup",'setNotif',]),

    /**
     * Sends a message through the WebSocket.
     * @param {Object} data - The data to send.
     */
    sendMessage(data) {
      console.log(data);
      this.sendWebSocketMessage(JSON.stringify(data));
    },

    /**
     * Transforms the game name for display.
     * @param {string} game - The game identifier.
     * @returns {string} - The transformed game name.
     */
    transformGameName(game) {
      return this.$t(`message.${game}`);
    },

    /**
     * Requests the current lobby positions.
     */
    lobbyPos() {
      const data = {
        command: 'lobby',
        command_key: 'pos',
      };
      this.sendMessage(data);
    },

    /**
     * Creates a new lobby.
     */
    createLobby() {
      const data = {
        command: "lobby",
        command_key: "create",
      };
      this.sendMessage(data);
    },

    /**
     * Leaves the current lobby and redirects to the home page.
     */
    leaveLobby() {
      const data = {
        command: "lobby",
        command_key: "leave",
      };
      this.sendMessage(data);
      this.$router.push({
        name: 'home',
      });
    },

    /**
     * Closes the popup.
     */
    closePopup() {
      this.setPopup(null);
    },

    /**
     * Swaps the position of the player in the lobby.
     */
    swapPositionInLobby() {
      const data = {
        command: "lobby",
        command_key: "swap",
        pos: this.positionSelect,
      };
      this.sendMessage(data);
    },

    /**
     * Generates a QR code for the lobby key.
     * @async
     * @returns {Promise<void>}
     */
    async generateQrCode() {
      await nextTick(); // Ensure the DOM updates are done
      const canvas = this.$refs.qrcodeCanvas;
      if (this.lobbyKey) {
        try {
          await QRCode.toCanvas(canvas, this.lobbyKey);
          console.log('QR code generated!');
        } catch (error) {
          console.error('Failed to generate QR code:', error);
        }
      }
    },

    /**
     * Requests the current position in the Lobby
     */
    showPos() {
      const data = {
        command: "lobby",
        command_key: "pos",
      };
      this.sendMessage(data);
    },

    /**
     * Requests the status of the lobby.
     */
    lobbyStatus() {
      const data = {
        command: "lobby",
        command_key: "status",
      };
      this.sendMessage(data);
    },

    /**
     * Starts the game if the position is valid and the game is ready.
     * Checks which position is currently occupied by the user to selecte the proper gamemode
     * Checks whether a GameClient is connected to the Lobby.
     * Retries if the game is not ready.
     */
    playCreate() {
      this.lobbyStatus();
      if (this.gameReady && this.position === 'p1') {
        const data = {
          command: 'play',
          command_key: 'create',
          game: this.game,
          mode: this.mode,
          difficulty: this.difficulty,
        };
        this.setGame(this.game);
        this.sendMessage(data);
        if (this.gameActive) {
          this.$router.push({
            name: 'play'
          });
        }
      } else if (this.gameReady) {
        const data = {
          command: 'play',
          command_key: 'create',
          game: this.game,
          mode: this.mode === 'player_vs_kim' ? 'kim_vs_player' :
            this.mode === 'playerai_vs_kim' ? 'kim_vs_playerai' : this.mode,
          difficulty: this.difficulty,
        };
        this.setGame(this.game);
        this.sendMessage(data);
        if (this.gameActive) {
          this.$router.push({
            name: 'play'
          });
        }
      } else {
        setTimeout(() => {
          this.playCreate();
        }, 1000);
      }
    },
  },

  watch: {
    /**
     * Updates the selected game when the game is changed via Vuex
     * @param {string} newGame - The new game identifier.
     */
    game(newGame) {
      this.selectedGame = newGame;
    },

    /**
     * Automatically updates the lobby Status if there are potential changes.
     */
    callPos() {
      this.lobbyPos();
      this.lobbyStatus();
      console.log(this.positionsInLobby);
    },

    /**
     * Redirects to the play page once a game has started.
     * @param {boolean} newVal - The new value indicating if the game is active.
     */
    gameActive(newVal) {
      if (newVal) {
        this.$router.push({
          name: 'play',
        });
      }
    },
        /**
     * Displays notification when needed and clears them after a delay.
     * @param {string|null} newVal - The new value of notif.
     */
        notif(newVal) {
          if (newVal) {
            setTimeout(() => {
              this.setNotif(null);
            }, 5000);
          }
        },
  },
};
