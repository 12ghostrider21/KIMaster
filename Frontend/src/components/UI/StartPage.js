import { mapActions, mapGetters } from 'vuex';
import * as ENUMS from "@/components/enums.js";
import BaseDialog from "@/components/UI/BaseDialog.vue";

/**
 * Vue component for handling the logic of the StartPage.
 * Includes methods for interacting with the game lobby and handling UI state.
 * @module StartPage 
 * @vue-prop {string} title - The title to display in the component.
 * @vue-data {Array} games - List of available games from ENUMS.
 * @vue-data {string|null} lobbyKeyToJoin - Key for joining a lobby.
 * @vue-data {boolean} popUpTrigger - Flag to trigger the popup dialog.
 * @vue-computed {Object} ENUMS - Returns the ENUMS object.
 * @vue-computed {Object} ...mapGetters - Vuex getters mapped to component computed properties.
 * @vue-event {void} joinLobbyWait - Polls for the lobby status and navigates to the waiting page if the lobby is joined.
 * @vue-event {void} callPos - Automatically updates the lobby status if there are potential changes.
 * @vue-event {void} notif - Displays notification when needed and clears them after a delay.
 */
export default {
  components: {
    BaseDialog,
  },
  data() {
    return {

      games: ENUMS.games,

      lobbyKeyToJoin: null,


      popUpTrigger: false,
    };
  },
  computed: {
    /**
     * Returns the ENUMS object.
     * @returns {Object}
     */
    ENUMS() {
      return ENUMS;
    },

    /**
     * Vuex getters mapped to component computed properties.
     * @type {Object}
     */
    ...mapGetters(['inLobby', 'popup', 'notif', 'gameActive', 'game', 'callPos']),
  },
  methods: {
    /**
     * Vuex actions mapped to component methods.
     * @type {Object}
     */
    ...mapActions(['sendWebSocketMessage', 'setNotif', 'setGame']),

    /**
     * Sends a message via WebSocket.
     * @param {Object} data - The data to send.
     */
    sendMessage(data) {
      console.log(data);
      this.sendWebSocketMessage(JSON.stringify(data));
    },

    /**
     * Transforms a game name by replacing underscores with spaces and capitalizing each word.
     * @param {string} game - The game name to transform.
     * @returns {string} - The transformed game name.
     */
    transformGameName(game) {
      return game.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    },

    /**
     * Starts the process of joining a lobby.
     * Sends a message to join the lobby and waits for confirmation.
     */
    joinLobbyStart() {
      if (!this.lobbyKeyToJoin) return; // Avoid sending request with empty key

      const data = {
        command: 'lobby',
        command_key: 'join',
        key: this.lobbyKeyToJoin.trim(),
        pos: 'sp',
      };
      this.sendMessage(data);
      this.joinLobbyWait();
    },

    /**
     * Sends a message to surrender the current game and closes the popup.
     * Usable when you're in an active game and you try to join a new Lobby
     */
    surrenderGame() {
      const data = {
        command: 'play',
        command_key: 'surrender',
      };
      this.sendMessage(data);
      this.closePopUp();
    },

    /**
     * Navigates back to the game page when double clicking on the game board
     */
    returnToGame() {
      this.closePopUp();
      this.$router.push({ name: 'play', params: { game: this.game }});
    },

    /**
     * Triggers the display of the popup dialog.
     */
    triggerPopUp() {
      this.popUpTrigger = true;
    },

    /**
     * Closes the popup dialog.
     */
    closePopUp() {
      console.log("Popup closed");
      this.popUpTrigger = false;
    },

    /**
     * Sends a message to get the current position in the lobby.
     */
    lobbyPos() {
      const data = {
        command: 'lobby',
        command_key: 'pos',
      };
      this.sendMessage(data);
    },

    /**
     * Sends a message to get the current status of the lobby.
     */
    lobbyStatus() {
      const data = {
        command: "lobby",
        command_key: "status",
      };
      this.sendMessage(data);
    },

    /**
     * Polls for the lobby status and navigates to the waiting page if the lobby is joined.
     * Retries if the lobby join fails.
     */
    joinLobbyWait() {
      console.log(this.inLobby);
      if (this.inLobby) {
        this.$router.push({ name: 'wait' });
      } else if (this.notif === ENUMS.notifStatus.LOBBYJOINFAIL) {
        console.log("Couldn't Find Lobby!");
      } else {
        setTimeout(() => {
          this.joinLobbyWait();
        }, 1000);
      }
    },
  },
  watch: {
    /**
     * Automatically updates the lobby Status if there are potential changes.
     * @param {Object} newVal - The new value of callPos.
     */
    callPos(newVal) {
      this.lobbyPos();
      this.lobbyStatus();
      console.log(this.positionsInLobby); // Ensure positionsInLobby is defined if used
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
