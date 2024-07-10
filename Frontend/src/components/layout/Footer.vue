<template>
    <footer>
    <a href="https://www.thm.de"> THM</a>

    <RouterLink :to="{name:'about'}">Copyright</RouterLink>

    <RouterLink :to="{name:'impressum'}">Impressum</RouterLink>
  </footer>
</template>

<style scoped>
footer {
  width: 100%;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  background-color: #f8f9fa; /* Optional: Hintergrundfarbe für den Footer */
  box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1); /* Optional: Schatten für den Footer */
}

footer a {
  color: green;
  text-decoration: none;
  margin-left: 30px;
}
footer a:hover{
    color: #007bff; 
}
</style>