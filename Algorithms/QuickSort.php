<?php
// 計算量O(n^2), Ω(nlogn)
// 基準値を決めてそれより大きいか小さいかを繰り返す

function quick_sort(array $array): array {
    if (count($array) <= 1) return $array;

    // 基準点(ピボット)を決める
    $pivot = array_shift($array);
    $left = [];
    $right = [];

    for ($i=0; $i < count($array); $i++) {
        // ピボットより小さい数は左, 大きい数は右
        if ($array[$i] < $pivot) {
            $left[]  = $array[$i];
        } else {
            $right[] = $array[$i];
        }
    }
    // 左右のデータを再帰的にソートする
    return array_merge(quick_sort($left), [$pivot], quick_sort($right));
}

$unsorted_array = [5, 2, 1, 3, 6, 4];
echo join(",", quick_sort($unsorted_array)), PHP_EOL;
?>
