<?php

$a = new Swoole\Database\MysqliConfig();
$a->withHost('106.14.153.173');



$b = new Swoole\Database\MysqliPool($a);
// var_dump(serialize($b));
use Opis\Closure\SerializableClosure;
$wrapper = new SerializableClosure($b);
var_dump(serialize($wrapper));