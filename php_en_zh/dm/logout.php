<?php
setcookie('username', '', time()+3600, '/'); // "/" 表示根目录下有效
setcookie('token', '', time()+3600, '/'); // "/" 表示根目录下有效
setcookie('user_id', '', time()+3600, '/'); // "/" 表示根目录下有效
setcookie('paper_search', '', time()+3600, '/'); // "/" 表示根目录下有效
header('Location: login.php'); // 登录成功后重定向到dashboard页面

