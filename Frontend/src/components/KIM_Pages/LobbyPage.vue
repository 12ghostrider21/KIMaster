<template>
  <section id = "hauptteil-lobby">
  <section class="content-container">
    <base-card>
      <template #header>
        <h1>{{ $t('message.lobby_welcome') }} {{ transformGameName(game) }} Lobby</h1>
      </template>
    </base-card>

    <base-card>
      <div class="control">
        <div class="horizontal-selects">
          <select v-model="positionSelect" @change="swapPositionInLobby">
            <option value="p1">{{ $t('message.player1') }}</option>
            <option value="p2">{{ $t('message.player2') }}</option>
            <option value="sp">{{ $t('message.spectator') }}</option>
          </select>
          <div class="message-box" v-if="notif === enums.notifStatus.POSOCCUPIED">
          {{ $t('message.lobby_swap_failed') }}
        </div>
          <select v-model="mode">
            <option value="player_vs_player">{{ $t('message.player_vs_player') }}</option>
            <option value="player_vs_kim">{{ $t('message.player_vs_ai') }}</option>
            <option value="playerai_vs_kim">{{ $t('message.playerai_vs_ai') }}</option>
            <option value="playerai_vs_playerai">{{ $t('message.playerai_vs_playerai') }}</option>
          </select>
          <select v-model="difficulty" v-if="mode==='player_vs_kim'||mode==='playerai_vs_kim'||mode==='kim_vs_player'|| mode==='kim_vs_playerai'">
            <option value="easy">{{ $t('message.easy') }}</option>
            <option value="medium">{{ $t('message.medium') }}</option>
            <option value="hard">{{ $t('message.hard') }}</option>
          </select>

          <select v-model="selectedGame" @change="setGame(selectedGame)">
            <option v-for="(value, key) in enums.games" :key="key" :value="value">
              {{ $t(`message.${value}`) }}
            </option>
          </select>
     
          </div>
        </div>

  
    </base-card>

    <base-card>
      <div class="button-group">
        <p1 v-if="lobbyKey === null">{{ $t('message.lobby_key_generating') }}</p1>
        <p1 v-else>Lobby Key: {{ lobbyKey }} 
          <base-button class="qr-code-button" @click="{setPopup(enums.popUpStatus.QR);generateQrCode();}">
            QR-Code
          </base-button>
        </p1>
        <p class="myPosition">{{ $t('message.your_position', { position: position }) }}</p>
        <p class="guestPosition">{{ $t('message.lobby_position', { p1: positionsInLobby[0], p2: positionsInLobby[1], spectators: positionsInLobby[2] }) }}</p>
      </div>
    </base-card>

    
    <base-card class="LobbyButton">
      <base-button @click="leaveLobby">{{ $t('message.leave_lobby') }}</base-button>
      <base-button @click="playCreate">{{ $t('message.startGame') }}</base-button>
      <div class="message-box" v-if="notif === enums.notifStatus.NOTENOUGHPLAYERS">
          {{ $t('message.game_start_failed') }}
        </div>
    </base-card>

<div v-if="popup===enums.popUpStatus.QR">
 <teleport to="body"><base-dialog  @close="() => { closePopup();}">
      <template #default>
        <canvas ref="qrcodeCanvas"></canvas>
        </template>
       <template #actions>
        <base-button @click="() => { closePopup();}">{{ $t('message.okay') }}</base-button>
      </template></base-dialog> </teleport>
 </div>

  </section>
</section>
  <footer-bar></footer-bar>
</template>

<script src="./src/components/UI/LobbyPage.js"></script>
<style src="./src/components/UI/LobbyPage.css"></style>
