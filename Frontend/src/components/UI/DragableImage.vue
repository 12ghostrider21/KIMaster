<template>
  <div
    :style="{ left: position.x + 'px', top: position.y + 'px', position: 'absolute' }"
    class="draggable"
    @mousedown="startDrag"
    @dblclick="handleClick"
  >
    <div class="blackbox">
      <img
        class="imageRef"
        ref="imageRef"
        v-if="imageSrc"
        :src="imageSrc"
        alt="Received Image"
      />
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import * as ENUMS from '../enums';
export default {
  data() {
    return {
      position: { x: 0, y: 0 },
      dragging: false,
      offset: { x: 0, y: 0 },
    };
  },
  computed: {
    ...mapGetters(["imageSrc","game"]),
    enums() { return ENUMS; }
  },
  methods: {
    
    startDrag(event) {
      this.dragging = true;
      this.offset.x = event.clientX - this.position.x;
      this.offset.y = event.clientY - this.position.y;
      document.addEventListener('mousemove', this.onDrag);
      document.addEventListener('mouseup', this.stopDrag);
    },
    onDrag(event) {
      if (this.dragging) {
        this.position.x = event.clientX - this.offset.x;
        this.position.y = event.clientY - this.offset.y;
      }
    },
    stopDrag() {
      this.dragging = false;
      document.removeEventListener('mousemove', this.onDrag);
      document.removeEventListener('mouseup', this.stopDrag);
    },
    handleClick() {
      this.$router.push({ name: 'play', params: { game: this.game }});
      
    },
  },
};
</script>

<style scoped>
.draggable {
  cursor: grab;
  user-select: none;
  position: relative;
}

.draggable:active {
  cursor: grabbing;
}

.blackbox {
  width: 250px; /*TODO Change to Dynamic size */
  height: 250px; 
  background-color: black;
  position: relative;
  overflow: hidden;
}

.imageRef {
  width: 100%;
  height: 100%;
  object-fit: contain; 
  pointer-events: none; 
  border: 2px solid black; 
}
</style>
