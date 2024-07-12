<template>

  <!-- Game Controls -->
  <base-card>
    <div class="ButtonUp">
      <base-button @click="showRules">{{ $t('message.show_rules') }}</base-button>
      <base-button v-if="!this.gameOver && position !== 'sp'" @click="surrenderGame()">
        {{ $t('message.surrender') }}
      </base-button>
      <base-button v-if="this.gameOver && position !== 'sp'" @click="returnLobby()">
      {{ $t('message.lobby') }}   
      </base-button>
      <base-button v-if="this.gameOver && position !== 'sp'" @click="quitGame()">
        {{ $t('message.quit_game') }}
      </base-button>
      <base-button v-if="position === 'sp'" @click="leaveGame()">
        {{ $t('message.quit_game') }}
      </base-button>
      <base-button v-if="this.gameOver && position !== 'sp'" @click="newGame">
      {{ $t('message.new_game') }}   
      </base-button>
      <div v-if="this.gameOver && position !== 'sp'">
        <base-button @click="blunder()">{{ $t('message.blunder') }}</base-button>
      </div>
    </div>
  </base-card>

  <div class="SpielerZug">
    <p v-if="yourTurn && position !== 'sp'">{{ $t('message.your_turn') }}</p>
    <p v-if="!yourTurn && position !== 'sp'">{{ $t('message.opponent_turn') }}</p>
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
      v-if="hoveredCell"
      class="highlight-cell"
      :style="{
        width: `${300 / boardWidth}px`,
        height: `${300 / boardHeight}px`,
        top: `${(hoveredCell.y - 1) * (300 / boardHeight)}px`,
        left: `${(hoveredCell.x - 1) * (300 / boardWidth)}px`,
      }"
    ></div>
  </div>

  <base-card class="lower-card" v-if="position!=='sp'">
    <base-button
      v-if="!this.gameOver && game === 'nim' && nimTest[0] !== -1"
      @click="sendNimMove"
    >
      {{ $t('message.nim_move') }} - {{ $t('message.row') }}: {{ Number(nimTest[0]) + 1 }},
      {{ $t('message.amount') }}: {{ nimTest[1] }}
    </base-button>
    <base-button v-if="!this.gameOver" @click="undoMove()">
      {{ $t('message.undo_move') }}
    </base-button>
    <div v-if="this.gameOver" >
      <div class="control-Buttons">
        <base-button @click="first()">{{ $t('message.first') }}</base-button>
        <base-button @click="unstep()">{{ $t('message.previous') }}</base-button>
        <base-button @click="step()">{{ $t('message.next') }}</base-button>
        <base-button @click="last()">{{ $t('message.last') }}</base-button>
    </div>
  </div>
</base-card>

  <!-- Footer -->
  <footer-bar class="FooterPlay"></footer-bar>

  <!-- Blunder Dialog -->
  <teleport to="body">
    <base-dialog
      v-if="popup === enums.popUpStatus.BLUNDER"
      :title="$t('message.blunder')"
      @close="() => { closePopup(); }"
    >
      <template #default>
        <div class="scrollable">
          <img
            width="300"
            height="300"
            v-if="imageSrc"
            :src="imageSrc"
            alt="Received Image"
          />
          <base-button @click="unstep()">{{ $t('message.previous') }}</base-button>
          <base-button @click="step()">{{ $t('message.next') }}</base-button>
        </div>
        <div>
          <base-button
            v-for="blunder in blunders"
            :key="blunders.action"
            @click="jumpTimeLine(Number(blunder.it) + 1)"
          >
            {{ $t('message.turn') }}: {{ Number(blunder.it) + 1 }}
          </base-button>
        </div>
      </template>
      <template #actions>
        <base-button v-if="position !== 'sp'" @click="newGame">
          {{ $t('message.new_game') }}
        </base-button>
        <base-button @click="() => { closePopup(); }">{{ $t('message.okay') }}</base-button>
      </template>
    </base-dialog>
  </teleport>

  <!-- Game Over Dialog -->
  <teleport to="body">
    <base-dialog
      v-if="popup === enums.popUpStatus.GAMEOVER"
      :title="$t('message.game_over')"
      @close="() => { closePopup(); unstep(); }"
    >
      <template #default>
        <p v-if="playerWon === 1&& position==='sp'">{{ $t('message.player_1_won') }}</p>
        <p v-if="playerWon === -1">{{ $t('message.player_2_won') }}</p>
        <p v-if="playerWon === 0 && position==='sp'">{{ $t('message.draw') }}</p>
        <p v-if="playerWon === 1&& position==='p1' ||playerWon === -1 & position==='p2'" >{{ $t('message.you_won') }}</p>
        <p v-if="playerWon === 1&& position==='p2' ||playerWon === -1 & position==='p1'"> {{ $t('message.opponent_won') }}</p>
        <p>{{ $t('message.game_over_after') }} {{ turn }} {{ $t('message.turns') }}</p>
      </template>
      <template #actions>
        <base-button v-if="position !== 'sp'" @click="newGame">
          {{ $t('message.new_game') }}
        </base-button>
        <base-button @click="() => { closePopup(); unstep(); }">
          {{ $t('message.okay') }}
        </base-button>
      </template>
    </base-dialog>
  </teleport>

  <!-- Rules Dialog -->
  <teleport to="body">
    <base-dialog
      v-if="isRulesVisible"
      @close="closeRules"
    >
      <component :is="currentRuleComponent" />
      <template #actions>
        <base-button @click="closeRules">{{ $t('message.okay') }}</base-button>
      </template>
    </base-dialog>
  </teleport>
</template>

<script>
import PlayPageLogic from '../UI/PlayPage.js';
// import ChessRules from '@/components/gameRules/ChessRules.vue';
import Connect4Rules from '@/components/gameRules/Connect4Rules.vue';
import TicTacToeRules from '@/components/gameRules/TicTacToeRules.vue';
import OthelloRules from '@/components/gameRules/OthelloRules.vue';
import NimRules from '@/components/gameRules/NimRules.vue';
import CheckersRules from '@/components/gameRules/CheckersRules.vue';

export default {
  mixins: [PlayPageLogic],
  components: {
    Connect4Rules,
    TicTacToeRules,
    NimRules,
    OthelloRules,
    CheckersRules,
  },
  methods: {
    showRules() {
      this.isRulesVisible = true;
    },
    closeRules() {
      this.isRulesVisible = false;
    },
  },
};
</script>

<style src="./src/components/UI/PlayPage.css"></style>