<?php
// Generates password and prints to command line

$password = 'pass';

// Hash the password using SHA-256
$hashed_password = hash('sha256', $password);

// Hash the password using bcrypt
// $hashed_password = password_hash($password, PASSWORD_DEFAULT);

echo $hashed_password;
?>
