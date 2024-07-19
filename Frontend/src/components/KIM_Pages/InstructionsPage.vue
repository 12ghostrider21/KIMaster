<template>
    <div class="instructions">
      <h1>{{ $t('instructions.instruction_title') }}</h1>
      <section>
        <h2>{{ $t('instructions.instruction.title') }}</h2>
        <p>{{ $t('instructions.introduction.description1') }}</p>
        <p>{{ $t('instructions.introduction.description2') }}</p>
        <p>{{ $t('instructions.introduction.description3') }}</p>
      </section>

      <section>
        <h2>{{ $t('instructions.requirements.title') }}</h2>
        <ul>
          <li>{{ $t('instructions.requirements.network_access') }}</li>
          <li>{{ $t('instructions.requirements.websocket_uri') }}</li>
          <li>{{ $t('instructions.requirements.browser_url') }}</li>
          <li>{{ $t('instructions.requirements.message_format') }}</li>
          <li>{{ $t('instructions.requirements.documentation') }}</li>
        </ul>
      </section>

      <section>
        <h2>{{ $t('instructions.webSocketConnection.title') }}</h2>
        <h3>{{ $t('instructions.webSocketConnection.step1.title') }}</h3>
        <ul>
          <li>{{ $t('instructions.webSocketConnection.vpn') }}</li>
          <li>{{ $t('instructions.webSocketConnection.eduroam') }}</li>
        </ul>
        <h3>{{ $t('instructions.webSocketConnection.step2.title') }}</h3>
        <h4>{{ $t('instructions.webSocketConnection.step2.browser.title') }}</h4>
        <ul>
           <li>{{ $t('instructions.webSocketConnection.step2.browser.open_browser') }}</li>
           <li>{{ $t('instructions.webSocketConnection.step2.browser.enter_url') }}</li>
           <li>{{ $t('instructions.webSocketConnection.step2.browser.internal_network') }}</li>
      </ul>

      <h4>{{ $t('instructions.connection_with_ProgrammingLanguage.title') }}</h4>
      <ul>
        <li>{{ $t('instructions.webSocketConnection.step2.connection_with_ProgrammingLanguage.install_python') }}</li>
        <li>{{ $t('instructions.webSocketConnection.step2.connection_with_ProgrammingLanguage.install_webSocket ') }}</li>
        <li>{{ $t('instructions.webSocketConnection.step2.connection_with_ProgrammingLanguage.pip_command') }}</li>
        <li>{{ $t('instructions.webSocketConnection.step2.connection_with_ProgrammingLanguage.connection_code') }}</li>
      </ul>

      <prism language="python">
        {{ $t('instructions.webSocketConnection.step2.connection_with_ProgrammingLanguage.example_code') }}
      </prism>
      </section>

      


    </div>
    <footer-bar></footer-bar>
  </template>

  <script>
  import Prism from 'vue-prism-component';
  import 'prismjs';
  import 'prismjs/themes/prism.css';

  export default {
    name:'Instructions'
    
  };
  </script>

<style scoped>
.instructions {
  max-height: 80vh; /* Set the maximum height */
  overflow-y: auto; /* Enable vertical scrolling */
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  border-radius: 8px;
}

.instructions h1,
.instructions h2,
.instructions h3,
.instructions h4 {
  margin-top: 20px;
}

.instructions ul {
  padding-left: 20px;
}

.instructions p {
  margin-bottom: 10px;
}

prism {
  display: block;
  background: #f5f2f0;
  padding: 10px;
  border-radius: 8px;
  overflow-x: auto; /* Enable horizontal scrolling */
  max-width: 100%; /* Ensure it doesn't exceed the container width */
}
</style>