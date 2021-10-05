<?php
// 選択ソート
// 計算量O(n^2), Ω(n^2)
function selectSort($numbers)
{
    for ($i = 0; $i < count($numbers) - 1; $i++) {
        // 最小値を先頭に仮置き
        $min = $numbers[$i];
        $min_index = $i;
        for ($j = $min_index + 1; $j < count($numbers); $j++) {
            // 最小値が新たに発見された場合の数値とインデックスを記憶
            if ($min > $numbers[$j]) {
                $min_index = $j;
                $min = $numbers[$j];
            }
        }
        // 最小値と仮置きされていた先頭の数値を交換
        $numbers[$min_index] = $numbers[$i];
        $numbers[$i] = $min;
    }
    return $numbers;
}

$numbers = [2, 9, 8, 5, 6, 1, 3, 4, 10, 7];
echo join(",", selectSort($numbers)), PHP_EOL;
?>
