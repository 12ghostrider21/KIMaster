<template>
  <div>
    <h2>{{ $t('rules.tic_tac_toe.game_title') }}</h2>
    <p>{{ $t('rules.tic_tac_toe.description') }}</p>

    <h3>{{ $t('rules.tic_tac_toe.setup.title') }}</h3>
    <ul>
      <li>{{ $t('rules.tic_tac_toe.setup.point1') }}</li>
      <li>{{ $t('rules.tic_tac_toe.setup.point2') }}</li>
    </ul>

    <h3>{{ $t('rules.tic_tac_toe.gameplay.title') }}</h3>
    <ul>
      <li>{{ $t('rules.tic_tac_toe.gameplay.point1') }}</li>
      <li>{{ $t('rules.tic_tac_toe.gameplay.point2') }}</li>
    </ul>

    <h3>{{ $t('rules.tic_tac_toe.endgame.title') }}</h3>
    <ul>
      <li>{{ $t('rules.tic_tac_toe.endgame.point1') }}</li>
      <li>{{ $t('rules.tic_tac_toe.endgame.point2') }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'TicTacToeRules'
};
</script>

<style scoped>

</style>
