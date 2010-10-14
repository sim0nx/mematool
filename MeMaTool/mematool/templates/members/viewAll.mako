<%inherit file="/base.mako" />

<table class="table_content" width="95%">
        <tr>
                <td class="table_title">
                        ${_('Username')}
                </td>
                <td class="table_title">
                        ${_('Common name')}
                </td>
                <td class="table_title">
                        ${_('Surname')}
                </td>
                <td class="table_title">
                        ${_('Given name')}
                </td>
                <td class="table_title">
                        ${_('Home directory')}
                </td>
                <td class="table_title">
                        ${_('Mobile')}
                </td>
		<td>
			&nbsp;
		</td>
        </tr>


% for m in c.members:
	<tr>
		<td>${m.dtusername}</td>
                <td>${m.cn}</td>
	        <td>${m.sn}</td>
	        <td>${m.gn}</td>
		<td>${m.homeDirectory}</td>
		<td>${m.mobile}</td>
		<td><a href="${url(controller='members', action='editMember', member_id=m.dtusername)}">edit</a></td>
        </tr>
% endfor

</table>
