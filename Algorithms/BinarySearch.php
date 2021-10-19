<?php
// 二分探索
// 配列がソート済みであることが前提条件
// 計算量 O(logn), Ω(1)

function binary_search($numbers, $target) {
    $trials = 1; // 試行回数
    $low = 0; // 最小インデックス
    $high = count($numbers) - 1; // 最大インデックス

    while ($low <= $high) {
        $pivot = (int)(($low + $high) / 2); //中間のインデックス

        if ($numbers[$pivot] === $target) {
            return [$target, $trials];
        } elseif ($target > $numbers[$pivot]) {
            $low = $pivot + 1;
        } else { //elseif($target < $numbers[$pivot]) {
            $high = $pivot - 1;
        }
        $trials++;
    }

    return ["Not found", $trials];
}

$numbers = range(1, 100);
$target = 100;
$answer = binary_search($numbers, $target);

echo "binary_search execution", PHP_EOL;
echo "ターゲット:{$answer[0]}", PHP_EOL;
echo "試行回数:{$answer[1]}", PHP_EOL;


function binary_search_recursion(array $numbers, int $target) {
    // ターゲットに配列最大値より大きい自然数が来た時ガード
    if (count($numbers) === 1 && $numbers[0] != $target) return 1;

    $half = count($numbers) / 2;

    if ($numbers == null) {
        return 1;
    } elseif ($target < $numbers[$half]) {
        return binary_search_recursion(array_slice($numbers, 0, $half), $target);
    } elseif ($target > $numbers[$half]) {
        return binary_search_recursion(array_slice($numbers, $half), $target);
    } elseif ($target === $numbers[$half]) {
        return 0;
    }
}

$target = 1;
$answer = binary_search_recursion(range(1,10), $target);

echo "binary_search_recursion execution", PHP_EOL;
echo "ターゲット:{$target}", PHP_EOL;
echo "Response statement:{$answer}", PHP_EOL;

?>
