<?php

$a = 'Simple string';
function query($a) {
    echo $a;
}
query($a);

$b = $_GET['q'];
$sql = `SELECT * FROM table WHERE id = ${b}`;

?>