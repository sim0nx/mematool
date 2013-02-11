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

${h.form(url(controller='members', action='doEditMember'), method='post', name='editMemberForm')}

<div id="content" class="span-18 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
<article>
<table class="table_content">
  ${parent.all_messages()}
  <tr>
    <td class="table_title">
      ${_('Username')} ${_('(3-20chars, lowercase, alphanumeric only)')}
    </td>
    <td>
    % if c.mode is 'add':
    ${h.text('member_id', value=getFormVar(session, c, 'member_id'), class_='text')}
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
      ${h.checkbox('full_member', value='1', checked=getFormVar(session, c, 'full_member'), class_='text')}${_('full member')}<br>
      ${h.checkbox('locked_member', value='1', checked=getFormVar(session, c, 'locked_member'), class_='text')}${_('locked member')}

        <%
          i = 0
          first = True
        %>
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
      ${h.text('sn', value=getFormVar(session, c, 'sn'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Given name')}
    </td>
    <td>
      ${h.text('givenName', value=getFormVar(session, c, 'givenName'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Nationality (2 char iso-code)')}
    </td>
    <td>
      ${h.text('nationality', value=getFormVar(session, c, 'nationality'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Convention signer')}
    </td>
    <td>
      ${h.text('conventionSigner', value=getFormVar(session, c, 'conventionSigner'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Is minor')} (YYYY-MM-DD)
    </td>
    <td>
      ${h.checkbox('isMinor', value='1', checked=getFormVar(session, c, 'isMinor'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Address')}
    </td>
    <td>
      ${h.textarea('homePostalAddress', content=getFormVar(session, c, 'homePostalAddress'), rows='10', cols='60', class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Phone')} (+xxx.yyyyyyyyy)
    </td>
    <td>
      ${h.text('homePhone', value=getFormVar(session, c, 'homePhone'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Mobile')} (+xxx.yyyyyyyyy)
    </td>
    <td>
      ${h.text('mobile', value=getFormVar(session, c, 'mobile'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('E-Mail')}
    </td>
    <td>
      ${h.text('mail', value=getFormVar(session, c, 'mail'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('XMPP/Jabber/GTalk ID')}
    </td>
    <td>
      ${h.text('xmppID', value=getFormVar(session, c, 'xmppID'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Login Shell')}
    </td>
    <td>
      ${h.text('loginShell', value=getFormVar(session, c, 'loginShell'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Member since')} (YYYY-MM-DD)
    </td>
    <td>
      ${h.text('arrivalDate', value=getFormVar(session, c, 'arrivalDate'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Membership canceled')} (YYYY-MM-DD)
    </td>
    <td>
      ${h.text('leavingDate', value=getFormVar(session, c, 'leavingDate'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('PGP Key')}
    </td>
    <td>
      ${h.text('pgpKey', value=getFormVar(session, c, 'pgpKey'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('iButton UID')}
    </td>
    <td>
      ${h.text('iButtonUID', value=getFormVar(session, c, 'iButtonUID'), class_='text', autocomplete='off')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Has space key')}
    </td>
    <td>
      ${h.checkbox('spaceKey', value='1', checked=getFormVar(session, c, 'spaceKey'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Is NPO member')}
    </td>
    <td>
      ${h.checkbox('npoMember', value='1', checked=getFormVar(session, c, 'npoMember'), class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('SSH Public Key')}
    </td>
    <td>
      ${h.textarea('sshPublicKey', content=getFormVar(session, c, 'sshPublicKey'), rows='10', cols='60', class_='text')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Password')} (min 8)
    </td>
    <td>
      ${h.password('userPassword', value='', class_='text', autocomplete='off')}
    </td>
  </tr>
  <tr>
    <td class="table_title">
      ${_('Repeat Password')} (min 8)
    </td>
    <td>
      ${h.password('userPassword2', value='', class_='text', autocomplete='off')}
    </td>
  </tr>
</table>

% if c.mode is 'edit':
${h.hidden('member_id', value=c.member.uid)}
% endif

${h.hidden('mode', value=c.mode)}
${h.submit('submit', _('Submit'), class_='input button right')}

${h.end_form()}
</article>
<div id="make-space" class="prepend-top">&nbsp;</div>
</div>

<%
if 'reqparams' in session:
  del session['reqparams']
  session.save()
%>
