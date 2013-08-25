<%inherit file="/base.mako" />

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
    <td><a href="/groups/editGroup/?gid=${g.gid}">${_('Edit')}</a></td>
    <td><a href="/groups/unmanageGroup/?gid=${g.gid}">${_('Un-manage')}</a></td>
    <td><a href="/groups/deleteGroup/?gid=${g.gid}" onclick="return confirm('${_('Are you sure you want to delete {0}'.format(g.gid))}?')">${_('Delete')}</a></td>
  </tr>
  %endfor
  </tbody>
</table>
