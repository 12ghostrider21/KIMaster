<template>
  <header>
    <nav-bar></nav-bar>
  </header>
  <main>
    <RouterView v-if="connectionLost===false"/>
    <div v-else>
      <teleport to="body"><base-dialog  :title="'Connection Lost'">
        <template #default>
          {{$t('message.connection_not_possible')}}:
        </template>
        <template #actions>
          <base-button @click="connectWebSocket">Try Reconnecting</base-button>
        </template></base-dialog> </teleport></div>
    <dragable-image v-if="gameActive && !isPlayPage"></dragable-image>
  </main>
  <footer>
    <footer-bar></footer-bar>
  </footer>
</template>

<script>
import { useRouter } from 'vue-router';
import { mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters(["gameActive",'connectionLost']),
    isPlayPage() {
      return this.$route.name === "play";

    }
  },
  methods: {
    connectWebSocket(){
      this.$router.push({
      name: "home"
    });
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
