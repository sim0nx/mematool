<%inherit file="/base.mako" />

<h3>${c.heading}</h3>

<%include file="/pendingMemberValidations.mako" />
<table class="table table-striped">
  ${parent.flash()}
  <thead>
  <tr>
    <th>${_('Domain')}</th>
    <th>${_('Tools')}</th>
  </tr>
  </thead>
  <tbody>
  %for d in c.domains:
  <tr class="table_row">
    <td>${d.dc}</td>
    <td>${h.link_to(_('Aliases'),url(controller='mails', action='listAliases', domain=d.dc))}</td>
    <td>${h.link_to(_('Delete'),url(controller='mails', action='deleteDomain', domain=d.dc), onclick='return confirm(\'' + _('Are you _really_ sure you want to delete') + ' "' + d.dc + '"?\')')}</td>
  </tr>
  %endfor
  </tbody>
</table>
