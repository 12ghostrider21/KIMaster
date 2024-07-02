import { mapActions, mapGetters } from "vuex";
import * as ENUMS from '../enums';
export default {

  props: ["game"],
  data() {
    return {
      positionSelect: "p1",
      mode: "player_vs_kim",
      difficulty: "easy",
      selectedGame: this.game,
    };
  },
  computed: {
    ...mapGetters(["lobbyKey", "position","gameReady"]),
    enums() {return ENUMS},
  },
  mounted() {
    if(this.lobbyKey === null){
    this.createLobby();}
  },

  methods: {
    ...mapActions(["initWebSocket", "sendWebSocketMessage","setGame"]),
    sendMessage(data) {
      //if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      console.log(data);
      this.sendWebSocketMessage(JSON.stringify(data));
      /*} else {
      console.error('WebSocket connection is not open.');
    }*/
    },
    transformGameName(game) {
      return game.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    },
    createLobby() {
      const data = {
        command: "lobby",
        command_key: "create",
      };
      this.sendMessage(data);
    },

    leaveLobby() {
      const data = {
        command: "lobby",
        command_key: "leave",
      };
      this.sendMessage(data);
      this.$router.push("/");
    },
    navigateToGame(){  this.$router.push({
          name: 'lobby',
          params: { game: this.selectedGame }})
         },

    swapPositionInLobby() {
      const data = {
        command: "lobby",
        command_key: "swap",
        pos: this.positionSelect,
      };
      this.sendMessage(data);
    },

    showPos() {
      const data = {
        command: "lobby",
        command_key: "pos",
      };
      this.sendMessage(data);
    },

    showLobbyList() {
      const data = {
        command: "lobby",
        command_key: "status",
      };
      this.sendMessage(data);
    },

    showStatus() {
      const data = {
        command: 'lobby',
        command_key: 'status',
      };
      this.sendMessage(data);
    },
    playCreate() {
      this.showStatus();
      if (true) {
        const data = {
          command: 'play',
          command_key: 'create',
          game: this.game,
          mode: this.mode,
          difficulty: this.difficulty,
        };
        this.setGame(this.game);
        this.sendMessage(data);

        this.$router.push({
          name: 'play',
          params: { game: this.game }
        }); }
      else {
        setTimeout(() => {
          this.playCreate();
        }, 1000);
      }
    },
  },
  watch: {
    position(newVal) {
      this.positionSelect = newVal;
    },
  },
};