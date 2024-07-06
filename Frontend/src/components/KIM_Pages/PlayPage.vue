<template>
  <div>
    <!-- Game Controls -->
    <div>
      <base-button v-if="position!='sp'" @click="surrenderGame()">{{ $t('message.surrender') }}</base-button>
      <base-button v-if="position!='sp'" @click="quitGame()">{{ $t('message.quit_game') }}</base-button>
      <base-button @click="showRules">{{ $t('message.show_rules') }}</base-button>
      <base-button v-if="position==='sp'" @click="leaveGame()">{{ $t('message.quit_game') }}</base-button>
      
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

    <base-button  v-if="position!='sp'" @click="undoMove()">{{ $t('message.undo_move') }}</base-button>
    <base-button v-if="this.gameOver&& position!='sp'" @click="newGame">{{ $t('message.new_game') }}</base-button>
    <div v-if="gameOver" class="control-Buttons">
      <base-button @click="first()">{{ $t('message.first') }}</base-button>
      <base-button @click="unstep()">{{ $t('message.previous') }}</base-button>
      <base-button @click="step()">{{ $t('message.next') }}</base-button>
      <base-button @click="last()">{{ $t('message.last') }}</base-button>
    </div>
    
    <!-- Footer -->
    <footer-bar></footer-bar>

    <!-- Game Over Dialog -->
    <teleport to="body">
      <base-dialog
        v-if="popup === enums.popUpStatus.GAMEOVER"
        :title="$t('message.game_over')"
        @close="() => { closePopup(); unstep(); }"
      >
        <template #default>
          <p v-if="playerWon === 1">{{ $t('message.player_1_won') }}</p>
          <p v-else>{{ $t('message.player_2_won') }}</p>
          <p>{{ $t('message.game_over_after') }} {{ turn }} {{ $t('message.turns') }}</p>
        </template>
        <template #actions>
          <base-button v-if="position!='sp'" @click="newGame">{{ $t('message.new_game') }}</base-button>
          <base-button @click="() => { closePopup(); unstep(); }">{{ $t('message.okay') }}</base-button>
        </template>
      </base-dialog>
    </teleport>

    <!-- Rules Dialog -->
    <teleport to="body">
      <base-dialog
        :title="$t('rules.game_title')"
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
import OthelloRules from '@/components/gameRules/OthelloRules.vue';
import NimRules from '@/components/gameRules/NimRules.vue';

export default {
  mixins: [PlayPageLogic],
  components: {
    Connect4Rules,
    TicTacToeRules,
    NimRules,
    OthelloRules
   
  },
  methods: {
    showRules() {
      this.isRulesVisible = true;
    },
    closeRules() {
      this.isRulesVisible = false;
    }
  },
};
</script>

<style src="./src/components/UI/PlayPage.css"></style>

