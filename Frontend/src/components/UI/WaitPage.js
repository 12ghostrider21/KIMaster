import { mapActions, mapGetters } from 'vuex';
import * as ENUMS from '../enums';

/**
 * Vue component logic for managing the Wait Page. 
 * @module Waitpage
 * 
 * @vue-computed {Object} ...mapGetters- Vuex getters mapped to component computed properties.
 * @vue-computed {string} positionSelect - Computed property for selecting the position. Provides getter and setter for the `position` value.
 * @vue-event {boolean} gameActive - Watches for changes in the `gameActive` value and redirects to the game page when a game starts.
 * @vue-event {void} callPos - Watches for changes in the `callPos` value and updates the lobby status if there are potential changes.
 */
export default {
  data() {

  },
  computed: {
    /**
     * Vuex getters mapped to component computed properties.
     * @type {Object}
     */
    ...mapGetters(['gameActive', 'position', 'game', 'callPos', 'positionsInLobby']),

    /**
     * Computed property for selecting the position.
     * Provides getter and setter for the `position` value.
     * @type {'p1'|'p2'|'sp'}
     */
    positionSelect: {
      get() {
        return this.position;
      },
      set(value) {
        this.updatePosition(value);
      }
    }
  },
  beforeMount() {
    /**
     * Lifecycle hook called before the component is mounted.
     * Initializes the lobby position and status.
     */
    this.lobbyPos();
    this.lobbyStatus();
  },
  mounted() {
    /**
     * Lifecycle hook called after the component is mounted.
     * Redirects to the game page if the game is active.
     */
    if (this.gameActive) {
      this.goToGame();
    }
  },
  methods: {
    /**
     * Vuex actions mapped to component methods.
     * @type {Object}
     */
    ...mapActions(['initWebSocket', 'sendWebSocketMessage', 'updatePosition']),

    /**
     * Sends a message via WebSocket after converting it to a JSON string.
     * @param {Object} data - The data to send.
     */
    sendMessage(data) {
      console.log(data);
      this.sendWebSocketMessage(JSON.stringify(data));
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
     * Sends a message to swap the current position in the lobby.
     */
    swapPositionInLobby() {
      const data = {
        command: 'lobby',
        command_key: 'swap',
        pos: this.positionSelect
      };
      this.sendMessage(data);
    },

    /**
     * Navigates to the game page with the current game parameters.
     */
    goToGame() {
      this.$router.push({
        name: 'play',
        params: { game: this.game }
      });
    },
  },
  watch: {
    /**
     * Watches for changes in the `gameActive` value.
     * Redirects to the game page when a game has started starts.
     * @param {boolean} newVal - The new value of gameActive.
     */
    gameActive(newVal) {
      if (newVal) {
        this.goToGame();
      }
    },

    /**
     * Watches for changes in the `callPos` value.
     * Automatically updates the lobby Status if there are potential changes.
     * @param {Object} newVal - The new value of callPos.
     */
    callPos() {
      this.lobbyPos();
      this.lobbyStatus();
    },
  },
};
