<template>
  <header>
    <nav-bar></nav-bar>
  </header>
  <main>
    <RouterView/>
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
    },
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
