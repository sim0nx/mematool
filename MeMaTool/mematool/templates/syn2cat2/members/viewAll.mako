<%inherit file="/base.mako" />

<h3>${c.heading}</h3>
<%include file="/pendingMemberValidations.mako" />
<a href="${url(controller='members', action='exportList')}">${_('Export as CSV')}<img src="/images/icons/pencil.png"></a><br/>
<a href="${url(controller='members', action='exportList', listType='RCSL')}">${_('Export as RCSL CSV')}<img src="/images/icons/pencil.png"></a>
${parent.error_messages()}
<table class="table table-striped"> 
  ${parent.flash()}
  <thead>
    <tr> 
      <th>#</th>
      <th>${_('Username')}</th>
      <th>${_('Surname')}</th>
      <th>${_('Given name')}</th>
      <th>${_('E-Mail')}</th>
      <th>${_('SSH')}</th>
      <th>${_('Tools')}</th>
    </tr>
  </thead>
  <tbody>
  <% i = 0 %>
  % for m in c.members:
  <%
    sshPublicKey = h.literal('<img src="/images/icons/notok.png">') if not m.sshPublicKey else h.literal('<img src="/images/icons/ok.png">')
    uid = '<font color="green"><b>' + m.uid + '</b></font>' if m.fullMember else '<font color="#0479FF">' + m.uid + '</font>'
    i += 1
  %>
  <tr class="table_row"> 
    <td>${i}</td>
    <td><img src="${m.getGravatar()}" alt="${_('user profile image')}"> ${uid|n}</td>
    <td>${m.sn.decode('utf-8')}</td>
    <td>${m.gn.decode('utf-8')}</td>
    <td>${m.mail}</td>
    <td>${sshPublicKey}</td>
    <td><a href="${url(controller='members', action='editMember', member_id=m.uid)}"><img src="/images/icons/pencil.png"></a></td>
    <td><a href="${url(controller='payments', action='listPayments', member_id=m.uid)}"><img src="/images/icons/payment.png"></a></td>
    <td><a href="${url(controller='members', action='deleteUser', member_id=m.uid)}" onClick="return confirm('Are you sure you want to delete \'${m.uid}\'?')"><img src="/images/icons/notok.png"></a></td>
    % if m.validate:
    <td><a href="${url(controller='members', action='viewDiff', member_id=m.uid)}">validation</a></td>
    % endif
  </tr>
  % endfor
  </tbody>
</table>
