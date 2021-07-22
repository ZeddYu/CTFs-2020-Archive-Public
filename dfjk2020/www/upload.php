<?php
require_once('classes.php');
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload</title>
</head>
<center>
<form action="" method="post" enctype="multipart/form-data" style="margin-top: 200px">
    <h2>来尽情地上传我吧</h2>
    <div>
        <input type="file" name="file" id="file" />
    </div>
    <div class="text-right mt-4">
        <button type="submit">SUBMIT</button>
</center>
</html>
<?php
$user=new User();
$user->upload();
?>