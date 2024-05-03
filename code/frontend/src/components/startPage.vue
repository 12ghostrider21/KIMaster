<template>
  <div>
    <button @click="redirectToImage">Lobby erstellen</button>
  </div>
</template>

<script>
export default {
  methods: {
    redirectToImage() {
      this.$router.push('/lobby');
    }
  }
};
</script>

<style scoped>
/* Add your styles here */
</style>