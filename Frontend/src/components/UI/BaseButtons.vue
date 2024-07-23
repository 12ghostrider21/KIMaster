<template>
  <button class="button">
    <slot></slot>
  </button>
</template>

<script>
/**
* Basic reusable Button
* @module BaseButton 
*/
export default {

};
</script>
<style scoped>

.button {
  background-color: rgba(255, 255, 255, 0.5); /* Durchsichtige weiße Farbe */
  color: black; /* Schwarzer Text */
  border: 2px solid black; /* Schwarzer Rand */
  padding: 15px 30px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 0 0 rgba(255, 255, 255, 0); /* Initialer Schatten auf transparent setzen */
  
}

.button:hover {
  background-color: rgba(211, 211, 211, 0.5); /* Leicht graue Farbe beim Hover */
  box-shadow: 0 0 15px rgba(128, 128, 128, 0.8); /* Grauer Schatten für den Leuchteffekt */
  transform: scale(1.1); /* Vergrößert den Button beim Hovern */
}

.button:active {
  transform: scale(0.98); /* Leichte Verkleinerung beim Klicken */
}

.button:focus{
  outline: none; /* Entfernt den Fokus-Rand */
}

</style>
