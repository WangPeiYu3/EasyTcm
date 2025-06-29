<?php
header('Content-Type: application/json'); // 设置内容类型为JSON

// 数据库配置
$servername = "localhost";
$username = "root";
$password = "root1234";
$dbname = "web8";

$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    $response = array('success' => false, 'message' => "Connection failed: " . $conn->connect_error);
    setcookie('username', '', time()+3600, '/'); // "/" 表示根目录下有效
    setcookie('token', '', time()+3600, '/'); // "/" 表示根目录下有效
    setcookie('user_id', '', time()+3600, '/'); // "/" 表示根目录下有效
    setcookie('paper_search', '', time()+3600, '/'); // "/" 表示根目录下有效
    echo json_encode($response);
    exit;
}

// 接收POST数据
$phone_number = $_POST['phone_number'];
$register_time = date('Y-m-d H:i:s'); // 当前时间
$password = $_POST['password'];
$university = $_POST['university'];
$email = $_POST['email'];
$qq = $_POST['qq'];
$wechat = $_POST['wechat'];
$tags = $_POST['tags'];
$company = $_POST['company'];
$name = $_POST['your_name'];
$hash_password = password_hash($password, PASSWORD_DEFAULT); // 加密密码

// 创建预处理语句
$stmt = $conn->prepare("INSERT INTO user_info (phone_number, register_time, hash_password, university, email, qq, wechat, tags, company,password,name) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");

// 绑定参数
$stmt->bind_param("sssssssssss",  $phone_number, $register_time, $hash_password, $university, $email, $qq, $wechat, $tags, $company, $password,$name);

// 执行语句
if ($stmt->execute()) {
    $response = array('success' => true, 'message' => "New record created successfully");
    setcookie('username', $name, time()+3600, '/'); // "/" 表示根目录下有效
    setcookie('token', $hash_password, time()+3600, '/'); // "/" 表示根目录下有效
    setcookie('user_id', $phone_number, time()+3600, '/'); // "/" 表示根目录下有效
    setcookie('paper_search', '', time()+3600, '/'); // "/" 表示根目录下有效
    header('Location: index.php');

    exit;

} else {
    $response = array('success' => false, 'message' => "Error: " . $stmt->error);
    setcookie('username', '', time()+3600, '/'); // "/" 表示根目录下有效
    setcookie('token', '', time()+3600, '/'); // "/" 表示根目录下有效
    setcookie('user_id', '', time()+3600, '/'); // "/" 表示根目录下有效
    setcookie('paper_search', '', time()+3600, '/'); // "/" 表示根目录下有效
    header('Location: reg.php');
    exit;
}

echo json_encode($response); // 输出JSON响应

$stmt->close();
$conn->close();
?>