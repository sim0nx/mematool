<%inherit file="/base.mako" />

<form method="post" action="${url(controller='members', action='doEditMember')}" name="recordform">

<table class="table_content" width="95%">
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
                        <input type="text" name="gidNumber" value="${c.member.gidNumber}" class="input">
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Common name')}
                </td>
                <td>
                        <input type="text" name="cn" value="${c.member.cn}" class="input">
                </td>
	</tr>
	<tr>
                <td class="table_title">
                        ${_('Surname')}
                </td>
                <td>
                        <input type="text" name="sn" value="${c.member.sn}" class="input">
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Given name')}
                </td>
                <td>
                        <input type="text" name="gn" value="${c.member.gn}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Birth Date')}
                </td>
                <td>
                        <input type="text" name="birthDate" value="${c.member.birthDate}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Address')}
                </td>
                <td>
                        <input type="text" name="address" value="${c.member.address}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Phone')}
                </td>
                <td>
                        <input type="text" name="phone" value="${c.member.phone}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Mobile')}
                </td>
                <td>
                        <input type="text" name="mobile" value="${c.member.mobile}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('E-Mail')}
                </td>
                <td>
                        <input type="text" name="mail" value="${c.member.mail}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Login Shell')}
                </td>
                <td>
                        <input type="text" name="loginShell" value="${c.member.loginShell}" class="input">
                </td>
        </tr>
	<tr>
                <td class="table_title">
                        ${_('Home directory')}
                </td>
                <td>
                        <input type="text" name="homeDirectory" value="${c.member.homeDirectory}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Member since')}
                </td>
                <td>
                        <input type="text" name="arrivalDate" value="${c.member.arrivalDate}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Membership canceled')}
                </td>
                <td>
                        <input type="text" name="leavingDate" value="${c.member.leavingDate}" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Password')}
                </td>
                <td>
                        <input type="password" name="userPassword" value="********" class="input">
                </td>
        </tr>
        <tr>
                <td class="table_title">
                        ${_('Repeat Password')}
                </td>
                <td>
                        <input type="password" name="userPassword2" value="********" class="input">
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


<input type="hidden" name="member_id" value="${c.member.dtusername}">
</form>
