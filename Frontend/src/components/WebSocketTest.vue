<template>
  <div id="app">
    <div class="box">
      <div class="grid-section">
        Lobby:
        <button @click="createLobby">Create Lobby</button>
        <input type="text" v-model="lobbyKey" placeholder="Enter Lobby Key">
       
        <br>
        
        <label for="joinLobbyPosition">Join as:</label>
    <select id="joinLobbyPosition" v-model="joinLobbyPosition">
        <option value="p1">Player 1</option>
        <option value="p2">Player 2</option>
        <option value="sp">Spectator</option>
        <option value=null>null</option>
    </select>
    <button @click="joinLobby">Join Lobby</button>
        <br>
        <button @click="leaveLobby">Leave Lobby</button>
        <select v-model="position" @change="swapPositionInLobby">
          <option value="p1">Player 1</option>
          <option value="p2">Player 2</option>
          <option value="sp">Spectator</option>
          <option value="sp">Spectator</option>
        </select>
        <br>
        <button @click="showPos">Lobby Pos</button>
        <button @click="showLobbyList">Lobby Status</button>
        <h1>WebSocket Connection Status: {{ connectionStatus }}</h1>
      </div>
    </div>

    <div class="box">
      <div class="grid-section">
        Play:
        <select v-model="game" >
          <option value='connect4'>Vier Gewinnt</option>
          <option value="tictactoe">Tic Tac Toe</option>
          <option value="othello">Othello</option>
        </select>
        <select v-model="mode">
          <option value="player_vs_player">Player vs Player</option>
          <option value='player_vs_ai'>Player vs Ai</option>
          <option value="playerai_vs_ai">Player Ai vs Ai</option>
          <option value="playerai_vs_playerai">Player Ai vs Player Ai</option>
        </select>
        <select v-model="difficulty" >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value='hard'>Hard</option>
        </select>
        <button @click="playCreate">Create </button>
        <br>
        <label for="widthInput">Grid Width:</label>
        <input type="number" id="widthInput" v-model="boardWidth" min="1" step="1">
        <br>
        <label for="heightInput">Grid Height:</label>
        <input type="number" id="heightInput" v-model="boardHeight"  min="1" step="1">
        <br>
        <label for="undoNum">Undo this Number of turns:</label>
        <input type="number" id="undoNum" v-model="undoNum"  min="1" step="1">
        <button @click="playUndoMove">Undo Moves</button>
        <button @click="playSurrender">Surrender</button>
        <button @click="playNewGame">New Game</button>
        <button @click="playBlunder">Blunder</button>
        <button @click="playTimeLine">TimeLine</button>
        <button @click="playStep">Step</button>
        <button @click="playUnstep">Unstep</button>
        <br>
        <input type="number" id="evaluateNum" v-model="evaluateNum"  min="1" step="1">
        <button @click="playEvaluate">Evaluate</button>
        <br>
        <label for="moveSwitch">Valid Moves Instead of Make Move:</label>
        <input type="checkbox" id="moveSwitch" v-model="validMoveInsteadOfMakeMove">
        <br>
        <label for="twoTurnGame">Activate two turn Game (fromPos-> toPos):</label>
        <input type="checkbox" id="twoTurnGame" v-model="twoTurnGame">
        <br>
      </div>
    </div>

    <div class="box">
  <div class="grid-section" style="position: relative;">
    <img
      width="300"
      height="300"
      class="imageRef"
      ref="imageRef"
      v-if="imageSrc"
      :src="imageSrc"
      alt="Received Image"
      @click="trackMousePosition"
      @mousemove="highlightCellOnHover"
      style="display: block; margin: auto; position: relative;"
    />
    <div
      v-if="hoveredCell"
      class="highlight-cell"
      :style="{
        width: `${300 / boardWidth}px`,
        height: `${300 / boardHeight}px`,
        top: `${(hoveredCell.y - 1) * (300 / boardHeight)}px`,
        left: `${(hoveredCell.x - 1) * (300 / boardWidth)}px`
      }"
    ></div>
  </div>
</div>

    <div class="box limited-width-box">
      <div class="grid-section">
        <h2>Received From Server:</h2>
        <pre>{{ receivedJSONObject }}</pre>
      </div>
    </div>
  </div>
