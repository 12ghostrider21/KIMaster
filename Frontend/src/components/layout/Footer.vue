<template>
  <footer>
    <!-- External link to the THM website -->
    <a href="https://www.thm.de">THM</a>

    <!-- Router link to the 'about' page -->
    <RouterLink :to="{ name: 'about' }">{{ $t('footer.datenschutz') }}</RouterLink>

    <!-- Router link to the 'impressum' page -->
    <RouterLink :to="{ name: 'impressum' }">{{ $t('footer.impressum') }}</RouterLink>
  </footer>
</template>

<script>
/**
 * Footer component that includes links for navigation and external sites.
 * 
 * @component
 */
export default {
  name: 'Footer'
}
</script>

<style scoped>
/* Styles for the footer element */
footer {
  width: 100%; /* Full width of the container */
  bottom: 0; /* Fixed at the bottom of the viewport */
  display: flex; /* Flexbox layout for the footer */
  justify-content: center; /* Center items horizontally */
  align-items: center; /* Center items vertically */
  padding: 10px; /* Padding inside the footer */
  background-color: #f8f9fa; /* Light background color */
  box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1); /* Subtle shadow effect */
}

/* Styles for anchor tags within the footer */
footer a {
  color: green; /* Text color for links */
  text-decoration: none; /* No underline for links */
  margin-left: 30px; /* Space between links */
}

/* Styles for anchor tags on hover */
footer a:hover {
  color: #007bff; /* Text color on hover */
}
</style>
