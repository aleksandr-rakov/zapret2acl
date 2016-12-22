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
      <h3>Load file to white_list</h3>
      <form accept-charset="utf-8" enctype="multipart/form-data" method="POST" action="${request.route_url('white_list')}">
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

    %if white_list_load_error:
      Ошибка парсинга white_list
    %endif
    current white list:
    <pre>${'\n'.join(white_list)}</pre>
  </body>
</html>
