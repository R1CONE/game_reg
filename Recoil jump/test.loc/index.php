<?php
$servername = "localhost";
$username = "root";
$dbPassword = ""; 
$database = "recjump_data_baze";

// Create connection
$conn = new mysqli($servername, $username, $dbPassword, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if the form was submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['reg_account'])) {
        // Get form data
        $nickname = $_POST['nickname'];
        $email = $_POST['email'];
        $password = $_POST['password'];

        // Prepare SQL statement to check if the nickname already exists
        $stmt = $conn->prepare("SELECT * FROM accounts WHERE nickname = ?");
        $stmt->bind_param("s", $nickname);
        $stmt->execute();
        $result = $stmt->get_result();

        $stmt_1 = $conn->prepare("SELECT * FROM accounts WHERE email = ?");
        $stmt_1->bind_param("s", $email);
        $stmt_1->execute();
        $result_1 = $stmt_1->get_result();

        if ($result->num_rows > 0) {
            $error_nick_exist = "Nick is already taken.";
            header("Location: registration.php?error_nick_exist=$error_nick_exist");
            exit;
        } 
        
        if ($result_1->num_rows > 0) {
            $error_email_exist = "Email is already registered.";
            header("Location: registration.php?error_email_exist=$error_email_exist");
            exit;
        }
        
        // Close statement
        $stmt->close();
        $stmt_1->close();
        
        // Prepare and bind SQL statement for inserting new user
        $stmt = $conn->prepare("INSERT INTO accounts (nickname, email, password) VALUES (?, ?, ?)");
        $stmt->bind_param("sss", $nickname, $email, $password);

        // Execute the statement
        if ($stmt->execute() === TRUE) {
            echo "Registration successful.";
        } else {
            header('Location: registration.php');
            exit;
        }
    } elseif (isset($_POST['have_account'])) {
        header("Location: enter.php");
        exit;
    }
}

// Close connection
$conn->close();

// Redirect user
header('Location: connect.php');
exit; // Ensure that script execution stops after redirect
?>
