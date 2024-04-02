<?php
// SQL Injection (SQLi) vulnerability
$username = $_POST['username'];
$password = $_POST['password'];
$query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
$result = mysqli_query($conn, $query);

// Cross-Site Scripting (XSS) vulnerability
echo "<h1>Welcome, $username!</h1>";

// Command Injection vulnerability
$cmd = $_GET['cmd'];
$output = shell_exec("ls $cmd");
echo "<pre>$output</pre>";

// File Inclusion vulnerability
$page = $_GET['page'];
include ($page . '.php');

# Prototype Pollution vulnerability
$data = $_GET['data'];
$array = [];
$array[$data] = 'tampered';
echo $array[$data];
?>