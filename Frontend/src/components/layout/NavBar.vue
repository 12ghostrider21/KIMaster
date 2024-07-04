<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary nav-bar">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">{{ $t('KI Master') }}</router-link>
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
            <router-link class="nav-link" to="/instruction">{{ $t('message.instruction') }}</router-link>
          </li>
          <li class="nav-item" v-if="isPlayPage">
            <a class="nav-link" href="#" @click.prevent="$emit('show-rules')">{{ $t('message.show_rules') }}</a>
          </li>
          <!-- <li class="nav-item">
            <a class="nav-link" href="#">{{ $t('message.leaderboard') }}</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">{{ $t('message.achievements') }}</a>
          </li> -->
        </ul>
        <language-switcher></language-switcher>
      </div>
    </div>
  </nav>
</template>

<script>

import { useRoute } from "vue-router";
import LanguageSwitcher from './LanguageSwitcher.vue';

export default {
  components: { LanguageSwitcher },
  data() {
    return {
      currentLanguage: this.$i18n.locale,
    };
  },
  computed: {
    isStartingPage() {
      return this.$route.name === 'home';
    },
    isPlayPage(){
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
