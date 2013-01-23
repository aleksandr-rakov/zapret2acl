<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <title>zapret-info.gov converter</title>
    <meta name="author" content="doggy">
  </head>
  <body>
    <div>
      <form accept-charset="utf-8" enctype="multipart/form-data" method="POST" action="${request.route_url('form')}">
        <p>
          <input type="file" name='file'>
        </p>
        <p>
          <input type="submit" value="Upoad file">
        </p>
        <p>
          <label><input type="text" name='cisco'>Cisco ip</label>
        </p>
        <p>
          <label><input type="text" name='acl'>Acl</label>
        </p>
        <p>
          <label><input type="text" name='user'>User</label>
        </p>
        <p>
          <label><input type="text" name='pass'>Password</label>
        </p>
      </form>
    </div>
    %if status:
    <pre>
        ${status}
    </pre>
    %endif
  </body>
</html>
