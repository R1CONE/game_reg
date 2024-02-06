<?php
$servername = "localhost";
$username = "root";
$dbPassword = "";
$database = "recjump_data_baze";

$conn = new mysqli($servername, $username, $dbPassword, $database);

if ($conn->connect_error) {
    die("Błąd połączenia: " . $conn->connect_error);
}

?>

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
        font-size: 30px;
    }

    button {
        padding: 15px 30px;
        font-size: 24px;
        margin-bottom: 10px;
    }
</style>
</head>
<body>

<div class="registration-container">
    <form method="post">
        <div class="input-group">
            <input type="text" name="nickname" placeholder="Nick-name">
        </div>
        <div class="input-group">
            <input type="email" name="email" placeholder="E-mail">
        </div>
        <div class="input-group">
            <input type="password" name="password" placeholder="Password">
        </div>
        <button type="submit">Reg account</button>
        <button type="create_ac">I have account</button>
    </form>
</div>

</body>
</html>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") && isset($_POST['submit']) {
    
        // Получаем данные из формы и удаляем лишние пробелы
        $nickname = trim($_POST["nickname"]);
        $email = trim($_POST["email"]);
        $password = trim($_POST["password"]);

        $sql = "INSERT INTO accounts (nickname, email, password) VALUES ('$nickname', '$email', '$password')";

        echo "Вы успешно зарегистрировались с ником: $nickname, email: $email, и паролем: $password";
    } else {
        // Если не все поля были заполнены, выводим сообщение об ошибке
        echo "Пожалуйста, заполните все поля формы.";
    }
}
?>
