<template>
  <div class="dialog-overlay" @click="$emit('close')">
    <dialog open @click.stop>
      <header>
        <slot name="header">
          <h2>{{ title }}</h2>
        </slot>
      </header>
      <section>
        <slot></slot>
      </section>
      <menu>
        <slot name="actions">
          <base-button @click="$emit('close')">Close</base-button>
        </slot>
      </menu>
    </dialog>
  </div>
</template>

<script>
/**
* Reusable Pop Up Object. Implement in such a way that clicking outside the PopUp closes it.
* @module BaseDialog 
*/

export default {
  props: {
    title: {
      type: String,
      required: false,
    },
  },
  emits: ["close"],
};
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.75);
  z-index: 10;
  display: flex;
  justify-content: center;
  align-items: center;
}

dialog {
  position: relative;
  width: 80%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  border-radius: 12px;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  padding: 0;
  margin: 0;
  background: white;
  display: flex;
  flex-direction: column;
  align-items: center;
}

header {
  background-color: white;
  color: black;
  width: 100%;
  padding: 1rem;
  text-align: center;
}

header h2 {
  margin: 0;
}

section {
  padding: 1rem;
  width: 100%;
  text-align: center;
}

menu {
  padding: 1rem;
  display: flex;
  justify-content: center;
  gap: 19px;
  width: 100%;
  margin: 0;
}

.dialog-content {
  display: flex;
  align-items: center; /* Zentriert den Inhalt vertikal */
  justify-content: center; /* Zentriert den Inhalt horizontal */
  gap: 20px; /* Abstand zwischen Bild und Buttons */
  height: 100%; /* Stellt sicher, dass der Container die volle Höhe hat */
}

.button-column {
  display: flex;
  flex-direction: column;
  gap: 19px; /* Abstand zwischen den Buttons */
  width: 75%;
  align-items: center; /* Zentriert die Buttons innerhalb der Spalte */
}

.button-column base-button {
  width: 100%; /* Setzt die Breite der Buttons auf 100% der Spaltenbreite */
  margin: 0.5rem 0; /* Vertikaler Abstand oben und unten */
}

@media (min-width: 768px) {
  dialog {
    width: 40rem;
  }
}
</style>
