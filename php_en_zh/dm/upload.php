<?php
session_start();
$uploadFolder = 'D:/dataMiner/'; // 更新为绝对路径的文件上传目录

// 语言国际化
$lang = isset($_COOKIE['lang']) && $_COOKIE['lang'] === 'zh' ? 'zh' : 'en';
$msgs = [
    'zh' => [
        'upload_success' => "文件已成功上传并重命名为 %s！数据已保存至数据库。",
        'db_error' => "数据库操作失败: ",
        'upload_fail' => "文件上传失败",
        'md5_error' => "计算文件MD5时出错",
        'processing' => '处理中...'
    ],
    'en' => [
        'upload_success' => "File uploaded successfully and renamed to %s! Data saved to database.",
        'db_error' => "Database operation failed: ",
        'upload_fail' => "File upload failed",
        'md5_error' => "Error calculating file MD5",
        'processing' => 'Processing...'
    ]
];

// 数据库连接配置
$dbHost = 'localhost';
$dbName = 'web8';
$dbUser = 'root';
$dbPass = 'root1234';

try {
    // 创建PDO实例以连接数据库
    $pdo = new PDO("mysql:host=$dbHost;dbname=$dbName;charset=utf8", $dbUser, $dbPass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die($msgs[$lang]['db_error'] . $e->getMessage());
}

// 如果上传目录不存在，则创建它
if (!file_exists($uploadFolder)) {
    mkdir($uploadFolder, 0777, true);
}

// 检查是否是POST请求并且表单已提交
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $file = $_FILES['file'];

    // 计算文件的MD5值
    $fileHash = md5_file($file['tmp_name']);
    if ($fileHash === false) {
        http_response_code(400);
        header("Location: index.php?message=400&file={$fileHash}&lang=$lang");
        echo json_encode(array('error' => $msgs[$lang]['md5_error']));
        exit;
    }

    // 确保文件名唯一
    $uniqueTimestamp = microtime(true);
    $uniqueFileName = $fileHash . '_' . $uniqueTimestamp . '.xlsx';
    $filePath = $uploadFolder . $uniqueFileName;

    // 尝试移动上传的文件到指定的目录
    if (move_uploaded_file($file['tmp_name'], $filePath)) {
        // 准备插入数据库的数据
        $originalFileName = $file['name'];
        $savedFileName = $uniqueFileName;
        $uploadTime = date('Y-m-d H:i:s');
        $phone = isset($_POST['phone']) ? $_POST['phone'] : '';
        $status = $msgs[$lang]['processing'];

        // 构建SQL插入语句
        $sql = "INSERT INTO dataminer_upload_records (original_filename, saved_filename, upload_time, phone, status) VALUES (?, ?, ?, ?, ?)";

        try {
            // 执行SQL插入
            $stmt = $pdo->prepare($sql);
            $stmt->execute([$originalFileName, $savedFileName, $uploadTime, $phone, $status]);

            // 返回JSON响应
            http_response_code(200);
            echo json_encode(array('message' => sprintf($msgs[$lang]['upload_success'], $uniqueFileName)));
            header("Location: index.php?message=200&file={$uniqueFileName}&lang=$lang");

        } catch (PDOException $e) {
            http_response_code(500);
            echo json_encode(array('error' => $msgs[$lang]['db_error'] . $e->getMessage()));
        }
    } else {
        http_response_code(400);
        header("Location: index.php?message=400&file={$uniqueFileName}&lang=$lang");
        echo json_encode(array('error' => $msgs[$lang]['upload_fail']));
    }
} else {
    // 如果不是POST请求或者文件未提交，显示上传表单
    include 'index.html';
}
?>