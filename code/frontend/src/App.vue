<script setup>
</script>

<template>

  <main>
    <RouterView/>
  </main>

  <footer>
    <a href="https://www.thm.de"> THM</a>
    |
    <RouterLink to="/">Home</RouterLink>
    |
    <RouterLink to="/about">About</RouterLink>
    |
    <RouterLink to="/impressum">Impressum</RouterLink>
  </footer>
</template>

<style scoped>
footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #333;
  color: white;
  padding: 10px;
  text-align: center;
  z-index: 9999; /* Ensure the footer is above all other content */
}
</style>
