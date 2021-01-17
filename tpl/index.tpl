<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Стена</title>
</head>
<body>
    <form action="/cgi-bin/Chat.py">
		<input type="hidden" name="action" value="Init">
        <input type="submit" value="Init To Server">
    </form>

    {posts}

    {publish}
	<br>
	{getdata}
	{delete}
</body>
</html>