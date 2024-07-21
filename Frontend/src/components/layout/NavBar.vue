<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary nav-bar">
    <div class="container-fluid">
      <router-link class="navbar-brand" @click="leaveLobby()" :to="{ name: 'home' }">
        <img :src="logo" alt="KI Master Logo" class="logo" />
      </router-link>
      <div class="navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item" v-if="isStartingPage">
            <router-link class="nav-link" :to="{ name: 'instruction' }">{{ $t('message.instruction') }}</router-link>
          </li>
        </ul>
      </div>
      <div class="top-right-controls">
        <label class="switch">
          <input type="checkbox" v-model="isDarkMode" @change="toggleDarkMode">
          <span class="slider round"></span>
        </label>
        <language-switcher class="me-2"></language-switcher>
      </div>
    </div>
    <!-- Rules Dialog -->
    <teleport to="body">
      <base-dialog :title="$t('rules.game_title')" v-if="isRulesVisible" @close="closeRules">
        <component :is="currentRuleComponent" />
        <template #actions>
          <base-button @click="closeRules">{{ $t('message.okay') }}</base-button>
        </template>
      </base-dialog>
    </teleport>
  </nav>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { useRoute } from "vue-router";
// import ChessRules from '@/components/gameRules/ChessRules.vue';
import Connect4Rules from '@/components/gameRules/Connect4Rules.vue';
import NimRules from '@/components/gameRules/NimRules.vue';
import OthelloRules from '@/components/gameRules/OthelloRules.vue';
import TicTacToeRules from '@/components/gameRules/TicTacToeRules.vue';
import PlayPageLogic from '../UI/PlayPage.js';
import BaseDialog from '@/components/UI/BaseDialog.vue';
import LanguageSwitcher from './LanguageSwitcher.vue';
import logo from '@/components/icons/logo.png'; // Importiere das Logo

export default {
  components: {
    Connect4Rules,
    NimRules,
    OthelloRules,
    TicTacToeRules,
    LanguageSwitcher,
    BaseDialog,
  },
  mixins: [PlayPageLogic],
  data() {
    return {
      currentLanguage: this.$i18n.locale,
      isRulesVisible: false,
      currentRuleComponent: null,
      logo, // Füge das Logo zur Datenfunktion hinzu
    };
  },
  computed: {
    isStartingPage() {
      return this.$route.name === 'home';
    },
    isPlayPage() {
      return this.$route.name === 'play';
    },
    isLobbyPage() {
      return this.$route.name === 'lobby';
    },
    ...mapGetters(['gameActive']),
  },
  methods: {
    ...mapActions(["sendWebSocketMessage"]),
    sendMessage(data) {
      console.log(data);
      this.sendWebSocketMessage(JSON.stringify(data));
    },
    leaveLobby() { //Leaving Lobby when pressing on the KIM Button in the Top right when a Game isn't running, removes unexpected behaviour when seemingly leaving a lobby and trying to join/create a new one
      if (this.$route.name === 'lobby' || 
        this.$route.name === 'wait' || 
        (this.$route.name === 'play' && !this.gameActive) || 
        (this.$route.name === 'instructions' && !this.gameActive) || 
        (this.$route.name === 'impressum' && !this.gameActive) || 
        (this.$route.name === 'about' && !this.gameActive)) {   
        const data = {
          command: "lobby",
          command_key: "leave",
        };
        this.sendMessage(data);
      }
    },
    changeLanguage() {
      if (this.$i18n.locale === 'en') {
        this.$i18n.locale = 'de';
        this.currentLanguage = 'de';
      } else {
        this.$i18n.locale = 'en';
        this.currentLanguage = 'en';
      }
      this.$nextTick(() => {
        document.querySelector('.form-select').blur();
      });
    },
    showRules() {
      if (this.game === 'connect4') {
        this.currentRuleComponent = 'Connect4Rules';
      } else if (this.game === 'tictactoe') {
        this.currentRuleComponent = 'TicTacToeRules';
      } else if (this.game === 'nim') {
        this.currentRuleComponent = 'NimRules';
      } else if (this.game === 'othello') {
        this.currentRuleComponent = 'OthelloRules';
      } else {
        this.currentRuleComponent = null;
      }
      this.isRulesVisible = true;
    },
    closeRules() {
      this.isRulesVisible = false;
    },
  },
};
</script>

<style scoped>
.container-fluid {
  padding-left: 15px;
  padding-right: 15px;
  margin-right: auto;
  margin-left: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  display: flex;
  align-items: center; /* Ensures the logo is vertically centered */
}

.nav-item {
  margin-left: 10px;
}

.nav-link:hover {
  color: #007bff;
}

.navbar-collapse {
  display: flex;
  flex-grow: 1;
  justify-content: space-between;
  align-items: center;
}

.top-right-controls {
  display: flex;
  align-items: center;
  position: absolute;
  right: 10px;
}

/* Toggle Switch Styles */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
  margin-right: 10px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.logo {
  width: auto;
  height: 40px; /* Adjust the height to fit within the navbar */
  max-height: 40px; /* Ensure it doesn't overflow the navbar */
  aspect-ratio: 2.31; /* Maintain the aspect ratio */
}

@media (max-width: 768px) {
  .navbar-collapse {
    flex-direction: row;
    align-items: center;
    width: 100%;
  }

  .navbar-nav {
    flex-direction: row;
    align-items: center;
  }

  .form-select {
    margin-bottom: 0.5rem;
  }
}
</style>
