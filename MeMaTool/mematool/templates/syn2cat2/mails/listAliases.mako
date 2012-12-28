<%inherit file="/base.mako" />

<h3>${c.heading}</h3>

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
    <td>${h.link_to(_('Edit'),url(controller='mails', action='editAlias', alias=a.dn_mail))}</td>
    <td>${h.link_to(_('Delete'),url(controller='mails', action='deleteAlias', alias=a.dn_mail), onclick='return confirm(\'' + _('Are you _really_ sure you want to delete') + ' "' + a.dn_mail + '"?\')')}</td>
  </tr>
  %endfor
  </tbody>
</table>
