<template>
    <div class="about">
      <h1>Waiting until Lobby is created...</h1>
      <select v-model="positionSelect" @change="swapPositionInLobby">
            <option value="p1">Player 1</option>
            <option value="p2">Player 2</option>
            <option value="sp">Spectator</option>
    </select>
      
    </div>
    <div>
    
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
    ...mapGetters([ 'gameActive','position','game','callPos']),

    positionSelect: {
      get() {
        return this.position;
      },
      set(value) {
        this.updatePosition(value);
      }
    }
  },

  mounted() {
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
swapPositionInLobby() {
  const data = {
    command: 'lobby',
    command_key: 'swap',
    pos: this.positionSelect
  };
  this.sendMessage(data);
},

goToGame() {
  console.log("GAME:" + this.game);
 

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