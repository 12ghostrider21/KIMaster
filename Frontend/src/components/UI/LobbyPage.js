import { mapActions, mapGetters } from "vuex";
import * as ENUMS from '../enums';
import QRCode from 'qrcode';
import { nextTick } from 'vue';
export default {

 
  data() {
    return {
      mode: "player_vs_kim",
      difficulty: "easy",
      selectedGame: '',
      test:[false,true],
      
    };
  },
  computed: {
    ...mapGetters(["lobbyKey", "position","gameActive","positionsInLobby","callPos",'game','socketConnected','popup']),
    enums() {return ENUMS},
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
    if(this.lobbyKey === null){
    this.createLobby();
    this.selectedGame=this.game;}
  },

  methods: {
    ...mapActions(["initWebSocket", "sendWebSocketMessage","setGame","updatePosition",'setPopup']),
    sendMessage(data) {
      //if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      console.log(data);
      this.sendWebSocketMessage(JSON.stringify(data));
      /*} else {
      console.error('WebSocket connection is not open.');
    }*/
    },
    transformGameName(game) {
      return this.$t(`message.${game}`);
    },
    lobbyPos(){
      const data = {
      command: 'lobby',
      command_key: 'pos',
    };
    this.sendMessage(data);
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
      this.$router.push({
        name: 'home',
      });
    },

    closePopup() {
      this.setPopup(null);
    },
    
    swapPositionInLobby() {
      const data = {
        command: "lobby",
        command_key: "swap",
        pos: this.positionSelect,
      };
      this.sendMessage(data);
    },

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

    showPos() {
      const data = {
        command: "lobby",
        command_key: "pos",
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

    playCreate() {
      this.lobbyStatus();
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
        if(this.gameActive) 
        this.$router.push({
          name: 'play'
        }); }
     
    },
  },
  watch: {
    game(){
      this.selectedGame=this.game;
    },
    callPos(){
      this.lobbyPos();
      this.lobbyStatus();
      console.log(this.positionsInLobby);
    },
   gameActive(newVal) {
        if (newVal) {
          this.$router.push({
            name: 'play',
          });
        }
      },
      socketConnected(newVal){if
        (newVal) {
          this.createLobby();
        }
      }
   
  },
};