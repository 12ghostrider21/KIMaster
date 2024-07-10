<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary nav-bar">
    <div class="container-fluid">
      <router-link class="navbar-brand" :to="{name:'home'}">{{ $t('KI Master') }}</router-link>
      <div class="navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item" v-if="isStartingPage">
            <router-link class="nav-link" :to="{name:'instruction'}">{{ $t('message.instruction') }}</router-link>
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
  </nav>
</template>

<script>
import { mapGetters } from "vuex";
import { useRoute } from "vue-router";
// import ChessRules from '@/components/gameRules/ChessRules.vue';
import Connect4Rules from '@/components/gameRules/Connect4Rules.vue';
import NimRules from '@/components/gameRules/NimRules.vue';
import OthelloRules from '@/components/gameRules/OthelloRules.vue';
import TicTacToeRules from '@/components/gameRules/TicTacToeRules.vue';
import PlayPageLogic from '../UI/PlayPage.js';
import BaseDialog from '@/components/UI/BaseDialog.vue'; // Importiere die base-dialog Komponente
import LanguageSwitcher from './LanguageSwitcher.vue';

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
    /** ...mapGetters(['game']) */
  },
  methods: {
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
      // Setze die Regel-Komponente abhängig vom aktuellen Spiel
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
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  align-items: center;
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

@media (max-width: 991.98px) {
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
