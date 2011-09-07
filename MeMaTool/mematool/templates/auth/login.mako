<%inherit file="/base.mako" />

<!-- content !-->
<div id="content" class="span-9 push-6 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${_('Login')}</header>
				
<article>
	<h3>Mematool Login</h3>
	${h.form(url(controller='auth', action='doLogin'), method='post', name='authform')}
     	<div><input type="text" class="text" name="username" tabindex=1 placeholder="${_('syn2cat username')}" required /></div> 
	<div><input type="password" class="text" name="password" tabindex=2 placeholder="${_('password')}" required /></div> 
	<div><input type="submit" class="text" name="submit" tabindex=3 value="${_('Login')}" /></div>
	</form> 
	 <div class="clear">&nbsp;</div>
</article>


<script language="JavaScript">
	document.forms[0].username.focus()
</script>
