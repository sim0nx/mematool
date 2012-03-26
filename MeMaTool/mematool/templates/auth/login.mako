<%inherit file="/base.mako" />

<!-- content !-->
<div id="content" class="span-9 push-6 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${_('Login')}</header>
        
<article>
  <h3>Mematool Login</h3>
  ${parent.flash()}
  ${h.form(url(controller='auth', action='doLogin'), method='post', name='authform')}
      <div>${h.text('username', tabindex='1', placeholder=_('syn2cat username'), class_='text', required=True)}</div>
  <div>${h.password('password', tabindex='2', placeholder=_('password'), class_='text', required=True)}</div> 
  <div>${h.submit('submit', _('Login'), tabindex='3', class_='text')}</div>
  ${h.end_form()}
   <div class="clear">&nbsp;</div>
</article>


<script language="JavaScript">
  document.forms[0].username.focus()
</script>
