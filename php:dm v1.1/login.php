<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>用户登录 -- 生物医药循证分析平台V3.5.1</title>
    <style>
        body {
            background-color: #f0f8ff; /* 背景颜色：淡绿 */
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh; /* 视口高度 */
            margin: 0;
            font-family: Arial, sans-serif;
        }

        .main_body {
            width: 1000px;
            max-width: 1000px;
            background-color: #f0f8ff; /* 主体颜色：浅绿 */
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 3px solid #4CAF50;

        }

        h2 {
            color: #006400; /* 标题颜色：深绿 */
        }

        label {
            display: block;
            margin-bottom: 5px;
            color: #333;
        }

        input[type="text"], input[type="password"] {
            width: 98%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 3px;
            background-color: #fff;
        }


        input[type="submit"] {
            background-color: #008000; /* 按钮颜色：绿 */
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 3px;
        }

        input[type="submit"]:hover {
            background-color: #006400; /* 鼠标悬停颜色：深绿 */
        }

        .error {
            color: red; /* 错误信息颜色：红 */
        }
        .form-group {
            text-align: right;
        }
        form{

        }
        a{
            color: #3e8e41;
            text-decoration: none;
        }
    </style>
</head>
<body>
<div class="main_body">
    <h2>
        用户登录
    </h2>
    <form action="login.php" method="post">
        <label for="phone_number">手机号:</label><br>
        <input type="text" id="phone_number" name="phone_number"><br>
        <label for="password">密码:</label><br>
        <input type="password" id="password" name="password"><br>
        <div class="form-group">
            <a href="register.php">没有账号？立即注册！</a>
            <input type="submit" value="登录">
        </div>
    </form>

    <?php
    // 检查表单是否已提交
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // 连接数据库的配置
        $servername = "localhost";
        $db_username = "root";
        $db_password = "root1234";
        $dbname = "web8";

        try {
            // 创建PDO实例
            $conn = new PDO("mysql:host=$servername;dbname=$dbname", $db_username, $db_password);
            // 设置PDO错误模式为异常
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

            // 准备SQL语句
            $stmt = $conn->prepare("SELECT * FROM `user_info` WHERE phone_number = :phone_number");

            // 绑定参数
            $stmt->bindParam(':phone_number', $_POST['phone_number']);
            $stmt->execute();

            // 获取查询结果
            $result = $stmt->fetch(PDO::FETCH_ASSOC);

            // 验证密码
            if ($result && password_verify($_POST['password'], $result['hash_password'])) {
                // 密码正确
                setcookie('username', $result['name'], time()+3600, '/'); // "/" 表示根目录下有效
                $hash_password = password_hash($_POST['password'], PASSWORD_DEFAULT); // 加密密码
                setcookie('token', $hash_password, time()+3600, '/'); // "/" 表示根目录下有效
                setcookie('user_id', $_POST['phone_number'], time()+3600, '/'); // "/" 表示根目录下有效
                setcookie('paper_search', $result['papersearch'], time()+3600, '/'); // "/" 表示根目录下有效

                header('Location: index.php'); // 登录成功后重定向到dashboard页面
                exit();
            } else {
                setcookie('username', '', time()+3600, '/'); // "/" 表示根目录下有效
                setcookie('token', '', time()+3600, '/'); // "/" 表示根目录下有效
                setcookie('user_id', '', time()+3600, '/'); // "/" 表示根目录下有效
                setcookie('paper_search', '', time()+3600, '/'); // "/" 表示根目录下有效
                // 密码错误
                echo '<p class="error">用户名或密码错误.</p>';
            }
        } catch (PDOException $e) {
            setcookie('username', '', time()+3600, '/'); // "/" 表示根目录下有效
            setcookie('token', '', time()+3600, '/'); // "/" 表示根目录下有效
            setcookie('user_id', '', time()+3600, '/'); // "/" 表示根目录下有效
            setcookie('paper_search', '', time()+3600, '/'); // "/" 表示根目录下有效
            echo "Connection failed: " . $e->getMessage();
        }
    }

    ?>
    <p>微信：yfxaybz</p>
    <p>网站备案号：<a href="https://beian.miit.gov.cn/" target="_blank">ICP备2022011369号-2</a></p>
</div>


</body>
</html>