<div class="box">
  <div class="grid-section">
    <div style="display: inline-block;">
     <label for="commandInUserJSON">command:</label>
     <input id="commandKeyInUserJSON" type="text" v-model="commandInUserJSON" placeholder="Enter Command">
    </div>
    <div style="display: inline-block;">
      <label for="commandKeyInUserJSON">command_key:</label>
      <input id="commandKeyInUserJSON" type="text" v-model="commandKeyInUserJSON" placeholder="Enter Command Key">
    </div>
  <h1>Key-Value Pair Input</h1>
  <div class="grid-section">
    <form @submit.prevent="addPair">
      <div>
        <label for="key">Key:</label>
        <input type="text" v-model="newKey" id="key" required />
      </div>
      <div>
        <label for="value">Value:</label>
        <input type="text" v-model="newValue" id="value" required />
      </div>
      <button type="submit">Add Pair</button>
      <br>
    </form>
    <h2>JSON Output</h2>
    <pre>{{ userSentJSON }}</pre>
    <button @click="sendUserSentJSON">Send</button>
  </div>
  </div>
  </div>
</template>
<script>

import imagePath from '../assets/tictactoe_board.png';

export default {
  data() {
    return {
      connectionStatus: 'Disconnected',
      socket: null,
      lobbyKey: null,
      position: null,
      joinLobbyPosition: null,
      receivedJSONObject: null,
      game:'connect4',
      mode:'player_vs_ai',
      difficulty:'hard',
      mouseX:null,
      mouseY:null,
      boardWidth:7,
      boardHeight:7,

      turnSelect:true,
      fromPos:null,
      toPos:null,
      undoNum:1,
      imageSrc:imagePath,
      timeLineNum:0,

      validMoveInsteadOfMakeMove:false,
      twoTurnGame:false,

      newKey: null,
      newValue:null,
      userSentJSON: {},
      commandInUserJSON:null,
      commandKeyInUserJSON:null,
      hoveredCell: null,
    };
  },
  methods: {

    connect() {
     
     const currentUrl = window.location.href;


if (currentUrl.startsWith('http://') && currentUrl.includes(':8086')) {

let modifiedUrl = currentUrl.replace('http://', 'ws://').replace(':8086', ':8010/ws');
if (modifiedUrl.endsWith('/')) {
      modifiedUrl = modifiedUrl.slice(0, -1);
    }


this.socket = new WebSocket(modifiedUrl);} //TODO change to proper adress, for now it's hacked together
else {this.socket = new WebSocket('ws://localhost:8010/ws');} //Static URL if adress not in the correct format


      this.socket.onopen = () => {
        this.connectionStatus = 'Connected';
      };

      this.socket.onclose = () => {
        this.connectionStatus = 'Disconnected';
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket error: ', error);
      };

      this.socket.onmessage = (event) => {
   
        try { this.receivedJSONObject=JSON.parse(event.data);
        if (this.receivedJSONObject.key!= null) {this.lobbyKey=this.receivedJSONObject.key;}
      } catch (e) {
        const blob = new Blob([event.data], { type: 'image/png' }); 
        const url = URL.createObjectURL(blob);
        this.imageSrc = url;
      }
       
      };
    },
    disconnect() {
      if (this.socket) {
        this.socket.close();
      }
    },
    sendMessage(data) {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        console.log(data);
        this.socket.send(JSON.stringify(data));
      } else {
        console.error('WebSocket connection is not open.');
      }
    },

    createLobby() {
      const data = {
        command: 'lobby',
        command_key: 'create'
      };
      this.sendMessage(data);
    },


    joinLobby() {
      const data = {
        command: 'lobby',
        command_key: 'join',
        key: this.lobbyKey,
        pos: this.joinLobbyPosition,

      };
      this.sendMessage(data);
    },

    leaveLobby() {
      const data = {
        command: 'lobby',
        command_key: 'leave',
      };
      this.sendMessage(data);
    },

    swapPositionInLobby() {
      const data = {
        command: 'lobby',
        command_key: 'swap',
        pos: this.position
      };
      this.sendMessage(data);
    },

    showPos() {
      const data = {
        command: 'lobby',
        command_key: 'pos'
      };
      this.sendMessage(data);
    },

    showLobbyList() {
      const data = {
        command: 'lobby',
        command_key: 'status',
      };
      this.sendMessage(data);
    },

    playCreate() {
      const data = {
        command: 'play',
        command_key: 'create',
        game: this.game,
        mode: this.mode,
        difficulty: this.difficulty
      };
      this.sendMessage(data);
    },

    playValidMoves(){  const data = {
      command: 'play',
      command_key: 'valid_moves',
      isFrontend:true,
    };
      this.sendMessage(data);
      },

    playValidMoves(fromPos)  {  const data = {
      command: 'play',
      command_key: 'valid_moves',
      fromPos:fromPos,
      isFrontend:true,
    };
      this.sendMessage(data);
      },


    playMakeMove(){
      let data;
      if (!this.twoTurnGame)
      {data = {
        command: 'play',
        command_key: 'make_move',
        move: this.toPos,
        isFrontend:true,
    };}
    else { data = {
        command: 'play',
        command_key: 'make_move',
        move: [this.fromPos, this.toPos],
        isFrontend:true
    };}
    this.sendMessage(data);
    },

    playUndoMove() {
      const data = {
        command: 'play',
        command_key: 'undo_move',
        num: this.undoNum,
      };
      this.sendMessage(data);
    },

    playSurrender() {
      const data = {
        command: 'play',
        command_key: 'surrender',
      };
      this.sendMessage(data);
    },

    playNewGame() {
      const data = {
        command: 'play',
        command_key: 'new_game',
      };
      this.sendMessage(data);
    },

    playBlunder() {
      const data = {
        command: 'play',
        command_key: 'blunder',
        isFrontend:true,
      };
      this.sendMessage(data);
    },

    playTimeLine() {
      const data = {
        command: 'play',
        command_key: 'timeline',
        num: this.timeLineNum,
      };
      this.sendMessage(data);
    },

    playStep() {
      const data = {
        command: 'play',
        command_key: 'step',
      };
      this.sendMessage(data);
    },

    playUnstep() {
      const data = {
        command: 'play',
        command_key: 'unstep',
      };
      this.sendMessage(data);
    },

    playEvaluate(){
      const data = {
        command: 'play',
        command_key: 'evaluate',
        num: this.evaluateNum,
        game: this.game,
        mode: this.mode,
        difficulty: this.difficulty,
      }
      this.sendMessage(data);
    },

    trackMousePosition(event) {
    this.mouseX = event.clientX;
    this.mouseY = event.clientY;
    const imageRect = this.$refs.imageRef.getBoundingClientRect();
    this.mouseX = this.mouseX - imageRect.left;
    this.mouseY = this.mouseY - imageRect.top;
    this.mouseX = Math.ceil(this.mouseX / (this.$refs.imageRef.offsetWidth / this.boardWidth));
    this.mouseY = Math.ceil(this.mouseY / (this.$refs.imageRef.offsetHeight / this.boardHeight));
    if (this.twoTurnGame) {
      if (this.turnSelect) {this.fromPos=this.mouseX+(this.boardHeight*this.mouseY-this.boardHeight -1); 
                            this.turnSelect=false;
                            this.playValidMoves(this.fromPos);}
      else {                this.toPos=this.mouseX+(this.boardHeight*this.mouseY-this.boardHeight -1);
                            this.turnSelect=true
                            this.playMakeMove();
      }
    }
    else {this.toPos=this.mouseX+(this.boardHeight*this.mouseY-this.boardHeight -1);


    if (!this.validMoveInsteadOfMakeMove)this.playMakeMove();
    else {
      this.fromPos=this.toPos; //TODO: Achtung nur für Debug, muss geändert werden für merhzügige Spiele!
      this.playValidMoves();}}
  },


    addPair() {  //TODO Verbessern, scheint noch kein richtiges JSON zu sein
      if (this.newKey && this.newValue) {
        this.userSentJSON[this.newKey] = this.newValue;
        this.newKey = '';
        this.newValue = '';
      }
    },

    sendUserSentJSON(){
      this.userSentJSON["command"] = this.commandInUserJSON;
      this.userSentJSON["command_key"] = this.commandKeyInUserJSON;
      this.sendMessage(JSON.stringify(this.userSentJSON));
      this.userSentJSON = {};
    },
    highlightCellOnHover(event) {
  const imageRect = this.$refs.imageRef.getBoundingClientRect();
  const mouseX = event.clientX - imageRect.left;
  const mouseY = event.clientY - imageRect.top;
  const cellX = Math.ceil(mouseX / (this.$refs.imageRef.offsetWidth / this.boardWidth));
  const cellY = Math.ceil(mouseY / (this.$refs.imageRef.offsetHeight / this.boardHeight));

  // Set the hovered cell coordinates
  this.hoveredCell = { x: cellX, y: cellY };
},


},


  mounted() {
    this.connect();
  },
  beforeDestroy() {
    this.disconnect();
  }
};
</script>


<style lang="css" scoped>
.grid-section {
  margin: 1rem;
}

.box {
  border: 2px solid white;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.limited-width-box {
  width: 350px; 
  overflow: auto;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.highlight-cell {
  position: absolute;
  background-color: rgba(255, 255, 0, 0.5);
  pointer-events: none;
  z-index: 10;
}

@media (min-width: 1024px) {
  #app {
    display: grid;
    grid-template-columns: repeat(autofill, 0.5fr);
    grid-gap: 1rem;
  }
}
</style>
