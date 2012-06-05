<%inherit file="/base.mako" />

<div id="content" class="span-19 push-1 last ">
  <header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
  <article>
    <%include file="/pendingMemberValidations.mako" />
    <li><table class="table_content">
      ${parent.flash()}
      <tr>
        <th class="table_title">${_('Group')}</th>
        <th class="table_title">${_('Tools')}</th>
      </tr>
      %for g in c.groups:
      <tr class="table_row">
        <td>${g.gid}</td>
        <td>${h.link_to(_('Edit'),url(controller='groups', action='editGroup', gid=g.gid))}</td>
        <td>${h.link_to(_('Un-manage'),url(controller='groups', action='unmanageGroup', gid=g.gid))}</td>
        <td>${h.link_to(_('Delete'),url(controller='groups', action='deleteGroup', gid=g.gid), onclick='return confirm(\'' + _('Are you sure you want to delete') + ' "' + g.gid + '"?\')')}</td>
      </tr>
      %endfor
    </table>
    <div class="clear">&nbsp;</div>
  </article>
</div>
