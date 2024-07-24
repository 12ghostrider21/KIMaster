<template>
  <section id="hauptteil" class="d-flex align-items-center justify-content-center">
    <div class="content-container">
      <div class="welcome-container">
        <base-card>
          <template #header>
            <h1>{{ $t('message.welcome') }}</h1>
          </template>
          <p class="subtitle">{{ $t('message.subtitle') }}</p>
        </base-card>
      </div>
      <base-card>
      <div class="game-selection-container">
          <template v-if="gameActive">
            <base-button v-for="game in Object.values(games)" :key="game" @click="triggerPopUp">
              {{ $t(`message.${game}`) }}
            </base-button>
          </template>
          <template v-else>
            <router-link v-for="game in Object.values(games)" :key="game" :to="{ name: 'lobby' }">
              <base-button @click="setGame(game)">{{ $t(`message.${game}`) }}</base-button>
            </router-link>
          </template>
        </div>
      </base-card>

      <base-card class="LobbySection">
        <input type="text" v-model="lobbyKeyToJoin" :placeholder="$t('message.enter_lobby_key')" />
        <div class="message-box" v-if="this.notif === ENUMS.notifStatus.LOBBYJOINFAIL">
          {{ $t('message.lobby_join_failed') }}
        </div>
        <base-button @click.prevent="joinLobbyStart">{{ $t('message.join_lobby') }}</base-button>
    </base-card>
    </div>

    <teleport to="body">
      <base-dialog
        v-if="popUpTrigger"
        @close="closePopUp"
      >
        <template #default>
         <p>{{ $t('message.surrender_before_start') }}</p>
        </template>
        <template #actions>
          <base-button @click="surrenderGame">{{ $t('message.surrender') }}</base-button>
          <base-button @click="returnToGame">  {{ $t('message.return_to_game') }} </base-button>
          <base-button @click="closePopUp">{{ $t('message.okay') }}</base-button>
        </template>
      </base-dialog>
    </teleport>

  </section>
  <footer-bar class="FooterStart"></footer-bar>
</template>

<script src="./src/components/UI/StartPage.js"></script>
<style src="./src/components/UI/StartPage.css"></style>