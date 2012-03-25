<%inherit file="/base.mako" />

<div id="content" class="span-19 push-1 last ">
	<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
	<article>
		<li><table class="table_content">
			${parent.flash()}
			<tr>
				<th class="table_title">${_('Domain')}</th>
				<th class="table_title">${_('Tools')}</th>
			</tr>
			%for d in c.domains:
			<tr class="table_row">
				<td>${d.dc}</td>
				<td>${h.link_to(_('Aliases'),url(controller='mails', action='listAliases', domain=d.dc))}</td>
				<td>${h.link_to(_('Delete'),url(controller='mails', action='deleteDomain', domain=d.dc), onclick='return confirm(\'' + _('Are you _really_ sure you want to delete') + ' "' + d.dc + '"?\')')}</td>
			</tr>
			%endfor
		</table>
		<div class="clear">&nbsp;</div>
	</article>
</div>
