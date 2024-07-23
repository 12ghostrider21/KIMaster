<template>
  <div class="base-card">
    <header v-if="$slots.header">
      <slot name="header"> 
      </slot>
    </header>
    <slot></slot>
  </div>
</template>

<script>
  /**
  * Used to group several Elements together into one basic Unit
  * @module BaseCard 
  */
export default {
    mounted(){
        console.log(this.$slots.header)
    }
};
</script>

<style scoped>

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
div {
  margin: 1.5rem auto;
  max-width: 50rem;
  border-radius: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
  padding: 1rem;
}

.base-card {
  background-color: #ffffff; /* Hintergrundfarbe auf Weiß gesetzt */
}
</style>
