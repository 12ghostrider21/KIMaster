<template>
  <section class="content-container">
    <base-card>
      <template #header>
        <h1>{{ $t('message.lobby_welcome') }} {{ transformGameName(game) }} Lobby</h1>
      </template>
    </base-card>

    <div class="control">
      <base-button @click="leaveLobby">{{ $t('message.leave_lobby') }}</base-button>
      <div class="horizontal-selects">
        <select v-model="positionSelect" @change="swapPositionInLobby">
          <option value="p1">{{ $t('message.player1') }}</option>
          <option value="p2">{{ $t('message.player2') }}</option>
          <option value="sp">{{ $t('message.spectator') }}</option>
        </select>
        <select v-model="mode" >
          <option value="player_vs_player">{{ $t('message.player_vs_player') }}</option>
          <option value="player_vs_kim">{{ $t('message.player_vs_ai') }}</option>
          <option value="kim_vs_player">Kim vs Player</option>
          <option value="playerai_vs_kim">{{ $t('message.playerai_vs_ai') }}</option>
          <option value="kim_vs_playerai">Kim vs Player Ai</option>
          <option value="playerai_vs_playerai">{{ $t('message.playerai_vs_playerai') }}</option>
          
        </select>

        <select v-model="difficulty" v-if="mode==='player_vs_kim'||mode==='playerai_vs_kim'||mode==='kim_vs_player'|| mode==='kim_vs_playerai'">
          <option value="easy">{{ $t('message.easy') }}</option>
          <option value="medium">{{ $t('message.medium') }}</option>
          <option value="hard">{{ $t('message.hard') }}</option>
        </select>
      </div>
      <div>
        <select v-model="game" @change="setGame()">
          <option value="" disabled>{{ $t('message.change_game_lobby') }}</option>
          <option v-for="(value, key) in enums.games" :key="key" :value="value">
            {{ $t(`message.${value}`) }}
      </option>
    </select>
      </div>
      <div class="button-group">
        <p v-if="lobbyKey === null">{{ $t('message.lobby_key_generating') }}</p>
        <p v-else>Lobby Key: {{ lobbyKey }}</p>
        <p>{{ $t('message.your_position', { position:position }) }}</p>
        <p>{{ $t('message.lobby_position', { p1: positionsInLobby[0], p2: positionsInLobby[1], spectators: positionsInLobby[2] }) }}</p>
      </div>

      <base-button @click="playCreate">Start Game!</base-button>
    </div>

  </section>
  <footer-bar></footer-bar>
</template>

<script src="./src/components/UI/LobbyPage.js"></script>
<style src="./src/components/UI/LobbyPage.css"></style>
