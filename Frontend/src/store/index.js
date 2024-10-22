/**
 * The Central State Management System.
 * Is the sole connection to the Backend Logic
 * @module Store
 */
import { createStore } from 'vuex';
import * as ENUMS from '../components/enums.js';

/**
 * Returns the default state for the Vuex store.
 * @returns {Object} The default state object.
 */
const getDefaultState = () => {
    return {
        socket: null,
        socketConnected: false,
        connectionLost: true, // True here so reset doesn't close and popup again
        messages: [],
        lobbyKey: null,
        game: 'none',
        position: "p1",
        positionsInLobby: [false, false, 0],
        imagesrc: null,
        inLobby: false,
        popup: null,
        notif: null,
        gameReady: false,
        gameOver: false,
        gameActive: false,
        turn: 0,
        playerTurn: 1,
        playerWon: 0,
        isValidMoveImage: false,
        callPos: false,
        invalidMoveObserver: false,
        skipMove: false,
        blunder: [],
        yourTurn: false,
        playSound: false,
    };
};

export default createStore({
    /**
     * The Vuex store's state.
     * @type {Object}
     */
    state: {
        socket: null, // Stores the WebSocket
        socketConnected: false,
        connectionLost: false, // If the WebSocket connection cuts off for any reason, this is set to true
        messages: [],
        lobbyKey: null,
        game: null, // Which Game
        position: "p1", // Position of yourself in the Lobby
        positionsInLobby: [false, false, 0], // Occupied Positions, 0=p1 1=p2, 2= number of Spectators
        imagesrc: null, // Holds the currently active GameBoard
        inLobby: false,
        popup: null, // Activates PopUps
        notif: null, // Activates Notifications
        gameReady: false,
        gameOver: false,
        gameActive: false,
        turn: 0, // Turn of the Game
        playerTurn: 1, // Which Player is currently active 1 for Player 1
        playerWon: 0, // Which Player Won
        isValidMoveImage: false,
        callPos: false,
        blunders: [],
        invalidMoveObserver: false,
        skipMove: false,
        yourTurn: false,
        playSound: false,
    },
    mutations: {
        /**
         * Toggles the playSound state.
         * @param {Object} state - The current state.
         */
        playSound(state) {
            state.playSound = !state.playSound;
        },

        /**
         * Resets the state to its default values.
         * @param {Object} state - The current state.
         */
        resetState(state) {
            Object.assign(state, getDefaultState());
        },

        /**
         * Sets the positions in the lobby.
         * @param {Object} state - The current state.
         * @param {Object} payload - The positions to set.
         * @param {boolean} payload.p1 - Player 1 position.
         * @param {boolean} payload.p2 - Player 2 position.
         * @param {number} payload.sp - Number of spectators.
         */
        setPositionsInLobby(state, { p1, p2, sp }) {
            state.positionsInLobby[0] = p1;
            state.positionsInLobby[1] = p2;
            state.positionsInLobby[2] = sp;
        },

        /**
         * Sets the blunders.
         * @param {Object} state - The current state.
         * @param {Array} blunders - The list of blunders.
         */
        setBlunders(state, blunders) {
            state.blunders = blunders;
        },

        /**
         * Toggles the call position state.
         * @param {Object} state - The current state.
         */
        setCallPos(state) {
            state.callPos = !state.callPos;
        },

        /**
         * Sets the skip move state.
         * @param {Object} state - The current state.
         * @param {boolean} skipMove - Whether to skip the move.
         */
        setSkipMove(state, skipMove) {
            state.skipMove = skipMove;
        },

        /**
         * Toggles the invalid move observer state.
         * @param {Object} state - The current state.
         * @param {boolean} invalidMoveObserver - The state of the invalid move observer.
         */
        setInvalidMoveMade(state, invalidMoveObserver) {
            state.invalidMoveObserver = !state.invalidMoveObserver;
        },

        /**
         * Sets the current image index.
         * @param {Object} state - The current state.
         * @param {number} currentImageIndex - The current image index.
         */
        setCurrentImageIndex(state, currentImageIndex) {
            state.currentImageIndex = currentImageIndex;
        },

        /**
         * Sets the WebSocket connection.
         * @param {Object} state - The current state.
         * @param {WebSocket} socket - The WebSocket instance.
         */
        setWebSocket(state, socket) {
            state.socket = socket;
        },

        /**
         * Adds a message to the messages list.
         * @param {Object} state - The current state.
         * @param {string} message - The message to add.
         */
        addMessage(state, message) {
            state.messages.push(message);
        },

        /**
         * Sets the WebSocket connection status.
         * @param {Object} state - The current state.
         * @param {boolean} socketConnected - Whether the WebSocket is connected.
         */
        setSocketConnected(state, socketConnected) {
            state.socketConnected = socketConnected;
        },

        /**
         * Sets the connection lost status.
         * @param {Object} state - The current state.
         * @param {boolean} connectionLost - Whether the connection is lost.
         */
        setConnectionLost(state, connectionLost) {
            state.connectionLost = connectionLost;
        },

        /**
         * Sets the lobby key.
         * @param {Object} state - The current state.
         * @param {string} lobbyKey - The lobby key.
         */
        setLobbyKey(state, lobbyKey) {
            state.lobbyKey = lobbyKey;
        },

        /**
         * Sets the current game.
         * @param {Object} state - The current state.
         * @param {string} game - The current game.
         */
        setGame(state, game) {
            console.log("Game changed?");
            state.game = game;
        },

        /**
         * Sets whether the player is in the lobby.
         * @param {Object} state - The current state.
         * @param {boolean} inLobby - Whether the player is in the lobby.
         */
        setInLobby(state, inLobby) {
            state.inLobby = inLobby;
        },

        /**
         * Sets the player's position in the game.
         * @param {Object} state - The current state.
         * @param {string} position - The player's position.
         */
        setPosition(state, position) {
            state.position = position;
        },

        /**
         * Sets whether the game is ready.
         * @param {Object} state - The current state.
         * @param {boolean} gameReady - Whether the game is ready.
         */
        setGameReady(state, gameReady) {
            state.gameReady = gameReady;
        },

        /**
         * Sets the current turn.
         * @param {Object} state - The current state.
         * @param {number} turn - The current turn number.
         */
        setTurn(state, turn) {
            state.turn = turn;
        },

        /**
         * Sets the source of the image.
         * @param {Object} state - The current state.
         * @param {string} imagesrc - The image source URL.
         */
        setImagesrc(state, imagesrc) {
            state.imagesrc = imagesrc;
        },

        /**
         * Sets the popup state.
         * @param {Object} state - The current state.
         * @param {string|null} popup - The popup state.
         */
        setPopup(state, popup) {
            state.popup = popup;
        },

        /**
         * Sets the notification state.
         * @param {Object} state - The current state.
         * @param {string|null} notif - The notification state.
         */
        setNotif(state, notif) {
            state.notif = notif;
        },

        /**
         * Sets whether the game is over.
         * @param {Object} state - The current state.
         * @param {boolean} gameOver - Whether the game is over.
         */
        setGameOver(state, gameOver) {
            state.gameOver = gameOver;
        },

        /**
         * Sets whether the game is active.
         * @param {Object} state - The current state.
         * @param {boolean} gameActive - Whether the game is active.
         */
        setGameActive(state, gameActive) {
            state.gameActive = gameActive;
        },

        /**
         * Sets the player who won the game.
         * @param {Object} state - The current state.
         * @param {number} playerWon - The player number who won.
         */
        setPlayerWon(state, playerWon) {
            state.playerWon = playerWon;
        },

        /**
         * Sets whether the move image is valid.
         * @param {Object} state - The current state.
         * @param {boolean} isValidMoveImage - Whether the move image is valid.
         */
        setIsValidMoveImage(state, isValidMoveImage) {
            state.isValidMoveImage = isValidMoveImage;
        },

        /**
         * Sets whether it is the player's turn.
         * @param {Object} state - The current state.
         * @param {boolean} yourTurn - Whether it is the player's turn.
         */
        setYourTurn(state, yourTurn) {
            state.yourTurn = yourTurn;
        }
    },
    actions: {
        /**
         * Resets the state to its default values.
         * @param {Object} context - The Vuex context.
         * @param {Function} context.commit - The commit function.
         */
        resetState({ commit }) {
            commit('resetState');
        },

        /**
         * Updates the player's position.
         * @param {Object} context - The Vuex context.
         * @param {string} position - The new position.
         */
        updatePosition({ commit }, position) {
            commit('setPosition', position);
        },

        /**
         * Sets the popup state.
         * @param {Object} context - The Vuex context.
         * @param {string|null} popup - The popup state.
         */
        setPopup({ commit }, popup) {
            commit('setPopup', popup);
        },

        /**
         * Sets the notification state, needs to be cleared again in the Components
         * @param {Object} context - The Vuex context.
         * @param {string|null} newNotif - The notification state.
         */
        setNotif({ commit }, newNotif) {
            commit('setNotif', newNotif);

        },

        /**
         * Sets the current game.
         * @param {Object} context - The Vuex context.
         * @param {string} game - The current game.
         */
        setGame({ commit }, game) {
            commit('setGame', game);
        },

        /**
         * Initializes the WebSocket connection based on the current URL.
         * @param {Object} context - The Vuex context.
         * @param {Function} context.commit - The commit function.
         * @param {Object} context.state - The current state.
         */
        initWebSocket({ commit, state }) {
            commit('resetState');
            
            const currentUrl = window.location.href;
            let socket;

            if (currentUrl.startsWith('http://') && currentUrl.includes(':8086')) {
                let modifiedUrl = currentUrl.replace('http://', 'ws://').replace(':8086', ':8010/ws');
                if (modifiedUrl.endsWith('/')) {
                    modifiedUrl = modifiedUrl.slice(0, -1);
                }
                socket = new WebSocket(modifiedUrl); // When deployed on Local System
            } else {
                socket = new WebSocket('wss://kimaster.mni.thm.de/ws'); // Change to 'ws://localhost:8010/ws' when Locally deployed outside of the Docker File
            }

            socket.onopen = () => {
                console.log('WebSocket is open now.');
                commit("setSocketConnected", true);
                commit('setConnectionLost', false);
            };

            socket.onclose = () => {
                console.log('WebSocket is closed now.');
                commit('setConnectionLost', true);
            };

            socket.onerror = (error) => {
                console.log('WebSocketError? ' + error);
                commit('setConnectionLost', true);
            };

            socket.onmessage = (event) => {
                console.log('WebSocket message received:', event);
                commit('addMessage', event.data); // Commit the message to the store

                try {
                    const receivedJSONObject = JSON.parse(event.data);
                    if (receivedJSONObject.response_code != null) {
                        switch (receivedJSONObject.response_code) {
                            case 100: // Created Lobby
                                commit('setLobbyKey', receivedJSONObject.key);
                                commit('setPosition', "p1");
                                commit('setInLobby', true);
                                commit('setCallPos');
                                break;
                            case 101: // Joined Lobby
                                commit('setInLobby', true);
                                commit('setCallPos');
                                break;
                            case 102: // Left Lobby
                                commit('setCallPos');
                                break;
                            case 103: // Swapped Position
                                commit('setCallPos');
                                break;
                            case 104: // Current Position in Lobby
                                commit('setPosition', receivedJSONObject.pos);
                                break;
                            case 105: // Lobby Status
                                commit('setGameReady', receivedJSONObject.GameClient);
                                commit('setPositionsInLobby', {
                                    p1: receivedJSONObject.P1,
                                    p2: receivedJSONObject.P2,
                                    sp: receivedJSONObject.Spectators
                                });
                                commit('setGameActive', receivedJSONObject.GameRunning);
                                break;
                            case 150: 
                            case 151: 
                            case 152: 
                                commit('setNotif', ENUMS.notifStatus.LOBBYJOINFAIL); // Lobby Join failed
                                break;
                            case 153: // Lobby Status || Lobby Pos client doesn't exist
                                commit('setLobbyKey', null);
                                commit('setInLobby', false);
                                commit('setGameReady', false);
                                commit('setGameActive', false);
                                break;
                            case 154: 
                            case 155: // Lobby Swap Failed, position occupied
                                commit('setNotif', ENUMS.notifStatus.POSOCCUPIED);
                                commit('setCallPos');
                                break;
                            case 157: // Game not started, wrong amount of player
                                commit('setNotif', ENUMS.notifStatus.NOTENOUGHPLAYERS);
                                break;
                            case 200: // Game has started
                                if (receivedJSONObject.game != null) {
                                    commit('setGame', receivedJSONObject.game);
                                }
                                commit('setPopup', null);
                                commit('setGameActive', true);
                                commit('setGameOver', false);
                                break;
                            case 202: // Game is over
                                commit('setGameOver', true);
                                commit('setGameActive', false);
                                commit('setPlayerWon', receivedJSONObject.result);
                                commit('setTurn', receivedJSONObject.turn);
                                commit('setPopup', ENUMS.popUpStatus.GAMEOVER);
                                break;
                            case 207:
                                break;
                            case 208: 
                                // commit('setIsValidMoveImage', true);
                                if (state.game === ENUMS.games.OTHELLO) {
                                    if (receivedJSONObject.moves.includes("64") || receivedJSONObject.moves.includes(64)) {
                                        commit('setSkipMove', true);
                                        commit('setNotif', ENUMS.notifStatus.SKIPMOVE);
                                    } else {
                                        commit('setSkipMove', false); // For Special case no available Move on Othello Board to skip a turn
                                    }
                                }
                                break;
                            case 209:
                                // commit('setCurrentImageIndex', state.currentImageIndex - 3); // Set to the second to last image index
                                break;
                            case 210: // Surrender
                                commit('setGameOver', true);
                                commit('setGameActive', false);
                                commit('setTurn', receivedJSONObject.turn);
                                commit('setPlayerWon', receivedJSONObject.result);
                                commit('setPopup', ENUMS.popUpStatus.GAMEOVER);
                                break;
                            case 212: // Blunder
                                commit('setBlunders', receivedJSONObject.blunder);
                                if (state.blunders.length > 0) {
                                    commit('setPopup', ENUMS.popUpStatus.BLUNDER);
                                }
                                break;
                            case 218: // Currently active Player
                                commit('playSound');
                                commit('setYourTurn', state.position === "p1" && receivedJSONObject.cur_player == 1 || state.position === "p2" && receivedJSONObject.cur_player == -1);
                                break;
                            case 219: // KIM is making a move
                                commit('playSound');
                                commit('setYourTurn', false);
                                break;
                            case 256: // Invalid Move Made
                                commit('setInvalidMoveMade', true);
                                break;
                        }
                    }
                } catch (e) {
                    try {
                        const reader = new FileReader();
                        reader.onload = function() {
                            const arrayBuffer = reader.result;
                            const dataView = new DataView(arrayBuffer);
                            const pngSignature = [
                                0x89, 0x50, 0x4E, 0x47, 
                                0x0D, 0x0A, 0x1A, 0x0A
                            ];

                            // Check if the event.data starts with the PNG signature
                            let isPng = true;
                            for (let i = 0; i < pngSignature.length; i++) {
                                if (dataView.getUint8(i) !== pngSignature[i]) {
                                    isPng = false;
                                    break;
                                }
                            }

                            if (!isPng) {
                                throw new Error("Data is not a PNG file.");
                            }

                            const blob = new Blob([arrayBuffer], { type: 'image/png' });
                            console.log(event);

                            const url = URL.createObjectURL(blob);
                            commit('setImagesrc', url);
                        };

                        reader.onerror = function() {
                            throw new Error("Failed to read the Blob.");
                        };

                        reader.readAsArrayBuffer(event.data);
                    } catch (error) {
                        console.log(error);
                    }
                }
            };

            commit('setWebSocket', socket);
        },

        /**
         * Sends a message through the WebSocket connection.
         * @param {Object} context - The Vuex context.
         * @param {string} message - The message to be sent.
         */
        sendWebSocketMessage({ state }, message) {
            if (state.socket && state.socket.readyState === WebSocket.OPEN) {
                state.socket.send(message);
            } else {
                console.error('WebSocket is not open.');
            }
        },
    },
    getters: {
        /**
         * Gets the WebSocket instance.
         * @param {Object} state - The current state.
         * @returns {WebSocket|null} - The WebSocket instance.
         */
        websocket: (state) => state.socket,

        /**
         * Gets the messages received through the WebSocket.
         * @param {Object} state - The current state.
         * @returns {Array} - The array of messages.
         */
        messages: (state) => state.messages,

        /**
         * Gets the currently active image source.
         * @param {Object} state - The current state.
         * @returns {string|null} - The image source URL.
         */
        imageSrc: (state) => state.imagesrc,

        /**
         * Gets the lobby key.
         * @param {Object} state - The current state.
         * @returns {string|null} - The lobby key.
         */
        lobbyKey: (state) => state.lobbyKey,

        /**
         * Gets the current game.
         * @param {Object} state - The current state.
         * @returns {string|null} - The current game.
         */
        game: (state) => state.game,

        /**
         * Gets the player's position.
         * @param {Object} state - The current state.
         * @returns {string} - The player's position.
         */
        position: (state) => state.position,

        /**
         * Gets the popup state.
         * @param {Object} state - The current state.
         * @returns {string|null} - The popup state.
         */
        popup: (state) => state.popup,

        /**
         * Gets whether the game is ready.
         * @param {Object} state - The current state.
         * @returns {boolean} - Whether the game is ready.
         */
        gameReady: (state) => state.gameReady,

        /**
         * Gets whether the game is over.
         * @param {Object} state - The current state.
         * @returns {boolean} - Whether the game is over.
         */
        gameOver: (state) => state.gameOver,

        /**
         * Gets whether the game is active.
         * @param {Object} state - The current state.
         * @returns {boolean} - Whether the game is active.
         */
        gameActive: (state) => state.gameActive,

        /**
         * Gets whether the player is in the lobby.
         * @param {Object} state - The current state.
         * @returns {boolean} - Whether the player is in the lobby.
         */
        inLobby: (state) => state.inLobby,

        /**
         * Gets the player who won the game.
         * @param {Object} state - The current state.
         * @returns {number} - The player who won the game.
         */
        playerWon: (state) => state.playerWon,

        /**
         * Gets the current player's turn.
         * @param {Object} state - The current state.
         * @returns {number} - The current player's turn.
         */
        playerTurn: (state) => state.playerTurn,

        /**
         * Gets the current turn.
         * @param {Object} state - The current state.
         * @returns {number} - The current turn.
         */
        turn: (state) => state.turn,

        /**
         * Gets the notification state.
         * @param {Object} state - The current state.
         * @returns {string|null} - The notification state.
         */
        notif: (state) => state.notif,

        /**
         * Gets whether the move image is valid.
         * @param {Object} state - The current state.
         * @returns {boolean} - Whether the move image is valid.
         */
        isValidMoveImage: (state) => state.isValidMoveImage,

        /**
         * Gets the call position state.
         * @param {Object} state - The current state.
         * @returns {boolean} - The call position state.
         */
        callPos: (state) => state.callPos,

        /**
         * Gets the list of blunders.
         * @param {Object} state - The current state.
         * @returns {Array} - The list of blunders.
         */
        blunders: (state) => state.blunders,

        /**
         * Gets the invalid move observer state.
         * @param {Object} state - The current state.
         * @returns {boolean} - The invalid move observer state.
         */
        invalidMoveObserver: (state) => state.invalidMoveObserver,

        /**
         * Gets the positions in the lobby.
         * @param {Object} state - The current state.
         * @returns {Array} - The positions in the lobby.
         */
        positionsInLobby: (state) => state.positionsInLobby,

        /**
         * Gets whether to skip the move.
         * @param {Object} state - The current state.
         * @returns {boolean} - Whether to skip the move.
         */
        skipMove: (state) => state.skipMove,

        /**
         * Gets whether it is the player's turn.
         * @param {Object} state - The current state.
         * @returns {boolean} - Whether it is the player's turn.
         */
        yourTurn: (state) => state.yourTurn,

        /**
         * Gets whether the WebSocket connection is open.
         * @param {Object} state - The current state.
         * @returns {boolean} - Whether the WebSocket connection is open.
         */
        socketConnected: (state) => state.socketConnected,

        /**
         * Gets whether the WebSocket connection is lost.
         * @param {Object} state - The current state.
         * @returns {boolean} - Whether the WebSocket connection is lost.
         */
        connectionLost: (state) => state.connectionLost,

        /**
         * Gets whether to play sound.
         * @param {Object} state - The current state.
         * @returns {boolean} - Whether to play sound.
         */
        playSound: (state) => state.playSound,
    },
});
