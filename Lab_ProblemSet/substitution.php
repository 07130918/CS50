<?php
function main(string $key): int {
    echo 'plaintext: ';
    $word = trim(fgets(STDIN));
    $alphabet = range('a', 'z');
    $ciphertext = '';

    for ($i=0; $i < strlen($word); $i++) {
        $alphabet_index = array_search(strtolower($word[$i]), $alphabet);
        if (ctype_lower($word[$i])) {
            $ciphertext .= strtolower($key[$alphabet_index]);
            continue;
        }
        $ciphertext .= $key[$alphabet_index];
    }
    echo 'ciphertext: ', $ciphertext, PHP_EOL;
    return 0;
}


if (strlen($argv[1]) != 26 ) return 1;

main($argv[1]);
// test key:YTNSHKVEFXRBAUQZCLWDMIPGJO
?>
