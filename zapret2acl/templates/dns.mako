<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <title>zapret-info.gov converter</title>
    <meta name="author" content="doggy">
  </head>
  <body>
    <div>
      Load file to DNS
      <form accept-charset="utf-8" enctype="multipart/form-data" method="POST" action="${request.route_url('dns')}">
        <p>
          <input type="file" name='file'>
        </p>
        <p>
          <input type="submit" value="Upoad file">
        </p>
      </form>
    </div>
    %if status:
      Статус
      <pre>
          ${status}
      </pre>
    %endif
    %if error:
      Ошибка
      <pre>
          ${error}
      </pre>
    %endif
  </body>
</html>
