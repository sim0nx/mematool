<%inherit file="/base.mako" />

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
    <td><a href="/mails/listAliases/?domain=${d.dc}">${_('Aliases')}</a></td>
    <td><a href="/mails/deleteDomain/?domain=${d.dc}" onclick="return confirm('${_('Are you _really_ sure you want to delete {0}'.format(d.dc))}?')">${_('Delete')}</a></td>
  </tr>
  %endfor
  </tbody>
</table>
