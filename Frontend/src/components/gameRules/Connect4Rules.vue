<template>
  <div>
    <h2>{{ $t('rules.connect4.game_title') }}</h2>
    <p>{{ $t('rules.connect4.description') }}</p>

    <h3>{{ $t('rules.connect4.setup.title') }}</h3>
    <ul>
      <li>{{ $t('rules.connect4.setup.point1') }}</li>
      <li>{{ $t('rules.connect4.setup.point2') }}</li>
    </ul>

    <h3>{{ $t('rules.connect4.gameplay.title') }}</h3>
    <ul>
      <li>{{ $t('rules.connect4.gameplay.point1') }}</li>
      <li>{{ $t('rules.connect4.gameplay.point2') }}</li>
      <li>{{ $t('rules.connect4.gameplay.point3') }}</li>
    </ul>

    <h3>{{ $t('rules.connect4.endgame.title') }}</h3>
    <ul>
      <li>{{ $t('rules.connect4.endgame.point1') }}</li>
      <li>{{ $t('rules.connect4.endgame.point2') }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Connect4Rules'
};
</script>
