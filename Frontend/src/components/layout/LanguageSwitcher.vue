<template>
  <!-- Dropdown for selecting language -->
  <select @change="changeLanguage($event)" v-model="currentLanguage">
    <option value="en">English</option>
    <option value="de">Deutsch</option>
    <option value="fr">Français</option>
    <option value="es">Español</option>
  </select>
</template>

<script>
/**
 * Dropdown that switches the currently active Language of the application
 * @module LanguageSwitcher
 */
export default {
  data() {
    return {
      /**
       * The currently selected language.
       * @type {string}
       */
      currentLanguage: this.$i18n.locale,
    };
  },
  methods: {
    /**
     * Changes the application's language.
     * @param {Event} event - The change event triggered by the language selection.
     */
    changeLanguage(event) {
      const language = event.target.value;
      this.$i18n.locale = language;
      localStorage.setItem('locale', language);
      this.currentLanguage = language;
    }
  },
  created() {
    /**
     * Sets the initial language based on the saved locale in localStorage.
     * This lifecycle hook is called after the instance is created.
     */
    const savedLanguage = localStorage.getItem('locale');
    if (savedLanguage) {
      this.$i18n.locale = savedLanguage;
      this.currentLanguage = savedLanguage;
    }
  }
};
</script>

<style scoped>
/* Styling for the select dropdown */
select {
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  line-height: 1.5;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  background-color: #fff;
  background-clip: padding-box;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.075);
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

/* Focus state styling for the select dropdown */
select:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
</style>
