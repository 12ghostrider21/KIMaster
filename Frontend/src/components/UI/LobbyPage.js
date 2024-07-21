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
    ...mapGetters(["lobbyKey", "position","gameActive","positionsInLobby","callPos",'game','socketConnected','popup','gameReady']),
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
      console.log(data);
      this.sendWebSocketMessage(JSON.stringify(data));
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

    playCreate() { /*Checks what position is currently occupied to decide which Command to send. Also tests wether a GameClient is connected to the Lobby so play Create actually works */
      this.lobbyStatus();
      if (this.gameReady&&this.position==='p1') {
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
        else if (this.gameReady){
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
          if(this.gameActive) 
          this.$router.push({
            name: 'play'
          }); 
          
        }
        else {
          setTimeout(() => {
            this.playCreate();
          }, 1000);}
     
    },
  },
  watch: {
    game(){
      this.selectedGame=this.game;
    },
    callPos(){ /*Automatically update the current Status of the Lobby */
      this.lobbyPos();
      this.lobbyStatus();
      console.log(this.positionsInLobby);
    },
   gameActive(newVal) { /*once a Game has started automatically go the PlayPage */
        if (newVal) {
          this.$router.push({
            name: 'play',
          });
        }
      },
   
  },
};