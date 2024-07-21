<template>
  <base-card>
    <div class="instructions">
      <h1>{{ $t('instructions.instruction_title') }}</h1>
      <section>
        <h1>{{ $t('instructions.introduction.title') }}</h1>
        <p>{{ $t('instructions.introduction.description1') }}</p>
        <p>{{ $t('instructions.introduction.description2') }}</p>
        <p>{{ $t('instructions.introduction.description3') }}</p>
      </section>

      <section>
        <h1>{{ $t('instructions.requirements.title') }}</h1>
        <ul>
          <li>{{ $t('instructions.requirements.network_access') }}</li>
          <li>{{ $t('instructions.requirements.websocket_uri_title') }}</li>
          <p>{{ $t('instructions.requirements.websocket_uri') }}</p>
          <li>{{ $t('instructions.requirements.browser_url_title') }}</li>
          <p>{{ $t('instructions.requirements.browser_url') }}</p>
          <li>{{ $t('instructions.requirements.message_format_title') }}</li>
          <p>{{ $t('instructions.requirements.message_format') }}</p>
          <li>{{ $t('instructions.requirements.documentation_title') }}</li>
          <p>{{ $t('instructions.requirements.documentation') }}</p>
        </ul>
      </section>

      <section>
        <h1>{{ $t('instructions.webSocketConnection.title') }}</h1>
        <h3>{{ $t('instructions.webSocketConnection.step1.title') }}</h3>
        <ul>
          <h4>{{ $t('instructions.webSocketConnection.step1.vpn') }}</h4>
          <li>{{ $t('instructions.webSocketConnection.step1.vpn_description') }}
            <a href="https://www.thm.de/its/campusnetz/vpn.html" target="_blank"> {{ $t('instructions.webSocketConnection.step1.vpn_link') }}</a>
          </li>

          <h4>{{ $t('instructions.webSocketConnection.step1.eduroam') }}</h4>
          <li>{{ $t('instructions.webSocketConnection.step1.eduroam_description') }}
            <a href="https://www.thm.de/its/campusnetz/wlan/anleitungen.html" target="_blank">{{ $t('instructions.webSocketConnection.step1.eduroam_link') }}</a>
          </li>
        </ul>
        <h3>{{ $t('instructions.webSocketConnection.step2.title') }}</h3>
        <h4>{{ $t('instructions.webSocketConnection.step2.browser.title') }}</h4>
        <ul>
          <li>{{ $t('instructions.webSocketConnection.step2.browser.open_browser') }}</li>
          <li>{{ $t('instructions.webSocketConnection.step2.browser.enter_url') }}</li>
          <li>{{ $t('instructions.webSocketConnection.step2.browser.internal_network') }}</li>
        </ul>

        <h4>{{ $t('instructions.webSocketConnection.step2.connection_with_ProgrammingLanguage.title') }}</h4>
        <ul>
          <li>{{ $t('instructions.webSocketConnection.step2.connection_with_ProgrammingLanguage.install_python') }}</li>
          <li>{{ $t('instructions.webSocketConnection.step2.connection_with_ProgrammingLanguage.install_webSocket') }}</li>
          <li>{{ $t('instructions.webSocketConnection.step2.connection_with_ProgrammingLanguage.pip_command') }}</li>
         
        </ul>
        
        <h4>{{ $t('instructions.webSocketConnection.step2.connection_with_ProgrammingLanguage.connection_code') }}</h4>
        <ul>
          <li>
             <a href="https://github.com/12ghostrider21/Plattform-fuer-Vergleich-von-Spiele-KIs/blob/rework/External/Python/kim_interface.py" target="_blank">{{ $t('instructions.webSocketConnection.step2.connection_with_ProgrammingLanguage.connection_code') }}</a>
         </li>
          <li>
             <a href="https://github.com/12ghostrider21/Plattform-fuer-Vergleich-von-Spiele-KIs/blob/rework/External/Python/Kim_example.py" target="_blank">{{ $t('instructions.webSocketConnection.step2.connection_with_ProgrammingLanguage.sending_code') }}</a>
         </li>
       </ul>

        <prism language="python">
          <pre><code>{{ $t('instructions.webSocketConnection.step2.connection_with_ProgrammingLanguage.example_code') }}</code></pre>
        </prism>
      </section>

      <section>
        <h3>{{ $t('instructions.webSocketConnection.step3.title') }}</h3>
        <ul>
          <li>{{ $t('instructions.webSocketConnection.step3.json_format') }}</li>
          <p>{{ $t('instructions.webSocketConnection.step3.json_format_descripton') }}</p>
          <li>{{ $t('instructions.webSocketConnection.step3.example_message') }}</li>
          <img :src="terminalScreenshot" alt="Example Terminal Command" class="example-image">
          <li>{{ $t('instructions.webSocketConnection.step3.send_message') }}</li>
          <p>{{ $t('instructions.webSocketConnection.step3.send_message_description') }}</p>
        </ul>

        <h3>{{ $t('instructions.webSocketConnection.step4.title') }}</h3>
        <ul>
          <li>{{ $t('instructions.webSocketConnection.step4.json_feedback') }}</li>
          <p>{{ $t('instructions.webSocketConnection.step4.feedback') }}</p>
          <li>{{ $t('instructions.webSocketConnection.step4.bytestream') }}</li>
          <p>{{ $t('instructions.webSocketConnection.step4.bytestream_receive') }}</p>
        </ul>
      </section>
    </div>
  </base-card>
  <footer-bar></footer-bar>
</template>

<script>
import Prism from 'vue-prism-component';

export default {
  name: 'Instructions',
  components: {
    Prism
  }
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
