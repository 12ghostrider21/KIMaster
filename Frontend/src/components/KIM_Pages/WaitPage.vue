<template>
    <div class="about">
      <h1>Waiting until Lobby is created...</h1>
      
    </div>
    <div>
    <select v-model="positionSelect" @change="swapPositionInLobby">
            <option value="p1">Player 1</option>
            <option value="p2">Player 2</option>
            <option value="sp">Spectator</option>
    </select>
    <select v-model="game">
            <option value="othello">Othello</option>
            <option value="connect4">Connect 4</option>
            <option value="Something else">Something else</option>
    </select>
    </div>
  </template>
  
<script>
import { mapActions, mapGetters } from 'vuex';
import * as ENUMS from '../enums';
export default {
  data() {
    return {
      positionSelect:"p1",
      game: ENUMS.games.OTHELLO,
      difficulty:'hard',
    };
  },
  computed: {
    ...mapGetters([ 'gameActive','position']),
  },

  mounted() {
  },
methods: {

    
  ...mapActions(['initWebSocket', 'sendWebSocketMessage',]),
  sendMessage(data) {
      console.log(data);
      this.sendWebSocketMessage(JSON.stringify(data));
  
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