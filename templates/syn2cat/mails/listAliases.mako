<%inherit file="/base.mako" />

<table class="table table-striped">
  ${parent.flash()}
  <thead>
  <tr>
    <th>${_('Alias')}</th>
    <th>${_('Destination')}</th>
    <th>${_('Tools')}</th>
  </tr>
  </thead>
  <tbody>
  %for a in c.aliases:
  <%
    maildrops = _('None')

    if len(a.maildrop) > 1:
      maildrops = str(len(a.maildrop)) + _(' Aliases')
    else:
      maildrops = a.maildrop[0]
  %>
  <tr class="table_row">
    <td>${a.dn_mail}</td>
    <td>${maildrops}</td>
    <td><a href="/mails/editAlias/?alias=${a.dn_mail}">${_('Edit')}</a></td>
    <td><a href="/mails/deleteAlias/?alias=${a.dn_mail}" onclick="return confirm('${_('Are you _really_ sure you want to delete {0}'.format(a.dn_mail))}?')">${_('Delete')}</a></td>
  </tr>
  %endfor
  </tbody>
</table>
