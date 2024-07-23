<template>
    <div>
      <h2>{{ $t('rules.checkers.game_title') }}</h2>
  
      <p>{{ $t('rules.checkers.description') }}</p>
  
      <h3>{{ $t('rules.checkers.setup.title') }}</h3>
      <p>{{ $t('rules.checkers.setup.description') }}</p>
  
      <h3>{{ $t('rules.checkers.movement.title') }}</h3>
      <p>{{ $t('rules.checkers.movement.description') }}</p>
  
      <h3>{{ $t('rules.checkers.capturing.title') }}</h3>
      <p>{{ $t('rules.checkers.capturing.description1') }}</p>
      <p>{{ $t('rules.checkers.capturing.description2') }}</p>
      <p>{{ $t('rules.checkers.capturing.description3') }}</p>
  
      <h3>{{ $t('rules.checkers.queening.title') }}</h3>
      <p>{{ $t('rules.checkers.queening.description1') }}</p>
      <p>{{ $t('rules.checkers.queening.description2') }}</p>
  
      <h3>{{ $t('rules.checkers.endgame.title') }}</h3>
      <p>{{ $t('rules.checkers.endgame.description') }}</p>
  
      <h3>{{ $t('rules.checkers.draw.title') }}</h3>
      <p>{{ $t('rules.checkers.draw.description') }}</p>
      <ul>
        <li>{{ $t('rules.checkers.draw.point1') }}</li>
        <li>{{ $t('rules.checkers.draw.point2') }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  /**
  * Rules for Checkers
  * @module gameRules 
  */
  export default {
    name: 'CheckersRules'
  };
  </script>
  
  <style scoped>
  
  </style>
  