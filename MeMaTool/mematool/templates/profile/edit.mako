<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
	if 'reqparams' in s:
		if var in s['reqparams']:
			return s['reqparams'][var]

	if hasattr(c, 'member'):
		if var in vars(c.member):
			return vars(c.member)[var]

	if var is 'gidNumber':
		return 100
	elif var is 'loginShell':
		return '/bin/false'
	elif var is 'homeDirectory':
		return '/home/'

	return ''
%>

<form method="post" action="${url(controller='profile', action='doEdit')}" name="recordform">

			<div id="content" class="span-18 push-5 last ">
			<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
				
				<article>
					<table class="table_content" width="95%"> 

	${parent.flash()}
	% if 'errors' in session:
	% if len(session['errors']) > 0:


	<tr>
		<td>&nbsp;</td>
		<td>
			<div class="error">
			% for k in session['errors']:
			<font color="red">${k}</font><br>
			% endfor
			</div>
		</td>
	</tr>
		<%
		del session['errors']
		session.save()
		%>
	% else:
		<%
                del session['errors']
                session.save()
                %>
	% endif
	% endif
        <tr>
                <td class="table_title">
                        ${_('Username')}
                </td>
		<td>
			${c.member.uid}
		</td>
	</tr>
        <tr>
                <td class="table_title">
                        ${_('User ID')}
                </td>
                <td>
                        ${c.member.uidNumber}
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Additional groups')}
                </td>
                <td>
                        ${_('full member')} ${getFormVar(session, c, 'full_member')}
                        ${_('locked member')} ${getFormVar(session, c, 'locked_member')}
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Common name')}
                </td>
                <td>
                        ${getFormVar(session, c, 'cn')}
                </td>
	</tr>
	<tr>
                <td class="table_title">
                        ${_('Surname')}
                </td>
                <td>
                        <input type="text" name="sn" value="${getFormVar(session, c, 'sn')}" class="input" ${c.formDisabled}>
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Given name')}
                </td>
                <td>
                        <input type="text" name="gn" value="${getFormVar(session, c, 'gn')}" class="input" ${c.formDisabled}>
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Birth Date')} (YYYY-MM-DD)
                </td>
                <td>
                        <input type="text" name="birthDate" value="${getFormVar(session, c, 'birthDate')}" class="input" ${c.formDisabled}>
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Address')}
                </td>
                <td>
                        <textarea rows='10' cols='60' name="homePostalAddress" ${c.formDisabled}>${getFormVar(session, c, 'homePostalAddress')}</textarea>
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Phone')} (+xxx.yyyyyyyyy)
                </td>
                <td>
                        <input type="text" name="phone" value="${getFormVar(session, c, 'phone')}" class="input" ${c.formDisabled}>
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Mobile')} (+xxx.yyyyyyyyy)
                </td>
                <td>
                        <input type="text" name="mobile" value="${getFormVar(session, c, 'mobile')}" class="input" ${c.formDisabled}>
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('E-Mail')}
                </td>
                <td>
                        <input type="text" name="mail" value="${getFormVar(session, c, 'mail')}" class="input" ${c.formDisabled}>
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Login Shell')}
                </td>
                <td>
                        ${getFormVar(session, c, 'loginShell')}
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Home directory')}
                </td>
                <td>
                        ${getFormVar(session, c, 'homeDirectory')}
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Member since')} (YYYY-MM-DD)
                </td>
                <td>
                        ${getFormVar(session, c, 'arrivalDate')}
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('SSH Public Key')}
                </td>
                <td>
                        <textarea rows='10' cols='60' disabled name="sshPublicKey">${getFormVar(session, c, 'sshPublicKey')}</textarea>
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Password')} (min 8, only ASCII chars)
                </td>
                <td>
                        <input type="password" name="userPassword" value="" class="input" ${c.formDisabled}>
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Repeat Password')} (min 8)
                </td>
                <td>
                        <input type="password" name="userPassword2" value="" class="input" ${c.formDisabled}>
                </td>
        </tr>
</table>
<input type="submit" name="" value="Submit" class="input button right" ${c.formDisabled}>
</form>
</article>
<div id="make-space" class="prepend-top">&nbsp;</div>
</div>

<%
if 'reqparams' in session:
	del session['reqparams']
	session.save()
%>
