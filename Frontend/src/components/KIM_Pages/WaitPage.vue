<template>
  <div id="hauptteil-about">
    <section class="content-container">
      <base-card class="WaitingTitle">
        <h1>{{ $t('message.waitMessage') }}</h1>
      </base-card>
      <base-card>
        <select v-model="positionSelect" @change="swapPositionInLobby">
          <option value="p1">{{ $t('message.player1') }}</option>
          <option value="p2">{{ $t('message.player2') }}</option>
          <option value="sp">{{ $t('message.spectator') }}</option>
        </select>
      </base-card>
      <base-card>
        <p>{{ $t('message.your_position', { position: position }) }}</p>
        <p>{{ $t('message.lobby_position', { p1: positionsInLobby[0], p2: positionsInLobby[1], spectators: positionsInLobby[2] }) }}</p>
      </base-card>
    </section>
  </div>
</template>


<style>

</style>

<script src="./src/components/UI/WaitPage.js"></script>
<style src="./src/components/UI/WaitPage.css"></style>