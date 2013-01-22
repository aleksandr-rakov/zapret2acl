<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <title>zapret-info.gov converter</title>
    <meta name="author" content="doggy">
  </head>
  <body>
    %if status:
    <div>
        ${status}
    </div>
    %endif
    <div>
      <form accept-charset="utf-8" enctype="multipart/form-data" method="POST" action="${request.route_url('form')}">
        <input type="file" name='file'>
        <input type="submit" value="Upoad file">
      </form>
    </div>
  </body>
</html>
