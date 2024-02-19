<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Registration Form</title>
<style>
    body {
        margin: 0;
        padding: 0;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .registration-container {
        text-align: center;
    }

    .input-group {
        margin-bottom: 10px;
    }

    .input-group input {
        width: 400px;
        padding: 12px;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 18px; /* Reduced font size for better aesthetics */
    }

    button {
        padding: 10px 20px; /* Adjusted padding for better button size */
        font-size: 16px; /* Reduced font size for better aesthetics */
        margin-bottom: 10px;
    }
</style>
</head>
<body>
<div class="registration-container">
    <form method="post" action="">
        <div class="input-group">
            <input type="text" name="nickname_email" placeholder="Nick-name or email">
        </div>
        <div class="input-group">
            <input type="password" name="password" placeholder="Password">
        </div>
        <button type="submit" name="reg_account">Enter</button>
        <button type="submit" name="restore_password">I don't remember password</button> <!-- Corrected the typo -->
    </form>
</div>
</body>
</html>

<?php
$servername = "localhost";
$username = "root";
$dbPassword = ""; 
$database = "recjump_data_baze";

$eror_text = "This password uncorrect";

// Create connection
$conn = new mysqli($servername, $username, $dbPassword, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if the form was submitted
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['reg_account'])){

    $nickname_email = $_POST['nickname_email'];
    $password = $_POST['password'];
 
    if (strpos($nickname_email, '@') !== false) {
        // if e-mail
        $sql = "SELECT password FROM accounts WHERE email = '$nickname_email'";
        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
            $row = $result->fetch_assoc();
            if ($row["password"] == $password) {
                $sql_id = "SELECT id FROM accounts WHERE email = '$nickname_email'";
                $result_id = $conn->query($sql_id);
                if ($result_id->num_rows > 0) {
                    $row_id = $result_id->fetch_assoc();
                    $id_user = $row_id["id"];
                    header("Location: connect.php?id_user=$id_user");
                    exit();
                }
            }
            else {
                echo $eror_text;
            }
        }
    } else {
        $sql = "SELECT password FROM accounts WHERE nickname = '$nickname_email'";
        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
            $row = $result->fetch_assoc();
            if ($row["password"] == $password) {
                $sql_id = "SELECT id FROM accounts WHERE nickname = '$nickname_email'";
                $result_id = $conn->query($sql_id);
                if ($result_id->num_rows > 0) {
                    $row_id = $result_id->fetch_assoc();
                    $id_user = $row_id["id"];
                    header("Location: connect.php?id_user=$id_user");
                    exit();
                }
            }
            else {
                echo $eror_text;
            }
        }
    }
}
?>
