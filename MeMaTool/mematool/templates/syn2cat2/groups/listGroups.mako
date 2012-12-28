<%inherit file="/base.mako" />

<h3>${c.heading}</h3>
<%include file="/pendingMemberValidations.mako" />
<table class="table table-striped"> 
  ${parent.flash()}
  <thead>
  <tr>
    <th class="table_title">${_('Group')}</th>
    <th class="table_title">${_('Tools')}</th>
  </tr>
  </thead>
  <tbody>
  %for g in c.groups:
  <tr class="table_row">
    <td>${g.gid}</td>
    <td>${h.link_to(_('Edit'),url(controller='groups', action='editGroup', gid=g.gid))}</td>
    <td>${h.link_to(_('Un-manage'),url(controller='groups', action='unmanageGroup', gid=g.gid))}</td>
    <td>${h.link_to(_('Delete'),url(controller='groups', action='deleteGroup', gid=g.gid), onclick='return confirm(\'' + _('Are you sure you want to delete') + ' "' + g.gid + '"?\')')}</td>
  </tr>
  %endfor
  </tbody>
</table>
