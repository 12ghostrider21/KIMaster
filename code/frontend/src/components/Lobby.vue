

<template>
  <div class="lobby">
    <h1>Welcome to the Lobby</h1>
    <div class="dropdowns">
      <div class="dropdown">
        <label for="dropdown1">Option 1:</label>
        <select id="dropdown1" v-model="selectedOption1">
          <option value="option1">Option 1</option>
          <option value="option2">Option 2</option>
          <option value="option3">Option 3</option>
        </select>
      </div>
      <div class="dropdown">
        <label for="dropdown2">Option 2:</label>
        <select id="dropdown2" v-model="selectedOption2">
          <option value="optionA">Option A</option>
          <option value="optionB">Option B</option>
          <option value="optionC">Option C</option>
        </select>
      </div>
      <div>
        <button @click="redirectToImage()">Start Game</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedOption1: 'option1',
      selectedOption2: 'optionA',
      // Add more data properties for each dropdown as needed
    };
  },
  methods: {
    redirectToImage() {
      this.$router.push('/image');
    }
  }

};
</script>

<style>
/* Add your CSS styles here */
</style>
