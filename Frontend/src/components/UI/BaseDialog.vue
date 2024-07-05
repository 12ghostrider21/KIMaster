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
    position: fixed;
  width: 80%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  border-radius: 12px;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  padding: 0;
  margin: 0;
  }

  header {
    background-color: white;
    color: black;
    width: 100%;
    padding: 1rem;
  }

  header h2 {
    margin: 0;
  }

  section {
    padding: 1rem;
  }

  menu {
    padding: 1rem;
    display: flex;
    justify-content: flex-end;
    margin: 0;
  }

  @media (min-width: 768px) {
    dialog {
      left: calc(50% - 20rem);
      width: 40rem;
    }
  }</style>
