<?php
// 計算量 O(nlogn), Ω(nlogn)

function merge_sort(array $my_array)
{
    // 単一の要素が来たらそのまま返せば良い(単一要素はsort済み)
    if (count($my_array) === 1) return $my_array;

    // 配列を前半部分と後半部分に分割, (int)は小数以下切り捨て
    $mid = (int)(count($my_array) / 2);
    $left = array_slice($my_array, 0, $mid);
    $right = array_slice($my_array, $mid);
    $left = merge_sort($left);
    $right = merge_sort($right);

    echo "left:", join(",", $left), " right:", join(",", $right), PHP_EOL;
    return merge($left, $right);
}

function merge(array $left, array $right)
{
    $merged_array = [];

    while(!empty($left) && !empty($right))
    {
        // それぞれのはじめの要素を比較し小さい方を$merged_arrayに追加
        if ($left[0] > $right[0]) {
            // 配列にインデックス指定をしないと最後に追加される
            $merged_array[] = $right[0];
            $right = array_slice($right, 1);
        } else {
            $merged_array[] = $left[0];
            $left = array_slice($left, 1);
        }
    }

    // どちらかの配列が空になった時
    while(!empty($left)) // $rightが空
    {
        // echo "rightなし", PHP_EOL;
        $merged_array[] = $left[0];
        $left = array_slice($left, 1);
    }

    while(!empty($right)) // $leftが空
    {
        // echo "leftなし", PHP_EOL;
        $merged_array[] = $right[0];
        $right = array_slice($right, 1);
    }

    echo "merged_array: ", join(",", $merged_array), PHP_EOL;
    return $merged_array;
}

// $unsorted_array = [3, 2, 1, 4, 15, 18, 13, 99, 77, 66, 100, 0];
$unsorted_array = [5, 2, 1, 3, 6, 4];
echo join(",", merge_sort($unsorted_array)), PHP_EOL;
?>
