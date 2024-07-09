<?php
// Generates password and inserts directly into MySQL table 
// Database connection
$servername = "";
$username = "";
$password = "";
$dbname = "";
$port = 4253;

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname, $port);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Plain-text password
$plain_password = 'pass';

// Hash the password
$hashed_password = password_hash($plain_password, PASSWORD_DEFAULT);

// Insert the hashed password into the database
$sql = "INSERT INTO login_password (pass) VALUES ('$hashed_password')";

if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
