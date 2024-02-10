<?php
$servername = "localhost";
$username = "root";
$dbPassword = ""; // Change this to your actual database password
$database = "recjump_data_baze";

// Create connection
$conn = new mysqli($servername, $username, $dbPassword, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if the form was submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $nickname = $_POST['nickname'];
    $email = $_POST['email'];
    $password = $_POST['password'];

    // Hash the password
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    // Prepare SQL statement to check if the nickname already exists
    $stmt = $conn->prepare("SELECT * FROM accounts WHERE nickname = ?");
    $stmt->bind_param("s", $nickname);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
    $error_nick_exist = "nick is exist";
    header("Location: registration.php?error_nick_exist=$error_nick_exist");
    exit;
    } else {
        // Prepare and bind SQL statement for inserting new user
        $stmt = $conn->prepare("INSERT INTO accounts (nickname, email, password) VALUES (?, ?, ?)");
        $stmt->bind_param("sss", $nickname, $email, $hashed_password);

        // Execute the statement
        if ($stmt->execute() === TRUE) {
            echo "Registration successful.";
        } else {
            header('Location: registration.html');
            echo "Error: " . $stmt->error;
        }
    }

    // Close statement
    $stmt->close();
}

// Close connection
$conn->close();

// Redirect user
header('Location: connect.php');
exit; // Ensure that script execution stops after redirect
?>