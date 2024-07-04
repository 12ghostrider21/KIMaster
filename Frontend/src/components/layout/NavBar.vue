<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary nav-bar">
    <div class="container-fluid">
      <router-link class="navbar-brand" :to="{name:'home'}">{{ $t('KI Master') }}</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item"> 
            <router-link class="nav-link" v-if="!isStartingPage" to="/">{{ $t('message.home') }}</router-link>
          </li>
          <li class="nav-item" v-if="isStartingPage">
            <router-link class="nav-link":to="{name:'instruction'}">{{ $t('message.instruction') }}</router-link>
          </li>
          <li class="nav-item" v-if="isPlayPage">
            <a class="nav-link" href="#" @click.prevent="showRules">{{ $t('message.show_rules') }}</a>
          </li>
        </ul>
        <language-switcher></language-switcher>
      </div>
    </div>

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
    BaseDialog, // Registriere die base-dialog Komponente
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
    }
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
      if (this.$route.params.game === 'connect4') {
        this.currentRuleComponent = 'Connect4Rules';
      } else if (this.$route.params.game === 'tictactoe') {
        this.currentRuleComponent = 'TicTacToeRules';
      } else if (this.$route.params.game === 'nim') {
        this.currentRuleComponent = 'NimRules';
      } else if (this.$route.params.game === 'othello') {
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

#navbarSupportedContent {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.form-select {
  width: auto;
  min-width: 100px;
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

.form-select:focus {
  box-shadow: none;
}

@media (max-width: 991.98px) {
  #navbarSupportedContent {
    flex-direction: column;
    align-items: flex-start; /* Align items to the start */
  }

  .navbar-nav {
    width: 100%;
  }
  
  .form-select {
    margin-bottom: 0.5rem;
  }
}
</style>
