<?php include 'visit.php'; ?>
<?php
// 检查是否设置了username和token cookies
if (isset($_COOKIE['username']) && isset($_COOKIE['token']) && isset($_COOKIE['user_id']) &&
    !empty($_COOKIE['username']) && !empty($_COOKIE['token']) && !empty($_COOKIE['user_id'])) {

    $login_text = $_COOKIE['username'];
    if (isset($_GET['message'])) {
        $message = $_GET['message'];
        $file = $_GET['file'];
    }

} else {
    $login_text = '登录';
    echo $_COOKIE['username'];
    header('Location: login.php'); // 登录成功后重定向到index页面
}


?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EasyTCM Data Mining System</title>
    <style>
        /* Global Styles */
        body {
            background-color: #f0f8ff;
            color: #333;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }

        /* Table Styles */
        #myTable {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        #myTable th, #myTable td {
            border: 1px solid #4CAF50;
            padding: 10px;
            text-align: left;
        }

        #myTable th {
            background-color: #4CAF50;
            color: white;
        }

        /* Input and Textarea Styles */
        .editable, textarea {
            width: calc(100% - 12px); /* Adjusted for padding */
            padding: 5px;
            border: none;
            border-radius: 4px;
            background-color: #f0f8ff;
        }

        textarea {
            height: 200px;
            border: 1px solid #4CAF50;
        }

        /* Button Styles */
        button, #submit_button, input[type='file'] {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
        }

        button:hover, #submit_button:hover, input[type='file']:hover {
            background-color: #3e8e41;
        }

        input[type='file'] {
            width: 850px;
        }

        /* Other Styles */
        .bottom_blank_div, #ref {
            height: 120px;

        }

        .main_body {
            width: 1000px;
            max-width: 1000px;
        }

        a {
            color: #3e8e41;
            text-decoration: none;
        }

        #loginForm {
            margin-top: 20px;
        }

        h2 {
            text-align: center;
            color: darkgreen;
        }

        .file_a {
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
        }

        #phone_label, #phone {
            visibility: hidden;
        }

        .button_container, .button_container2 {
            display: flex;
            justify-content: space-between;
        }

        .button_container2 {
            justify-content: flex-end;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #ddd;
        }
    </style>
</head>
<body>

<div class="main_body">

    <div class="button_container2">
        <form id="loginForm">
            <a id="login_a" href="login.php"><?php echo $login_text ?></a>
            <a id="login_out" href="logout.php"><?php echo 'logout' ?></a>

        </form>
    </div>
    <h2>EasyTCM Data Mining System</h2>
        <h3>Upload</h3>
    <form action="upload.php" method="post" enctype="multipart/form-data">

        <div class="button_container">
            <div class="file-input-container">
                <label for="file"></label>
                <input type="file" name="file" id="file" required>
            </div>
            <input id="submit_button" type="submit" value="upload">
        </div>
        <div class="button_container">
            <a class="file_a" href="数据挖掘模板.xlsx" download>template.xlsx</a>
        </div>
        <label for="phone" id="phone_label">Phone:</label>
        <input type="tel" name="phone" id="phone" value="<?php echo $_COOKIE['user_id'] ?>"><br>

    </form>

    <div>
        <?php
        if (isset($_COOKIE['username']) && isset($_COOKIE['token']) && isset($_COOKIE['user_id']) &&
            !empty($_COOKIE['username']) && !empty($_COOKIE['token']) && !empty($_COOKIE['user_id'])) {
            // 数据库配置信息
            $host = 'localhost'; // 数据库服务器地址
            $dbname = 'web8'; // 数据库名
            $username = 'root'; // 数据库用户名
            $password = 'root1234'; // 数据库密码

            // 创建数据库连接
            $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

            /**
             * 根据电话号码查询数据并输出为HTML表格
             * @param string $phoneNumber 电话号码
             */
            function queryAndOutputAsTable($phoneNumber) {
                global $pdo;

                // 准备SQL语句
                $sql = "SELECT original_filename, upload_time, status, url FROM dataminer_upload_records WHERE phone = :phone";

                // 执行查询
                $stmt = $pdo->prepare($sql);
                $stmt->execute([':phone' => $phoneNumber]);
                $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

                echo '<h3>Tasks</h3>';

                // 输出HTML表格
                echo '<table>';
                echo '<tr><th>Src File</th><th>Upload Time</th><th>status</th><th>download</th></tr>';
                foreach ($results as $row) {
                    echo '<tr>';
                    echo '<td>' . htmlspecialchars($row['original_filename']) . '</td>';
                    echo '<td>' . htmlspecialchars($row['upload_time']) . '</td>';
                    echo '<td>' . htmlspecialchars($row['status']) . '</td>';
                    echo '<td>' . htmlspecialchars($row['url']) . '</td>';
                    echo '</tr>';
                }
                echo '</table>';
            }

            // 调用函数，假设电话号码是1234567890
            queryAndOutputAsTable($_COOKIE['user_id']);

        } else {
            $login_text = '登录';
            echo $_COOKIE['username'];
            header('Location: login.php'); // 登录成功后重定向到index页面
        }


        ?>
    </div>



        <br>
        <br>        <br>
        <br>        <br>
        <br>        <br>        <br>
        <br>        <br>        <br>        <br>
        <br>
    <div>
        <br>
        <br>
        <h3>引用本站</h3>
        <textarea id="ref">[1]李海燕,周崇云,王一帆.生物医药循证分析平台V3.5.1［DB/OL］.（2024-06-01）［<?php echo date('Y-m-d'); ?>］. http://zytzbsy.com/dataminer/index.php
[2]周崇云,李盼飞,王一帆,等.中医药数据挖掘处理系统的设计与实现[J].中国数字医学,2025,In Presss.
            </textarea>
        <div class="button_container2">
            <button id="copy_button_ref">引用</button>
        </div>
    </div>

    <div class="bottom_blank_div"></div>
    <div class="container">
        <h3>网站信息</h3>
        <p>微信：yfxaybz</p>
        <p>中国中医科学院中医药信息研究所 ©版权所有2025-</p>
    </div>
    <div class="bottom_blank_div"></div>


</div>
</body>
</html>