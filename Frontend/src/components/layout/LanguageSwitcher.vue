<template>
  <select @change="changeLanguage($event)" v-model="currentLanguage">
    <option value="en">English</option>
    <option value="de">Deutsch</option>
    <option value="fr">Français</option>
    <option value="es">Español</option>
  </select>
</template>

<script>
export default {
  data() {
    return {
      currentLanguage: this.$i18n.locale,
    };
  },
  methods: {
    changeLanguage(event) {
      const language = event.target.value;
      this.$i18n.locale = language;
      localStorage.setItem('locale', language);
      this.currentLanguage = language;
    }
  },
  created() {
    const savedLanguage = localStorage.getItem('locale');
    if (savedLanguage) {
      this.$i18n.locale = savedLanguage;
      this.currentLanguage = savedLanguage;
    }
  }
};
</script>

<style scoped>
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

select:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
</style>
