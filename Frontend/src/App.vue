<template>
  <header>
    <nav-bar></nav-bar>
  </header>
  <main>
    <RouterView v-if="socketConnected===true"/>
    <div v-else>
      <teleport to="body"><base-dialog  :title="'Building Connection'"><template #actions>
          <base-button @click="connectWebSocket">Try Connecting</base-button>
        </template></base-dialog> </teleport></div>
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
    ...mapGetters(["gameActive",'socketConnected']),
    isPlayPage() {
      return this.$route.name === "play";
    }
  },
  methods: {
    connectWebSocket(){
      this.$store.dispatch("initWebSocket");
    },
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
