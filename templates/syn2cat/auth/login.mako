<%inherit file="/base.mako" />

<form class="form-horizontal" role="form" method="POST" action="/doLogin" name="authform">
  <div class="form-group">
    <label for="username" class="col-lg-2 control-label">${_('Username')}</label>
    <div class="col-lg-10">
      <input type="text" name="username" class="form-control" id="username" placeholder="username">
    </div>
  </div>
  <div class="form-group">
    <label for="password" class="col-lg-2 control-label">${_('Password')}</label>
    <div class="col-lg-10">
      <input type="password" name="password" class="form-control" id="password" placeholder="password">
    </div>
  </div>
  <div class="form-group">
    <div class="col-lg-offset-2 col-lg-10">
      <button type="submit" class="btn btn-default">${_('Sign in')}</button>
    </div>
  </div>
</form>

<script language="JavaScript">
  document.forms[0].username.focus()
</script>
