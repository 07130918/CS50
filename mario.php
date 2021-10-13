<?php
function main() {
    echo 'height: ';
    $height = trim(fgets(STDIN));
    return draw($height);
}

function draw(int $h) {
    // 再帰では絶対にbascaseを忘れない
    if ($h === 0) return;

    draw($h - 1);
    for ($i=0; $i < $h; $i++) {
        echo "■";
    }
    echo PHP_EOL;
}

main();
?>
