<template>
  <div>
    <h2>Vier Gewinnt Regeln</h2>
    <p>
      Vier Gewinnt ist ein Zwei-Personen-Spiel, bei dem die Spieler abwechselnd
      einen Stein ihrer Farbe in eine der sieben Spalten des Gitters fallen
      lassen. Das Ziel ist es, als Erster vier Steine in einer Reihe zu haben,
      sei es horizontal, vertikal oder diagonal.
    </p>

    <h3>Spielvorbereitung</h3>
    <ul>
      <li>Das Spielbrett besteht aus 7 Spalten und 6 Reihen.</li>
      <li>
        Jeder Spieler wählt eine Farbe und erhält eine unbegrenzte Anzahl an
        Steinen in dieser Farbe.
      </li>
    </ul>

    <h3>Spielablauf</h3>
    <ul>
      <li>
        Die Spieler lassen abwechselnd einen Stein in eine der Spalten fallen.
      </li>
      <li>Der Stein fällt in die tiefste verfügbare Position in der Spalte.</li>
      <li>
        Das Spiel geht weiter, bis ein Spieler vier seiner Steine in einer Reihe
        hat oder das Spielfeld voll ist.
      </li>
    </ul>

    <h3>Spielende</h3>
    <ul>
      <li>
        Ein Spieler gewinnt, wenn er vier Steine in einer Reihe hat (horizontal,
        vertikal oder diagonal).
      </li>
      <li>
        Das Spiel endet unentschieden, wenn das Spielfeld voll ist und kein
        Spieler vier Steine in einer Reihe hat.
      </li>
    </ul>
  </div>
</template>

<script>
export default {
    name : 'Connect4Rules'
    
}
</script>
