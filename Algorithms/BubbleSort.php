<?php
// 計算量 O(n^2), Ω(n)
function bubble_sort($array) {
    for ($i=0; $i < count($array); $i++) {
        $swap_counter = 0;
        for ($j=0; $j < count($array) - 1; $j++) {
            if ($array[$j] > $array[$j + 1]) {
                $swap_counter++;
                $store = $array[$j + 1];
                $array[$j + 1] = $array[$j];
                $array[$j] = $store;
            }
        }
        if ($swap_counter === 0) {
            return $array;
        }
    }
}

$unsorted_array = [3, 2, 1, 4, 15, 18, 13, 99, 77, 66, 100, 0];
echo join(",", bubble_sort($unsorted_array)), PHP_EOL;
?>
