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
      <h3>Load file to cisco</h3>
      <form accept-charset="utf-8" enctype="multipart/form-data" method="POST" action="${request.route_url('home')}">
        <p>
          <input type="file" name='file'>
        </p>
        <p>
          <input type="submit" value="Upoad file">
        </p>
        % if show_params:
          <p>
            <label><input type="text" name='cisco'>Cisco ip <strong>*</strong></label>
          </p>
          <p>
            <label><input type="text" name='acl'>Acl <strong>*</strong></label>
          </p>
          <p>
            <label><input type="text" name='user'>User</label>
          </p>
          <p>
            <label><input type="text" name='pass'>Password</label>
          </p>
        % endif
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
