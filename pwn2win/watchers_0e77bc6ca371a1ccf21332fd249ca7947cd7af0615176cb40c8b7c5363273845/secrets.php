<?php

    # $ip
    $ip = $_SERVER['REMOTE_ADDR'];

    # recaptcha v2
    $recaptcha_site = "redacted";
    $recaptcha_secret = "redacted";

    # sandbox append
    $secret_dir = 'redacted';
    $secret_file = bin2hex(random_bytes(10)); 

    # sandbox directory
    $sandbox_dir = hash('sha256', ($ip . $secret_dir));
    $sandbox_file = substr(hash('sha256', ($ip . $secret_file)), 1, 12);

    $file_home = 'pages/' . $sandbox_dir . '/' . $sandbox_file . '-home.html';
    $file_about = 'pages/' . $sandbox_dir . '/' . $sandbox_file . '-about.html';
    $file_contact = 'pages/' . $sandbox_dir . '/' . $sandbox_file . '-contact.html';
    $dir = 'pages/' . $sandbox_dir;