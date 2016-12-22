<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <title>zapret-info.gov converter</title>
    <meta name="author" content="doggy">
  </head>
  <body>
    <div>
      <%include file="nav.mako"/>
      <h3>Load file to DNS</h3>
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
