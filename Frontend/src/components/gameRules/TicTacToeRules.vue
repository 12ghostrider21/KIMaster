<template>
  <div>
    <h2>{{ $t('rules.tictactoe.game_title') }}</h2>
    <p>{{ $t('rules.tictactoe.description') }}</p>

    <h3>{{ $t('rules.tictactoe.setup.title') }}</h3>
    <ul>
      <li>{{ $t('rules.tictactoe.setup.point1') }}</li>
      <li>{{ $t('rules.tictactoe.setup.point2') }}</li>
    </ul>

    <h3>{{ $t('rules.tictactoe.gameplay.title') }}</h3>
    <ul>
      <li>{{ $t('rules.tictactoe.gameplay.point1') }}</li>
      <li>{{ $t('rules.tictactoe.gameplay.point2') }}</li>
    </ul>

    <h3>{{ $t('rules.tictactoe.endgame.title') }}</h3>
    <ul>
      <li>{{ $t('rules.tictactoe.endgame.point1') }}</li>
      <li>{{ $t('rules.tictactoe.endgame.point2') }}</li>
    </ul>
  </div>
</template>

<script>
   /**
  * Rules for Tic Tac Toe
  * @module gameRules 
  */
export default {
  name: 'TicTacToeRules'
};
</script>

<style scoped>

</style>
