<?php
// コラッツ予想を再帰で計算

function collatz(int $n) {
    if ($n === 1) return 0;

    if ($n % 2 === 0) {
        return 1 + collatz($n/2);
    } else {
        return 1 + collatz($n*3 + 1);
    }
}

echo "1に収束するまでにかかったstep数:", collatz(10), PHP_EOL;
?>
 