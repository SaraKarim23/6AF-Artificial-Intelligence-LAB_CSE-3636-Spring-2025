<?php
session_start();
include 'db.php';  // your DB connection

// Get JSON POST data
$data = json_decode(file_get_contents('php://input'), true);

if (!isset($_SESSION['email'])) {
    http_response_code(401);
    echo json_encode(['status' => 'error', 'message' => 'Not logged in']);
    exit;
}

$user_email = $_SESSION['email'];
$sender = $data['sender'] ?? '';
$message = $data['message'] ?? '';

if ($sender && $message) {
    $stmt = $conn->prepare("INSERT INTO chat_logs (user_email, sender, message) VALUES (?, ?, ?)");
    $stmt->bind_param("sss", $user_email, $sender, $message);
    $stmt->execute();
    if ($stmt->affected_rows > 0) {
        echo json_encode(['status' => 'success']);
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Insert failed']);
    }
    $stmt->close();
} else {
    echo json_encode(['status' => 'error', 'message' => 'Invalid data']);
}
?>
