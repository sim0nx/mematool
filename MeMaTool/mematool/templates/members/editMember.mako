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

<form method="post" action="${url(controller='members', action='doEditMember')}" name="recordform">

<div id="content" class="span-18 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
<article>
<table class="table_content">
	${parent.all_messages()}
        <tr>
                <td class="table_title">
                        ${_('Username')}
                </td>
		<td>
			% if c.mode is 'add':
			<input type="text" name="member_id" value="${getFormVar(session, c, 'member_id')}" class="input text">
			% else:
			${c.member.uid}
			% endif
		</td>
	</tr>
	% if c.mode is 'edit':
        <tr>
                <td class="table_title">
                        ${_('User ID')}
                </td>
                <td>
                        ${c.member.uidNumber}
                </td>
        </tr>
	% endif
        <tr>
                <td class="table_title">
                        ${_('Additional groups')}
                </td>
                <td>
                        ${_('full member')} <input type="checkbox" name="full_member" ${getFormVar(session, c, 'full_member')} class="input text">
                        ${_('locked member')} <input type="checkbox" name="locked_member" ${getFormVar(session, c, 'locked_member')} class="input text">
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Common name')}
                </td>
                <td>
                        <input type="text" name="cn" value="${getFormVar(session, c, 'cn')}" class="input text">
                </td>
	</tr>
	<tr>
                <td class="table_title">
                        ${_('Surname')}
                </td>
                <td>
                        <input type="text" name="sn" value="${getFormVar(session, c, 'sn')}" class="input text">
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Given name')}
                </td>
                <td>
                        <input type="text" name="givenName" value="${getFormVar(session, c, 'givenName')}" class="input text">
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Convention signer')}
                </td>
                <td>
                        <input type="text" name="conventionSigner" value="${getFormVar(session, c, 'conventionSigner')}" class="input text">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Birth Date')} (YYYY-MM-DD)
                </td>
                <td>
                        <input type="text" name="birthDate" value="${getFormVar(session, c, 'birthDate')}" class="input text">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Address')}
                </td>
                <td>
                        <textarea rows='10' cols='60' name="homePostalAddress">${getFormVar(session, c, 'homePostalAddress')}</textarea>
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Phone')} (+xxx.yyyyyyyyy)
                </td>
                <td>
                        <input type="text" name="homePhone" value="${getFormVar(session, c, 'homePhone')}" class="input text">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Mobile')} (+xxx.yyyyyyyyy)
                </td>
                <td>
                        <input type="text" name="mobile" value="${getFormVar(session, c, 'mobile')}" class="input text">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('E-Mail')}
                </td>
                <td>
                        <input type="text" name="mail" value="${getFormVar(session, c, 'mail')}" class="input text">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('XMPP/Jabber/GTalk ID')}
                </td>
                <td>
                        <input type="text" name="xmppID" value="${getFormVar(session, c, 'xmppID')}" class="input text">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Login Shell')}
                </td>
                <td>
                        <input type="text" name="loginShell" value="${getFormVar(session, c, 'loginShell')}" class="input text">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Member since')} (YYYY-MM-DD)
                </td>
                <td>
                        <input type="text" name="arrivalDate" value="${getFormVar(session, c, 'arrivalDate')}" class="input text">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Membership canceled')} (YYYY-MM-DD)
                </td>
                <td>
                        <input type="text" name="leavingDate" value="${getFormVar(session, c, 'leavingDate')}" class="input text">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('PGP Key')}
                </td>
                <td>
                        <input type="text" name="pgpKey" value="${getFormVar(session, c, 'pgpKey')}" class="input text">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('iButton UID')}
                </td>
                <td>
                        <input type="text" name="iButtonUID" value="${getFormVar(session, c, 'iButtonUID')}" class="input text">
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
                        <input type="password" name="userPassword" value="" class="input text">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Repeat Password')} (min 8)
                </td>
                <td>
                        <input type="password" name="userPassword2" value="" class="input text">
                </td>
        </tr>
</table>

% if c.mode is 'edit':
<input type="hidden" name="member_id" value="${c.member.uid}">
% endif
<input type="hidden" name="mode" value="${c.mode}">
<input type="submit" name="" value="${_('Submit')}" class="input button right"> 

</form>
</article>
<div id="make-space" class="prepend-top">&nbsp;</div>
</div>

<%
if 'reqparams' in session:
	del session['reqparams']
	session.save()
%>
