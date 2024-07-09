<template>
    <div class="about">
      <h1>{{ $t('message.waitMessage') }}</h1>
      <select v-model="positionSelect" @change="swapPositionInLobby">
            <option value="p1">{{ $t('message.player1') }}</option>
            <option value="p2">{{ $t('message.player2') }}</option>
            <option value="sp">{{ $t('message.spectator') }}</option>
    </select>
    <p>  {{ $t('message.your_position', { position:position }) }}</p>
    <p> {{ $t('message.lobby_position', { p1: positionsInLobby[0], p2: positionsInLobby[1], spectators: positionsInLobby[2] }) }}</p>
    </div>
    
  </template>
  
<script>
import { mapActions, mapGetters } from 'vuex';
import * as ENUMS from '../enums';
export default {


  data() {
    return {
      difficulty:'hard',
    };
  },
  computed: {
    ...mapGetters([ 'gameActive','position','game','callPos',"positionsInLobby"]),

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

  mounted(){
    if(this.gameActive) {this.goToGame();};
  },
methods: {

    
  ...mapActions(['initWebSocket', 'sendWebSocketMessage','updatePosition']),
  sendMessage(data) {
      console.log(data);
      this.sendWebSocketMessage(JSON.stringify(data));
  
  },
  lobbyPos(){
    const data = {
    command: 'lobby',
    command_key: 'pos',
  };
  this.sendMessage(data);
  },

  lobbyStatus(){ 
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
    gameActive(newVal) {
      if (newVal) {
        this.goToGame();
      }
    },
    callPos(newVal){
      this.lobbyPos();
      this.lobbyStatus();
    },
  },
};

</script>
  <style>
  @media (min-width: 1024px) {
    .about {
      min-height: 100vh;
      display: flex;
      align-items: center;
    }
  }
  </style>