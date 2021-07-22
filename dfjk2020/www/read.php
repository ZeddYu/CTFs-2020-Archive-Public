<?php
require_once('classes.php');
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Read</title>
</head>
<center>
   <form action="read.php" method="post" style="margin-top: 200px">
    <h2>本页面允许你读取一个文件QAQ</h2>
    <input type="text" name="filename" placeholder="Filename" method="POST">
    <br>
    <br>
    <a><?php
    $user=new User();
    $user->read();
    ?>
    </a>
   </form>
</center>
</html>