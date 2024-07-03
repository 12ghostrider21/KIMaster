import { createStore } from 'vuex';
import * as ENUMS from '../components/enums.js';

export default createStore({
    state: {
        socket: null,
        messages: [],
        lobbyKey: null,
        game: null,
        position: "p1",
        positionsInLobby:[false,false,0], //Occupied Positions, 0=p1 1=p2, 2= number of Spectators
        imagesrc: null,
        images:[],
        inLobby: false,
        popup: null,
        notif: null,
        gameReady: false,
        gameOver: false,
        gameActive: false,
        currentImageIndex:-1,
        turn:0, //Turn of the Game
        playerTurn:1, //Which Player is currently active 1 for Player 1
        playerWon:0, //WhichPlayer Won
        isValidMoveImage:false,
        callPos:false,
        invalidMoveObserver:false,
        skipMove:false,
    },
    mutations: {

        setPositionsInLobby(state,{ p1, p2, sp }) {
            state.positionsInLobby[0]=p1;
            state.positionsInLobby[1]=p2;
            state.positionsInLobby[2]=sp;
        },
        setCallPos(state) {
            state.callPos=!state.callPos;
        },
        setSkipMove(state,skipMove) {
            state.skipMove=skipMove;
        },
        setInvalidMoveMade(state,invalidMoveObserver) {
            state.invalidMoveObserver= !state.invalidMoveObserver;
        },

        setCurrentImageIndex(state, currentImageIndex) {
            state.currentImageIndex = currentImageIndex;
        },
        setWebSocket(state, socket) {
            state.socket = socket;
        },
        addMessage(state, message) {
            state.messages.push(message);
        },

        addImages(state, image) {
            state.images.push(image);
        },
        
        newImages(state) {
            state.images= [];
        },
        setLobbyKey(state, lobbyKey) {
            state.lobbyKey = lobbyKey;
        },
        setGame(state, game) {
            state.game = game;
        },
        setInLobby(state, inLobby) {
            state.inLobby = inLobby;
        },
        setPosition(state, position) { // Mutation to set position
            state.position = position;
        },
        setGameReady(state, gameReady) { 
            state.gameReady = gameReady;
        },
        setTurn(state, turn) { 
            state.turn = turn;
        },
        setImagesrc(state, imagesrc) {
            state.imagesrc = imagesrc;
        },
        setPopup(state, popup) {
            state.popup = popup;
        },
        setNotif(state, notif) {
            state.notif = notif;
        },
        setGameOver(state, gameOver) {
            state.gameOver = gameOver;
        },
        setGameActive(state, gameActive) {  // Added mutation to set gameActive
            state.gameActive = gameActive;
        },

        setPlayerWon(state, playerWon) {
            state.playerWon = playerWon;
        },
        setIsValidMoveImage(state, isValidMoveImage){
            state.isValidMoveImage=isValidMoveImage;
        },
    },
    actions: {

        updatePosition({ commit }, position) {
            commit('setPosition', position);
        },

        changePrevImage({ commit, state }) {
            if (state.currentImageIndex > 0) {
                commit("setImagesrc", URL.createObjectURL(state.images[state.currentImageIndex - 1]));
                commit("setCurrentImageIndex", state.currentImageIndex - 1);
            }
        },
        changeNextImage({ commit, state }) {
            if (state.currentImageIndex < state.images.length - 1) {
                commit("setImagesrc", URL.createObjectURL(state.images[state.currentImageIndex + 1]));
                commit("setCurrentImageIndex", state.currentImageIndex + 1);
            }
        },
        changeFirstImage({ commit, state }) {
            if (state.images.length > 0) {
                commit("setImagesrc", URL.createObjectURL(state.images[0]));
                commit("setCurrentImageIndex", 0);
            }
        },
        changeLastImage({ commit, state }) {
            const lastIndex = state.images.length - 1;
            if (lastIndex >= 0) {
                commit("setImagesrc", URL.createObjectURL(state.images[lastIndex]));
                commit("setCurrentImageIndex", lastIndex);
            }
        },

        setPopup({ commit }, popup) {
            commit('setPopup', popup);
        },

        setNotif({ commit }, newNotif) {
            commit('setNotif', newNotif);
            setTimeout(() => {
                commit('setNotif', null);
            }, 10000);
        },

        setGame({ commit }, game) {
            commit('setGame', game);
            console.log("Game Set!")
        },

        initWebSocket({ commit,state }) {
            const currentUrl = window.location.href;

            let socket;
            if (currentUrl.startsWith('http://') && currentUrl.includes(':8086')) {
                let modifiedUrl = currentUrl.replace('http://', 'ws://').replace(':8086', ':8010/ws');
                if (modifiedUrl.endsWith('/')) {
                    modifiedUrl = modifiedUrl.slice(0, -1);
                }
                socket = new WebSocket(modifiedUrl); //TODO change to proper address, for now, it's hacked together
            } else {
                socket = new WebSocket('ws://localhost:8010/ws'); // Static URL if address not in the correct format
            }

            socket.onopen = () => {
                console.log('WebSocket is open now.');
            };
            socket.onclose = () => {
                console.log('WebSocket is closed now.');
            };
            socket.onmessage = (event) => {
                console.log('WebSocket message received:', event);
                commit('addMessage', event.data); // Commit the message to the store

                try {
                    const receivedJSONObject = JSON.parse(event.data);
                    if (receivedJSONObject.response_code != null) {
                        switch (receivedJSONObject.response_code) {
                            case 100: //Created Lobby
                                commit('setLobbyKey', receivedJSONObject.key);
                                commit('setPosition', "p1");
                                commit('setInLobby', true);
                                commit('setCallPos');
                                break;
                            case 101: //JoinedLobby
                                commit('setInLobby', true);
                                commit('setCallPos');
                                break;
                            case 102:  //LeftLobby
                               commit('setCallPos');
                            
                            break;
                            case 103: //Swapped Position
                                console.log("1")
                                commit('setCallPos');
                                break;
                            case 104:   
                                commit('setPosition', receivedJSONObject.pos);
                                break;
                            case 105: //LobbyStatus
                                commit('setGameReady', receivedJSONObject.GameClient);
                                commit('setPositionsInLobby', {
                                    p1: receivedJSONObject.P1,
                                    p2: receivedJSONObject.P2,
                                    sp: receivedJSONObject.Spectators
                                });
                                break;
                            case 150: 
                            case 151:
                            case 152: 
                                commit('setNotif', ENUMS.notifStatus.LOBBYJOINFAIL) //Lobby Join failed
                                break;
                            case 153: //LobbyStatus || LobbyPos client doesn't exist
                                commit('setLobbyKey', null);
                                commit('setInLobby', false);
                                commit('setGameReady',false);
                                break;
                            case 154:
                            case 155: commit('setNotif', ENUMS.notifStatus.POSOCCUPIED);
                                      commit('setCallPos');
                                break;
                            case 157: //Game not started, wrong amount of player
                                commit('setNotif', ENUMS.notifStatus.NOTENOUGHPLAYERS);
                                break;
                            
                            case 200: //Game has started
                                commit('setGame', receivedJSONObject.game);
                                commit('setCurrentImageIndex',-1);
                                commit('newImages');
                                commit('setPopup',null);
                                commit('setGameActive', true);
                               
                                break;
                            case 202: //Game is over
                                commit('setGameOver', true);
                                commit('setGameActive', false);
                                commit('setPlayerWon', receivedJSONObject.result);
                                commit('setTurn',receivedJSONObject.turn);
                                commit('setPopup',ENUMS.popUpStatus.GAMEOVER);
                                break;
                            case 207:
                                break;
                            case 208:
                                commit('setIsValidMoveImage', true);
                                 if (true){
                                    if (receivedJSONObject.moves.includes("36")){
                                        commit('setSkipMove',true);
                                        commit('setNotif',ENUMS.notifStatus.SKIPMOVE)}
                                    else commit('setSkipMove',false); //For Special case no avaiable Move on Othello Board to skip a turn
                                    };
                                break;
                            case 209:
                                commit('setCurrentImageIndex', state.currentImageIndex - 3); // Set to the second to last image index
                                state.images.pop();
                                state.images.pop();
                                state.images.pop();
                                break;
                            case 210: //Surrender
                                commit('setGameOver', true);
                                commit('setGameActive', false);
                                commit('setPlayerWon', receivedJSONObject.result)
                                commit('setPopup',ENUMS.popUpStatus.GAMEOVER);
                                break;
                            case 256:
                                commit('setInvalidMoveMade',true);
                                break;
                        }
                    }
                } catch (e) {
                    const blob = new Blob([event.data], { type: 'image/png' });


                    console.log("ImageIndex: " +state.currentImageIndex + "ImagesLength:" + state.images.length);
                    if (state.images.length===0||state.currentImageIndex === state.images.length-1) {
                        const url = URL.createObjectURL(blob);
                        commit('setImagesrc', url);

                    }
                    if (!state.isValidMoveImage) { //TODO: Better more reliable Solution?
                    commit('addImages',blob);
                    commit('setCurrentImageIndex', state.currentImageIndex+1)}
                    else { commit('setIsValidMoveImage', false);}
                }
            };

            commit('setWebSocket', socket);
        },
        sendWebSocketMessage({ state }, message) {
            if (state.socket && state.socket.readyState === WebSocket.OPEN) {
                state.socket.send(message);
            } else {
                console.error('WebSocket is not open.');
            }
        },
    },
    getters: {
        websocket: (state) => state.socket,
        messages: (state) => state.messages,
        images: (state) => state.images,
        lobbyKey: (state) => state.lobbyKey,
        game: (state) => state.game,
        position: (state) => state.position,
        imageSrc: (state) => state.imagesrc,
        popup: (state) => state.popup,
        gameReady: (state) => state.gameReady,
        gameOver: (state) => state.gameOver,
        gameActive: (state) => state.gameActive,  
        inLobby: (state) => state.inLobby,
        playerWon: (state) => state.playerWon,
        playerTurn: (state) => state.playerTurn,
        turn: (state) => state.turn,
        notif:(state) => state.notif,
        currentImageIndex:(state) => state.currentImageIndex,
        isValidMoveImage:(state) => state.isValidMoveImage,
        callPos:(state) => state.callPos, 
        invalidMoveObserver:(state) => state.invalidMoveObserver,
        positionsInLobby:(state) => state.positionsInLobby,
        skipMove:(state) => state.skipMove,
    },
});
