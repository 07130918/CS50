<?php
// 選択ソート
// 計算量O(n^2)
function selectSort($numbers)
{
    for ($i = 0; $i < count($numbers) - 1; $i++) {
        $min = $numbers[$i];
        $num_index = $i;
        for ($j = $num_index + 1; $j < count($numbers); $j++) {
            if ($min > $numbers[$j]) {
                $num_index = $j;
                $min = $numbers[$j];
            }
        }
        $numbers[$num_index] = $numbers[$i];
        $numbers[$i] = $min;
    }
    return $numbers;
}

$numbers = [2, 9, 8, 5, 6, 1, 3, 4, 10, 7];
echo join(",", selectSort($numbers)), PHP_EOL;
?>
