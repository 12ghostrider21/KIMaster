
import { mapActions, mapGetters } from 'vuex';
import * as ENUMS from '../enums';

export default {
  data() {
    return {
      difficulty: 'hard',
    };
  },
  computed: {
    ...mapGetters(['gameActive', 'position', 'game', 'callPos', 'positionsInLobby']),
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
    this.lobbyPos();
    this.lobbyStatus();
  },
  mounted() {
    if (this.gameActive) {
      this.goToGame();
    }
  },
  methods: {
    ...mapActions(['initWebSocket', 'sendWebSocketMessage', 'updatePosition']),
    sendMessage(data) {
      console.log(data);
      this.sendWebSocketMessage(JSON.stringify(data));
    },
    lobbyPos() {
      const data = {
        command: 'lobby',
        command_key: 'pos',
      };
      this.sendMessage(data);
    },
    lobbyStatus() {
      const data = {
        command: "lobby",
        command_key: "status",
      };
      this.sendMessage(data);
    },
    swapPositionInLobby() {
      const data = {
        command: 'lobby',
        command_key: 'swap',
        pos: this.positionSelect
      };
      this.sendMessage(data);
    },
    goToGame() {
      this.$router.push({
        name: 'play',
        params: { game: this.game }
      });
    },
  },
  watch: {
    gameActive(newVal) { /*once a Game has started automatically go the PlayPage */
      if (newVal) {
        this.goToGame();
      }
    },
    callPos(newVal) { /*Automatically update the current Lobby Status */
      this.lobbyPos();
      this.lobbyStatus();
    },
  },
};

