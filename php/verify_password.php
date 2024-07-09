<?php
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $inputString = isset($_POST['userInput']) ? $_POST['userInput'] : '';

    // Call Python script with inputString
    $command = "/usr/bin/python3 ../cgi-bin/retrieve_password_sha256.py '$inputString'";
    $output = shell_exec($command);

    echo $output; // Output from Python script (JSON response)
} else {
    http_response_code(405);
    echo json_encode(['match' => false, 'error' => 'Invalid request method']);
}
?>
