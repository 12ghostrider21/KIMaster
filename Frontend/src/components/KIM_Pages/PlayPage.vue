<template>
  <div>
    <!-- Game Controls -->
    <div>
      <base-button @click="surrenderGame()">{{ $t('message.surrender') }}</base-button>
      <base-button @click="quitGame()">{{ $t('message.quit_game') }}</base-button>
      <base-button @click="showRules">{{ $t('message.show_rules') }}</base-button>
      <base-button v-if="game==='nim'" @click="sendNimMove" >NIM MOVE {{ nimTest }}</base-button>
    </div>
    
    <!-- Game Board -->
     
    <div class="grid-section">
      
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
        @contextmenu.prevent="playValidMoves()"
      />
     
      <div
        v-if="hoveredCell && currentImageIndex === images.length - 1"
        class="highlight-cell"
        :style="{
          width: `${300 / boardWidth}px`,
          height: `${300 / boardHeight}px`,
          top: `${(hoveredCell.y - 1) * (300 / boardHeight)}px`,
          left: `${(hoveredCell.x - 1) * (300 / boardWidth)}px`,
        }"
      ></div>
    </div>
    
    <!-- Image Control Buttons -->
    <div class="control-Buttons">
      <base-button @click="firstImage()">{{ $t('message.first') }}</base-button>
      <base-button @click="prevImage()">{{ $t('message.previous') }}</base-button>
      <base-button @click="nextImage()">{{ $t('message.next') }}</base-button>
      <base-button @click="lastImage()">{{ $t('message.last') }}</base-button>
    </div>
    <base-button @click="undoMove()">{{ $t('message.undo_move') }}</base-button>
    <base-button v-if="this.gameOver" @click="newGame()">{{ $t('message.new_game') }}</base-button>
    
    <!-- Footer -->
    <footer-bar></footer-bar>

    <!-- Game Over Dialog -->
    <teleport to="body">
      <base-dialog
        v-if="popup === enums.popUpStatus.GAMEOVER"
        :title="$t('message.game_over')"
        @close="closePopup"
      >
        <template #default>
          <p v-if="playerWon === 1">{{ $t('message.player1_won') }}</p>
          <p v-else>{{ $t('message.player2_won') }}</p>
          <p>{{ $t('message.game_over_after') }} {{ turn }} {{ $t('message.turns') }}</p>
        </template>
        <template #actions>
          <base-button @click="newGame">{{ $t('message.new_game') }}</base-button>
          <base-button @click="closePopup">{{ $t('message.okay') }}</base-button>
        </template>
      </base-dialog>
    </teleport>

    <!-- Rules Dialog -->
    <teleport to="body">
      <base-dialog
        :title="$t('message.rules')"
        v-if="isRulesVisible"
        @close="closeRules"
      >
        <component :is="currentRuleComponent" />
        <template #actions>
          <base-button @click="closeRules">{{ $t('message.okay') }}</base-button>
        </template>
      </base-dialog>
    </teleport>
  </div>
</template>

<script>
import PlayPageLogic from '../UI/PlayPage.js';
// import ChessRules from '@/components/gameRules/ChessRules.vue';
import Connect4Rules from '@/components/gameRules/Connect4Rules.vue';
import TicTacToeRules from '@/components/gameRules/TicTacToeRules.vue';
// import OthelloRules from '@/components/gameRules/OthelloRules.vue';

export default {
  mixins: [PlayPageLogic],
  components: {
    Connect4Rules,
    TicTacToeRules,
   
  },
  methods: {
    showRules() {
      this.isRulesVisible = true;
    },
    closeRules() {
      this.isRulesVisible = false;
    }
  }
};
</script>

<style src="./src/components/UI/PlayPage.css"></style>

