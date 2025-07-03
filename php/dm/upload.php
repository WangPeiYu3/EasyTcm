<?php
session_start();
$uploadFolder = 'D:/dataMiner/'; // 更新为绝对路径的文件上传目录

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
    die("数据库连接失败: " . $e->getMessage());
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
        header("Location: index.php?message=400&file={$fileHash}"); // 登录成功后重定向到index页面
        echo json_encode(array('error' => '计算文件MD5时出错'));
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
        $status = '处理中...';

        // 构建SQL插入语句
        $sql = "INSERT INTO dataminer_upload_records (original_filename, saved_filename, upload_time, phone, status) VALUES (?, ?, ?, ?, ?)";

        try {
            // 执行SQL插入
            $stmt = $pdo->prepare($sql);
            $stmt->execute([$originalFileName, $savedFileName, $uploadTime, $phone,$status]);

            // 返回JSON响应
            http_response_code(200);
            echo json_encode(array('message' => "文件已成功上传并重命名为 {$uniqueFileName}！数据已保存至数据库。"));
            header("Location: index.php?message=200&file={$uniqueFileName}"); // 登录成功后重定向到index页面

        } catch (PDOException $e) {
            http_response_code(500);
//            header("Location: index.php?message=500&file={$uniqueFileName}"); // 登录成功后重定向到index页面

            echo json_encode(array('error' => '数据库操作失败: ' . $e->getMessage()));
        }
    } else {
        http_response_code(400);
        header("Location: index.php?message=400&file={$uniqueFileName}"); // 登录成功后重定向到index页面
        echo json_encode(array('error' => '文件上传失败'));
    }
} else {
    // 如果不是POST请求或者文件未提交，显示上传表单
    include 'index.html';
}
?>