<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>生物医学循证分析平台V3.5.1--修改密码</title>
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
            background-color: #fff; /* 主体颜色：白色 */
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 3px solid #4CAF50;
        }

        h2 {
            color: #006400; /* 标题颜色：深绿 */
            text-align: center;
        }

        label {
            display: block;
            margin-bottom: 5px;
            color: #333;
        }

        input[type="text"], input[type="password"], input[type="tel"] {
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
            float: right;
        }

        input[type="submit"]:hover {
            background-color: #006400; /* 鼠标悬停颜色：深绿 */
        }

        .error {
            color: red; /* 错误信息颜色：红 */
            text-align: center;
            margin-top: 10px;
        }
        .form-group {
            text-align: right;
        }
        a{
            color: #3e8e41;
            text-decoration: none;
            display: block;
            text-align: center;
            margin-top: 10px;
        }
    </style>
</head>
<body>

<div class="main_body">
    <h2>修改密码</h2>

    <form id="change-password-form">
        <label for="phone_number">手机号(*):</label><br>
        <input type="tel" id="phone_number" name="phone_number" required placeholder="请输入手机号"><br>

        <label for="your_name">姓名(*):</label><br>
        <input type="text" id="your_name" name="your_name" required placeholder="请输入姓名"><br>

        <label for="university">毕业院校:</label><br>
        <input type="text" id="university" name="university" placeholder="请输入毕业院校"><br>

        <label for="new_password">新密码(*):</label><br>
        <input type="password" id="new_password" name="new_password" required pattern="^(?=.*\d)(?=.*[a-zA-Z]).{8,}$" placeholder="请输入新密码 (至少8位，包含字母和数字)"><br>

        <div class="form-group">
            <input type="submit" value="修改密码">
        </div>
    </form>
    <p id="response-message" class="error"></p>
    <a href="login.php">已有账号？立即登录！</a>
</div>

</body>
</html>