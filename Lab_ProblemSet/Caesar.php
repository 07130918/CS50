<?php
// シーザー暗号
function main(int $key): void {
    $key %= 26;
    echo 'plaintext: ';
    $word = trim(fgets(STDIN));
    $alphabet = range('a', 'z');
    $ciphertext = '';

    for ($i=0; $i < strlen($word); $i++) {
        if (!ctype_alpha($word[$i])) {
            $ciphertext .= $word[$i];
            continue;
        }

        for ($j = 0; $j < count($alphabet); $j++) {
            if ($alphabet[$j] === $word[$i]) {
                $ciphertext .= $alphabet[$j + $key];
            } elseif (strtoupper($alphabet[$j]) === $word[$i]) {
                $ciphertext .= strtoupper($alphabet[$j + $key]);
            }
        }
    }
    echo 'ciphertext: ', $ciphertext, PHP_EOL;
}

if (count($argv) != 2) return 1;
if ($argv[1] < 1) return 1;

main($argv[1]);
?>
