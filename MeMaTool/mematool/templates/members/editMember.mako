<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
	if 'reqparams' in s:
		if var in s['reqparams']:
			return s['reqparams'][var]

	if var in vars(c.member):
		return vars(c.member)[var]
%>

<form method="post" action="${url(controller='members', action='doEditMember')}" name="recordform">

<table class="table_content" width="95%%">
	% if 'errors' in session:
	% if len(session['errors']) > 0:
	<tr>
		<td>&nbsp;</td>
		<td>
		% for k in session['errors']:
		<font color="red">${k}</font><br>
		% endfor
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
			${c.member.dtusername}
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
                        ${_('Group ID')}
                </td>
                <td>
                        <input type="text" name="gidNumber" value="${getFormVar(session, c, 'gidNumber')}" class="input">
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Common name')}
                </td>
                <td>
                        <input type="text" name="cn" value="${getFormVar(session, c, 'cn')}" class="input">
                </td>
	</tr>
	<tr>
                <td class="table_title">
                        ${_('Surname')}
                </td>
                <td>
                        <input type="text" name="sn" value="${getFormVar(session, c, 'sn')}" class="input">
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Given name')}
                </td>
                <td>
                        <input type="text" name="gn" value="${getFormVar(session, c, 'gn')}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Birth Date')} (YYYY-MM-DD)
                </td>
                <td>
                        <input type="text" name="birthDate" value="${getFormVar(session, c, 'birthDate')}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Address')}
                </td>
                <td>
                        <input type="text" name="address" value="${getFormVar(session, c, 'address')}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Phone')} (+xxx.yyyyyyyyy)
                </td>
                <td>
                        <input type="text" name="phone" value="${getFormVar(session, c, 'phone')}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Mobile')} (+xxx.yyyyyyyyy)
                </td>
                <td>
                        <input type="text" name="mobile" value="${getFormVar(session, c, 'mobile')}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('E-Mail')}
                </td>
                <td>
                        <input type="text" name="mail" value="${getFormVar(session, c, 'mail')}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Login Shell')}
                </td>
                <td>
                        <input type="text" name="loginShell" value="${getFormVar(session, c, 'loginShell')}" class="input">
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Home directory')}
                </td>
                <td>
                        <input type="text" name="homeDirectory" value="${getFormVar(session, c, 'homeDirectory')}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Member since')} (YYYY-MM-DD)
                </td>
                <td>
                        <input type="text" name="arrivalDate" value="${getFormVar(session, c, 'arrivalDate')}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Membership canceled')} (YYYY-MM-DD)
                </td>
                <td>
                        <input type="text" name="leavingDate" value="${getFormVar(session, c, 'leavingDate')}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('SSH Public Key')}
                </td>
                <td>
                        <textarea rows='10' cols='60' name="sshPublicKey">${getFormVar(session, c, 'sshPublicKey')}</textarea>
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Password')} (min 8)
                </td>
                <td>
                        <input type="password" name="userPassword" value="" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Repeat Password')} (min 8)
                </td>
                <td>
                        <input type="password" name="userPassword2" value="" class="input">
                </td>
        </tr>
	<tr>
		<td>
			&nbsp;
		</td>
                <td>
                        <input type="submit" name="" value="Submit" class="input">
                </td>
        </tr>
</table>


<input type="hidden" name="member_id" value="${c.member.idmember}">
</form>

<%
if 'reqparams' in session:
	del session['reqparams']
	session.save()
%>
