<!DOCTYPE html>
<html lang="zh">
<head>
    <title>生物医学循证分析平台V3.5.1--检索系统</title>
    <style>
        body {
            margin-top: 100px;
            background-color: #f0f8ff; /* 背景颜色：淡绿 */
            display: flex;
            justify-content: center;
            align-items: center;
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

        input[type="text"], input[type="password"], input[type="tel"], input[type="email"] {
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
    <h2>用户注册</h2>

    <form action="register.php" method="post">
        <label for="phone_number">手机号(*):</label><br>
        <input type="tel" id="phone_number" name="phone_number" required><br>

        <label for="your_name">姓名(*):</label><br>
        <input type="text" id="your_name" name="your_name" required><br>

        <label for="university">毕业院校:</label><br>
        <input type="text" id="university" name="university"><br>

        <label for="wechat">微信:</label><br>
        <input type="text" id="wechat" name="wechat"><br>

        <label for="company">工作单位:</label><br>
        <input type="text" id="company" name="company"><br>

        <label for="email">邮箱:</label><br>
        <input type="email" id="email" name="email"><br>
        <label for="qq">QQ:</label><br>
        <input type="text" id="qq" name="qq"><br>
        <label for="password">密码(*):</label><br>
        <input type="password" id="password" name="password" required pattern="^(?=.*\d)(?=.*[a-zA-Z]).{8,}$"><br>
        <label for="confirm_password">确认密码(*):</label><br>
        <input type="password" id="confirm_password" name="confirm_password" required pattern="^(?=.*\d)(?=.*[a-zA-Z]).{8,}$"><br>

        <div class="form-group">
            <a id="login_button_a" href="login.php">已有账号？立即登录！</a>
            <input type="submit" value="注册">
        </div>
    </form>

</div>
</body>
</html>