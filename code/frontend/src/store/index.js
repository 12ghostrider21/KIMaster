import { createStore } from 'vuex';

const store = createStore({
    state: {
        isPlaying: false
    },
    mutations: {
        togglePlay(state) {
            state.isPlaying = !state.isPlaying;
        }
    },
    getters: {
        isPlaying(state) {
            return state.isPlaying;
        }
    }
});

export default store;