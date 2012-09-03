<%inherit file="/base.mako" />

<div id="content" class="span-19 push-1 last ">
  <header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
  <article>
    <li><table class="table_content">
      ${parent.flash()}
      <tr>
        <th class="table_title">${_('Alias')}</th>
        <th class="table_title">${_('Destination')}</th>
        <th class="table_title">${_('Tools')}</th>
      </tr>
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
    </table>
    <div class="clear">&nbsp;</div>
  </article>
</div>
