<template>
    <div>
      <h2>{{ $t('rules.othello.title') }}</h2>
      <p>{{ $t('rules.othello.description') }}</p>
  
      <h3>{{ $t('rules.othello.setup.title') }}</h3>
      <ul>
        <li>{{ $t('rules.othello.setup.point1') }}</li>
        <li>{{ $t('rules.othello.setup.point2') }}</li>
        <li>{{ $t('rules.othello.setup.point3') }}</li>
      </ul>
  
      <h3>{{ $t('rules.othello.gameplay.title') }}</h3>
      <ul>
        <li>{{ $t('rules.othello.gameplay.point1') }}</li>
        <li>{{ $t('rules.othello.gameplay.point2') }}</li>
        <li>{{ $t('rules.othello.gameplay.point3') }}</li>
        <li>{{ $t('rules.othello.gameplay.point4') }}</li>
      </ul>
  
      <h3>{{ $t('rules.othello.endgame.title') }}</h3>
      <ul>
        <li>{{ $t('rules.othello.endgame.point1') }}</li>
        <li>{{ $t('rules.othello.endgame.point2') }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'OthelloRules'
  };
  </script>
  