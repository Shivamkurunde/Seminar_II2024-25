<?php
$host = "localhost";
$user = "root";
$password = ""; // use your actual MySQL password
$db = "studentdb";

// Connect to database
$conn = new mysqli($host, $user, $password, $db);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if (isset($_GET['query'])) {
    $search = $conn->real_escape_string($_GET['query']);

    $sql = "SELECT * FROM students WHERE name LIKE '%$search%'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        echo "<table border='1' cellpadding='5'>
                <tr><th>ID</th><th>Name</th><th>Email</th><th>Course</th></tr>";
        while ($row = $result->fetch_assoc()) {
            echo "<tr>
                    <td>{$row['id']}</td>
                    <td>{$row['name']}</td>
                    <td>{$row['email']}</td>
                    <td>{$row['course']}</td>
                  </tr>";
        }
        echo "</table>";
    } else {
        echo "No student found.";
    }
}

$conn->close();
?>