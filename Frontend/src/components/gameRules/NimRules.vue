<template>
    <div>
      <h2>{{ $t('rules.nim.title') }}</h2>
      <p>{{ $t('rules.nim.description') }}</p>
  
      <h3>{{ $t('rules.nim.setup.title') }}</h3>
      <ul>
        <li>{{ $t('rules.nim.setup.point1') }}</li>
        <li>{{ $t('rules.nim.setup.point2') }}</li>
      </ul>
  
      <h3>{{ $t('rules.nim.gameplay.title') }}</h3>
      <ul>
        <li>{{ $t('rules.nim.gameplay.point1') }}</li>
        <li>{{ $t('rules.nim.gameplay.point2') }}</li>
        <li>{{ $t('rules.nim.gameplay.point3') }}</li>
        <li>{{ $t('rules.nim.gameplay.point4') }}</li>
      </ul>
  
      <h3>{{ $t('rules.nim.endgame.title') }}</h3>
      <ul>
        <li>{{ $t('rules.nim.endgame.point1') }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NimRules'
  };
  </script>
  