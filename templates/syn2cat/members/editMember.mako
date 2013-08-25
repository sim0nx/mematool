<%inherit file="/base.mako" />

<%!
def getFormVar(s, c, var):
  if 'reqparams' in s:
    if var in s['reqparams']:
      return s['reqparams'][var]

  if hasattr(c, 'member'):
    return getattr(c.member, var)

  if var == 'loginShell':
    return '/bin/false'

  return ''
%>

<form method="post" action="/members/doEditMember" class="form-horizontal">
  ${parent.all_messages()}
  <div class="control-group">
    <label class="control-label">${_('Username')} ${_('(3-20chars, lowercase, alphanumeric only)')}</label>
    <div class="controls">
    % if c.mode == 'add':
    <input type="text" name="member_id" value="${getFormVar(session, c, 'member_id')}" class="form-control">
    % else:
    ${c.member.uid}
    % endif
    </div>
  </div>
  % if c.mode == 'edit':
  <div class="control-group">
    <label class="control-label">${_('User ID')}</label>
    <div class="controls">
    ${c.member.uidNumber}
    </div>
  </div>
  % endif
  <div class="control-group">
    <label class="control-label">${_('Additional groups')}</label>
    <div class="controls">
      <input type="checkbox" name="fullMember" value="1" ${'checked' if getFormVar(session, c, 'fullMember') else ''}>${_('full member')}<br>
      <input type="checkbox" name="lockedMember" value="1" ${'checked' if getFormVar(session, c, 'lockedMember') else ''}>${_('locked member')}<br><br>
      % if c.mode == 'edit':
      ${', '.join(c.member.groups)}
      % endif
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Surname')}</label>
    <div class="controls">
    <input type="text" name="sn" value="${getFormVar(session, c, 'sn')}" class="form-control">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Given name')}</label>
    <div class="controls">
    <input type="text" name="givenName" value="${getFormVar(session, c, 'givenName')}" class="form-control">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Nationality (2 char iso-code)')}</label>
    <div class="controls">
    <input type="text" name="nationality" value="${getFormVar(session, c, 'nationality')}" class="form-control">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Convention signer')}</label>
    <div class="controls">
    <input type="text" name="conventionSigner" value="${getFormVar(session, c, 'conventionSigner')}" class="form-control">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Is minor')}</label>
    <div class="controls">
    <input type="checkbox" name="isMinor" value="1" ${'checked' if getFormVar(session, c, 'isMinor') else ''}>
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Address')}</label>
    <div class="controls">
    <textarea name="homePostalAddress" rows="10" cols="60" class="form-control">${getFormVar(session, c, 'homePostalAddress')}</textarea>
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Phone')} (+xxx.yyyyyyyyy)</label>
    <div class="controls">
    <input type="text" name="homePhone" value="${getFormVar(session, c, 'homePhone')}" class="form-control">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Mobile')} (+xxx.yyyyyyyyy)</label>
    <div class="controls">
    <input type="text" name="mobile" value="${getFormVar(session, c, 'mobile')}" class="form-control">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('E-Mail')}</label>
    <div class="controls">
    <input type="text" name="mail" value="${getFormVar(session, c, 'mail')}" class="form-control">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('XMPP/Jabber/GTalk ID')}</label>
    <div class="controls">
    <input type="text" name="xmppID" value="${getFormVar(session, c, 'xmppID')}" class="form-control">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Login Shell')}</label>
    <div class="controls">
    <input type="text" name="loginShell" value="${getFormVar(session, c, 'loginShell')}" class="form-control">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Member since')} (YYYY-MM-DD)</label>
    <div class="controls">
    <input type="text" id="arrivalDate" name="arrivalDate" value="${getFormVar(session, c, 'arrivalDate')}" class="form-control">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Membership canceled')} (YYYY-MM-DD)</label>
    <div class="controls">
    <input type="text" id="leavingDate" name="leavingDate" value="${getFormVar(session, c, 'leavingDate')}" class="form-control">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('PGP Key')}</label>
    <div class="controls">
    <input type="text" name="pgpKey" value="${getFormVar(session, c, 'pgpKey')}" class="form-control">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('iButton UID')}</label>
    <div class="controls">
    <input type="text" name="iButtonUID" value="${getFormVar(session, c, 'iButtonUID')}" class="form-control" autocomplete="off">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Has space key')}</label>
    <div class="controls">
    <input type="checkbox" name="spaceKey" value="1" ${'checked' if getFormVar(session, c, 'spaceKey') else ''}>
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Export to RCSL')}</label>
    <div class="controls">
    <input type="checkbox" name="npoMember" value="1" ${'checked' if getFormVar(session, c, 'npoMember') else ''}>
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('SSH Public Key')}</label>
    <div class="controls">
    <textarea name="sshPublicKey" rows="10" cols="60" class="form-control">${getFormVar(session, c, 'sshPublicKey')}</textarea>
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Password')} (min 8)</label>
    <div class="controls">
    <input type="password" name="userPassword" value="" class="form-control" autocomplete="off">
    </div>
  </div>
  <div class="control-group">
    <label class="control-label">${_('Repeat Password')} (min 8)</label>
    <div class="controls">
    <input type="password" name="userPassword2" value="" class="form-control" autocomplete="off">
    </div>
  </div>

  <div class="control-group">
    <div class="controls">
      <button type="submit" class="btn btn-default">Submit</button>
    </div>
  </div>

% if c.mode == 'edit':
<input type="hidden" name="member_id" value="${c.member.uid}">
% endif
<input type="hidden" name="mode" value="${c.mode}">
</form>

<script type="text/javascript" src="/javascript/bootstrap-datepicker.js"></script>
<script>
$('#leavingDate').datepicker({format: "yyyy-mm-dd", autoclose: true});
$('#arrivalDate').datepicker({format: "yyyy-mm-dd", autoclose: true});
</script>

<%
if 'reqparams' in session:
  del session['reqparams']
  session.save()
%>
