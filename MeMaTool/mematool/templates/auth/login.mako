<%inherit file="/base.mako" />

<!-- content !-->
<div id="content" class="span-9 push-6 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${_('Login')}</header>
				
<article>
	<h3>Mematool Login</h3>
	${h.form(url(controller='auth', action='doLogin'), method='post', name='authform')}
     	<div><input type="text" class="text" name="username" placeholder="${_('syn2cat username')}" required /></div> 
	<div><input type="password" class="text" name="password" placeholder="${_('password')}" required /></div> 
	${h.submit('send', _('Login'), class_='input text')}</td>
	</form> 
	 <div class="clear">&nbsp;</div>
</article>
