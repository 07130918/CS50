<?php
function main(): void {
    echo 'Player 1:';
    $word1 = trim(fgets(STDIN));
    echo 'Player 2:';
    $word2 = trim(fgets(STDIN));
    $score1 = compute_score($word1);
    $score2 = compute_score($word2);

    if ($score1 > $score2) {
        echo 'Player 1 wins!', PHP_EOL;
    } elseif ($score1  < $score2) {
        echo 'Player 2 wins!', PHP_EOL;
    } else {
        echo 'Tie!', PHP_EOL;
    }
}

function compute_score(string $word): int {
    $POINTS = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 0];
    $alphabet = range('a', 'z');
    $word = strtolower($word);
    $score = 0;
    for ($i=0; $i < strlen($word); $i++) {
        for ($j=0; $j < count($alphabet); $j++) {
            if ($alphabet[$j] === $word[$i]) {
                $score += $POINTS[$j];
            }
        }
    }
    return $score;
}

main();
?>
