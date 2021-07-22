<?php
require_once('classes.php');
?>

<!DOCTYPE html>
<html lang="en">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
<title>login</title>
<center>
<div>
    <!--或许这就是硬核前端吧-->
	<form  action="login.php" method="post" style="margin-top: 200px">
		<h2>别看了，你登不上</h2>
        <br>
        		<input type="text" name="username" placeholder="UserName" required>
        <br>
		<input type="password"  name="password" placeholder="password" required>
		<br>
		<button type="submit">登录</button>
		<br>
		<br>
		<br>
<?php 
$user=new user();
if(isset($_POST['username'])){
	if(preg_match("/union|select|drop|delete|insert|\#|\%|\`|\@|\\\\/i", $_POST['username'])){
		die("<br>为什么不肯尝试点别的东西呢？");
	}
	if(preg_match("/union|select|drop|delete|insert|\#|\%|\`|\@|\\\\/i", $_POST['password'])){
		die("<br>为什么不肯尝试点别的东西呢？");
	}
	$user->login();
}
?>
	</form>
</center>

</html>