<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
	if 'reqparams' in s:
		if var in s['reqparams']:
			return s['reqparams'][var]

	if var in vars(c.group):
		return vars(c.group)[var]
%>


${h.form(url(controller='groups', action='doEditGroup'), method='post', name='editGroupForm')}
<div id="content" class="span-19 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
<article>

<table class="table_content" width="95%">
	${parent.all_messages()}
        <tr>
                <td class="table_title"><label for="gid">${_('Group name:')}</label></td>
		<td>${h.text('gid', value=getFormVar(session, c, 'gid'), class_='input text')}</td>
        </tr>
	% if hasattr(c.group, 'gidNumber') and not c.group.gidNumber == None:
	<tr>
		<td class="table_title">
			${_('Group members')}
		</td>
		<td>
			<textarea rows='10' cols='60' name="users">${getFormVar(session, c, 'users')}</textarea>
		</td>
	</tr>
	% endif
	<tr>
		<td class="table_title"/>
		<td style="text-align:left;">
		<% 
			if not hasattr(c.group, 'gidNumber') or c.group.gidNumber == None:
				label = _('Add group')
			else:
				label = _('Edit group')
		%>
		${h.submit('send', label, class_='input text')}</td>
	</tr>
</table>
${h.end_form()}
