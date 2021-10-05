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
$anser = binary_search($numbers, $target);

echo "ターゲット:{$anser[0]}", PHP_EOL;
echo "試行回数:{$anser[1]}", PHP_EOL;
?>
