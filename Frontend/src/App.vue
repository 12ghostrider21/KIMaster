<template>
  <header>
    <nav-bar @show-rules="showRules"></nav-bar>
  </header>
  <main>
    <RouterView @show-rules="showRules"/>
    <dragable-image v-if="gameActive && !isPlayPage"></dragable-image>
  </main>
  <footer>
    <footer-bar></footer-bar>
  </footer>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters(["gameActive"]),
    isPlayPage() {
      return this.$route.name === "play";
    }
  },
  methods: {
    showRules() {
      this.$root.$emit('show-rules');
    }
  },
  created() {
    this.$store.dispatch("initWebSocket");
    const savedLanguage = localStorage.getItem("locale");
    if (savedLanguage) {
      this.$i18n.locale = savedLanguage;
    }
  },
};
</script>

<style scoped></style>
