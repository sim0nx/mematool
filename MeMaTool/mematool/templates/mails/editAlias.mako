<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
	if 'reqparams' in s:
		if var in s['reqparams']:
			return s['reqparams'][var]

	if var in vars(c.alias):
		return vars(c.alias)[var]
%>


${h.form(url(controller='mail', action='doEditAlias'), method='post', name='editAliasForm')}
<div id="content" class="span-19 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
<article>

<table class="table_content" width="95%">
	${parent.all_messages()}
        <tr>
                <td class="table_title"><label for="alias">${_('Alias name:')}</label></td>
		<td>${h.text('alias', value=getFormVar(session, c, 'alias'), class_='text')}</td>
        </tr>
	% if hasattr(c.alias, 'mails') and not c.alias.mails == None:
	<tr>
		<td class="table_title">
			${_('Aliases')}
		</td>
		<td>
			${h.textarea('mail', content=getFormVar(session, c, 'mails'), rows='10', cols='60', class_='text')}
		</td>
	</tr>
	% endif
	<tr>
		<td class="table_title"/>
		<td style="text-align:left;">
		<% 
			if not hasattr(c, 'alias') or c.alias == None:
				label = _('Add alias')
			else:
				label = _('Edit alias')
		%>
		${h.submit('send', label, class_='text')}</td>
	</tr>
</table>
${h.end_form()}
