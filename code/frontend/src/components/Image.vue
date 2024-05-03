<template>
  <div>
    <img
        ref="imageRef"
        class="imageRef"
        src="../assets/Images/tictactoe_board.png"
        alt="Tic Tac Toe Board"
        @click="trackMousePosition"
        style="display: block; margin: auto;"
    />
    <p v-if="clicked">Spielzug: {{ roundedMouseX }}, {{ roundedMouseY }}</p>
  </div>
</template>

<script>
import { onMounted, ref } from "vue";

export default {
  setup() {
    const mouseX = ref(0);
    const mouseY = ref(0);
    const relativeMouseX = ref(0);
    const relativeMouseY = ref(0);
    const roundedMouseX = ref(0);
    const roundedMouseY = ref(0);
    const gridsize = ref(3);
    const clicked = ref(false);
    const websocket = new WebSocket('ws://localhost:8000/ws');

    websocket.addEventListener('open', () => {
      console.log('Connected to WebSocket server');
    });

    websocket.addEventListener('message', (event) => {
      console.log('Message received:', event.data);
      const jsonObject = JSON.parse(event.data);
      roundedMouseX.value = jsonObject.x;
      roundedMouseY.value = jsonObject.y;
    });

    const sendMessage = (x, y) => {
      const message = JSON.stringify({ x, y });
      if (websocket.readyState === WebSocket.OPEN) {
        websocket.send(message);
      } else {
        console.error('WebSocket connection is not open.');
      }
    };

    const trackMousePosition = (event) => {
      mouseX.value = event.clientX;
      mouseY.value = event.clientY;
      const imageRect = imageRef.value.getBoundingClientRect();
      relativeMouseX.value = mouseX.value - imageRect.left;
      relativeMouseY.value = mouseY.value - imageRect.top;
      clicked.value = true;
      sendMessage( fitToGrid(relativeMouseX.value),fitToGrid(relativeMouseY.value));
    };

    const fitToGrid = (value) => {
      return Math.ceil(value / (imageRef.value.offsetWidth / gridsize.value));
    };

    const imageRef = ref(null);

    onMounted(() => {
      websocket.addEventListener('open', () => {
        console.log('Connected to WebSocket server');
      });
    });

    return { mouseX, mouseY, relativeMouseX, relativeMouseY, roundedMouseX, roundedMouseY, gridsize, clicked, trackMousePosition, imageRef };
  },
};
</script>

<style scoped>
.imageRef {
  width: 450px; /* Set the width to your desired size */
  height: auto; /* Maintain aspect ratio */
}
</style>

