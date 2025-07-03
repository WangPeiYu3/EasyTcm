<?php

// 数据库配置
$servername = "localhost";
$username = "root";
$password = "root1234";
$dbname = "web8";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// 获取用户agent和IP地址
$user_agent = $_SERVER['HTTP_USER_AGENT'];
$ip_address = $_SERVER['REMOTE_ADDR'];

// 准备SQL语句
$sql = "INSERT INTO visit_info (user_agent, ip_address) VALUES (?, ?)";

// 使用预处理语句防止SQL注入
$stmt = $conn->prepare($sql);
$stmt->bind_param("ss", $user_agent, $ip_address);

// 执行SQL语句
if ($stmt->execute()) {
    echo "";
} else {
    echo '<script type="text/javascript">alert("错误代码：E1!");</script>';

}

// 关闭连接
$stmt->close();
$conn->close();

