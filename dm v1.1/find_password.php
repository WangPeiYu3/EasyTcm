<?php
// 语言切换逻辑
$current_lang = isset($_GET['lang']) ? $_GET['lang'] : (isset($_COOKIE['lang']) ? $_COOKIE['lang'] : 'en');
if (!in_array($current_lang, ['en', 'zh'])) $current_lang = 'en';
setcookie('lang', $current_lang, time()+3600*24*30, '/');
$lang = [
    'en' => [
        'title' => 'Evidence-based Analysis Platform V3.5.1 -- Change Password',
        'change_password' => 'Change Password',
        'phone' => 'Phone Number(*)',
        'name' => 'Name(*)',
        'university' => 'University',
        'new_password' => 'New Password(*)',
        'submit' => 'Change Password',
        'login' => 'Already have an account? Login now!',
        'placeholder_phone' => 'Please enter phone number',
        'placeholder_name' => 'Please enter name',
        'placeholder_university' => 'Please enter university',
        'placeholder_new_password' => 'Please enter new password (at least 8 characters, including letters and numbers)',
    ],
    'zh' => [
        'title' => '生物医学循证分析平台V3.5.1--修改密码',
        'change_password' => '修改密码',
        'phone' => '手机号(*)',
        'name' => '姓名(*)',
        'university' => '毕业院校',
        'new_password' => '新密码(*)',
        'submit' => '修改密码',
        'login' => '已有账号？立即登录！',
        'placeholder_phone' => '请输入手机号',
        'placeholder_name' => '请输入姓名',
        'placeholder_university' => '请输入毕业院校',
        'placeholder_new_password' => '请输入新密码 (至少8位，包含字母和数字)',
    ]
];
$t = $lang[$current_lang];
?>
<!DOCTYPE html>
<html lang="<?php echo $current_lang ?>">
<head>
    <meta charset="UTF-8">
    <title><?php echo $t['title']; ?></title>
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
    <div style="text-align:right;margin-bottom:10px;">
        <a href="?lang=en">English</a> | <a href="?lang=zh">中文</a>
    </div>
    <h2><?php echo $t['change_password']; ?></h2>
    <form id="change-password-form">
        <label for="phone_number"><?php echo $t['phone']; ?></label><br>
        <input type="tel" id="phone_number" name="phone_number" required placeholder="<?php echo $t['placeholder_phone']; ?>"><br>
        <label for="your_name"><?php echo $t['name']; ?></label><br>
        <input type="text" id="your_name" name="your_name" required placeholder="<?php echo $t['placeholder_name']; ?>"><br>
        <label for="university"><?php echo $t['university']; ?></label><br>
        <input type="text" id="university" name="university" placeholder="<?php echo $t['placeholder_university']; ?>"><br>
        <label for="new_password"><?php echo $t['new_password']; ?></label><br>
        <input type="password" id="new_password" name="new_password" required pattern="^(?=.*\d)(?=.*[a-zA-Z]).{8,}$" placeholder="<?php echo $t['placeholder_new_password']; ?>"><br>
        <div class="form-group">
            <input type="submit" value="<?php echo $t['submit']; ?>">
        </div>
    </form>
    <p id="response-message" class="error"></p>
    <a href="login.php"><?php echo $t['login']; ?></a>
</div>
</body>
</html>