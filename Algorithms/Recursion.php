<?php
// 再帰関数
function fact(int $n):int {
    if ($n === 0 || $n === 1) return 1;

    return $n * fact($n - 1);
}

function fact2(int $n):int {
    $product = 1;
    while($n > 0) {
        $product *= $n;
        $n--;
    }
    return $product;
}

echo fact(5), PHP_EOL;
echo fact2(4), PHP_EOL;
?>
