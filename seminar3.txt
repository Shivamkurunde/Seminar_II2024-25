<!DOCTYPE html>
<html>
<head>
    <title>Sort Student Records</title>
</head>
<body>
    <h2>Sort Students by Name</h2>
    <form method="get">
        <label for="order">Select Order:</label>
        <select name="order" id="order">
            <option value="ASC" <?= (isset($_GET['order']) && $_GET['order'] == 'ASC') ? 'selected' : '' ?>>Ascending</option>
            <option value="DESC" <?= (isset($_GET['order']) && $_GET['order'] == 'DESC') ? 'selected' : '' ?>>Descending</option>
        </select>
        <input type="submit" value="Sort">
    </form>

    <?php
    // Database connection
    $conn = new mysqli("localhost", "root", "", "studentdb");
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Default order is ASC if not set
    $order = isset($_GET['order']) && in_array($_GET['order'], ['ASC', 'DESC']) ? $_GET['order'] : 'ASC';

    // SQL query with order
    $sql = "SELECT * FROM students ORDER BY name $order";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        echo "<h3>Student Records (Sorted $order)</h3>";
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
        echo "No records found.";
    }

    $conn->close();
    ?>
</body>
</html>