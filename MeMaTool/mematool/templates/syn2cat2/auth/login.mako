<%inherit file="/base.mako" />

<h3>${c.heading}</h3>
        
${parent.flash()}
${h.form(url(controller='auth', action='doLogin'), method='post', name='authform')}
<div>${h.text('username', tabindex='1', placeholder=_('syn2cat username'), required=True)}</div>
<div>${h.password('password', tabindex='2', placeholder=_('password'), required=True)}</div> 
<button type="submit" class="btn" tabindex='3'>${_('Login')}</button>
${h.end_form()}


<script language="JavaScript">
  document.forms[0].username.focus()
</script>
