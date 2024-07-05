import { mapActions, mapGetters } from 'vuex';
import * as ENUMS from "@/components/enums.js";
import BaseDialog from "@/components/UI/BaseDialog.vue";

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
    ENUMS() {
      return ENUMS
    },
    ...mapGetters(['inLobby', 'popup', 'notif','gameActive','game','callPos']),
  },
  methods: {
    ...mapActions(['sendWebSocketMessage','setNotif','setGame']),
    sendMessage(data) {
      console.log(data);
      this.sendWebSocketMessage(JSON.stringify(data));
    },
    transformGameName(game) {
      return game.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    },
    joinLobbyStart() {
      const data = {
        command: 'lobby',
        command_key: 'join',
        key: this.lobbyKeyToJoin,
        pos: 'sp',
      };
      this.sendMessage(data);
      this.joinLobbyWait();
    },

    surrenderGame(){
      
      const data = {
        command: 'play',
        command_key: 'surrender',
      };
      this.sendMessage(data);
      this.closePopUp()
    },

    returnToGame(){
      this.closePopUp()
      this.$router.push({ name: 'play', params: { game: this.game }});
    },

    triggerPopUp(){
      this.popUpTrigger=true;
    },

    closePopUp(){
      console.log("Test");
      this.popUpTrigger=false;
    },
    lobbyPos(){
      const data = {
      command: 'lobby',
      command_key: 'pos',
    };
    this.
    sendMessage(data);
    },
    lobbyStatus() {
      const data = {
        command: "lobby",
        command_key: "status",
      };
      this.sendMessage(data);
    },

    joinLobbyWait() {
      console.log(this.inLobby);
      if (this.inLobby) {
        this.$router.push({
          name: 'wait',
        });
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
    callPos(){
      this.lobbyPos();
      this.lobbyStatus();
      console.log(this.positionsInLobby);
    },
    notif(newVal) {
      setTimeout(() => {
        this.setNotif(null);
      }, 5000);
    },
  },

      }