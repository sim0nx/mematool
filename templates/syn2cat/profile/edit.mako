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

% if c.member.validate:
<div class="alert alert-warning">
  ${_('Your account is currently locked for validation')}
</div>
% endif

<form method="post" action="/profile/doEdit" name="recordform">
    <table class="table table-striped"> 
      ${parent.all_messages()}
      <tr>
        <td class="table_title">
          <a href="/profile/editAvatar"><img src="${c.member.avatarUrl}" alt="${_('user profile image')}"></a>
        </td>
        <td>
          &nbsp;
        </td>
      </tr>
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
          <%
            full_member = r'<img src="/images/icons/notok.png">' if not c.member.fullMember else r'<img src="/images/icons/ok.png">'
            locked_member = r'<img src="/images/icons/notok.png">' if not c.member.lockedMember else r'<img src="/images/icons/ok.png">'
            i = 0
            first = True
          %>
          ${_('full member')} ${full_member}
          ${_('locked member')} ${locked_member}
          % if len(c.groups) > 0:
          <br><br>
            % for g in c.groups:
              % if i == 4:
          <br>
                <% i = 0 %>
              % endif
              % if first:
              <% first = False %>
              % else:
          ,
              % endif
          ${g}
              <% i += 1 %>
            % endfor
          % endif
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
          <input type="text" name="sn" value="${getFormVar(session, c, 'sn')}" class="form-control" ${c.formDisabled}>
        </td>
      </tr>
      <tr>
        <td class="table_title">
          ${_('Given name')}
        </td>
        <td>
          <input type="text" name="givenName" value="${getFormVar(session, c, 'givenName')}" class="form-control" ${c.formDisabled}>
        </td>
      </tr>
      <tr>
        <td class="table_title">
          ${_('Convention signer')}
        </td>
        <td>
          ${getFormVar(session, c, 'conventionSigner')}
        </td>
      </tr>
      <tr>
        <td class="table_title">
          ${_('Address')}
        </td>
        <td>
          <textarea rows='10' cols='60' name="homePostalAddress" ${c.formDisabled} class="form-control">${getFormVar(session, c, 'homePostalAddress')}</textarea>
        </td>
      </tr>
      <tr>
        <td class="table_title">
          ${_('Phone')} (+xxx.yyyyyyyyy)
        </td>
        <td>
          <input type="text" name="homePhone" value="${getFormVar(session, c, 'homePhone')}" class="form-control" ${c.formDisabled}>
        </td>
      </tr>
      <tr>
        <td class="table_title">
          ${_('Mobile')} (+xxx.yyyyyyyyy)
        </td>
        <td>
          <input type="text" name="mobile" value="${getFormVar(session, c, 'mobile')}" class="form-control" ${c.formDisabled}>
        </td>
      </tr>
      <tr>
        <td class="table_title">
          ${_('E-Mail')}
        </td>
        <td>
          <input type="text" name="mail" value="${getFormVar(session, c, 'mail')}" class="form-control" ${c.formDisabled}>
        </td>
      </tr>
      <tr>
        <td class="table_title">
          ${_('XMPP/Jabber/GTalk ID')}
        </td>
        <td>
          <input type="text" name="xmppID" value="${getFormVar(session, c, 'xmppID')}" class="form-control" ${c.formDisabled}>
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
          ${_('PGP Key')}
        </td>
        <td>
          ${getFormVar(session, c, 'pgpKey')}
        </td>
      </tr>
      <tr>
        <td class="table_title">
          ${_('SSH Public Key')}
        </td>
        <td>
          <textarea rows='10' cols='60' disabled name="sshPublicKey" class="form-control">${getFormVar(session, c, 'sshPublicKey')}</textarea>
        </td>
      </tr>
      <tr>
        <td class="table_title">
          ${_('Password')} (min 8, ${_('only ASCII chars')})
        </td>
        <td>
          <input type="password" name="userPassword" value="" class="form-control" ${c.formDisabled}>
        </td>
      </tr>
      <tr>
        <td class="table_title">
          ${_('Repeat Password')} (min 8)
        </td>
        <td>
           <input type="password" name="userPassword2" value="" class="form-control" ${c.formDisabled}>
        </td>
      </tr>
      <tr>
        <td></td>
        <td><button type="submit" class="btn btn-default" ${c.formDisabled}>${_('Submit')}</button></td>
      </tr>
    </table>
  </form>

<%
if 'reqparams' in session:
  del session['reqparams']
  session.save()
%>
