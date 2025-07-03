// 假设 $new_password 是用户提供的新密码

if ($result->num_rows > 0) {
    // 用户信息匹配，允许修改密码
    $hash_password = password_hash($new_password, PASSWORD_DEFAULT); // 加密新密码
    
    // 更新用户的密码
    $update_query = "UPDATE user_info SET password = ?, hash_password = ? WHERE phone_number = ?";
    $update_stmt = $conn->prepare($update_query);
    $update_stmt->bind_param("sss", $new_password, $hash_password, $phone_number); // 注意这里的顺序与SQL语句中的占位符对应
    
    if ($update_stmt->execute()) {
        $response = ['success' => true, 'message' => "Password updated successfully"];
        // 设置cookie或者其他必要的会话信息
        setcookie('username', $name, time() + 3600, '/');
        setcookie('token', $hash_password, time() + 3600, '/');
        setcookie('user_id', $phone_number, time() + 3600, '/');
        setcookie('paper_search', '', time() + 3600, '/');
        
        // 返回成功响应
        echo json_encode($response);
    } else {
        // 如果更新失败
        $response = ['success' => false, 'message' => "Failed to update password: " . $update_stmt->error];
        echo json_encode($response);
    }
}