<?php
// 線形探索
// 計算量 O(n), Ω(1)

function linear_search(array $numbers, int $target) {
    for ($i=0; $i < count($numbers); $i++) {
        if ($numbers[$i] === $target) {
            return $numbers[$i];
        }
    }
    return "Not found";
};

$numbers = [2, 9, 8, 5, 6, 1, 3, 4, 10, 7];
echo linear_search($numbers, 5), PHP_EOL;
echo linear_search($numbers, 99), PHP_EOL;
?>
