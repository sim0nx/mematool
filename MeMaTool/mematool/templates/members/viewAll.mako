<%inherit file="/base.mako" />

<div id="content" class="span-19 push-1 last ">
	<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
		<article>
			<li><table class="table_content"> 
			        <tr> 
			                <th class="table_title">
			                        ${_('Username')}
			                </th>
			                <th class="table_title">
			                        ${_('Surname')}
			                </th>
			                <th class="table_title">
			                        ${_('Given name')}
			                </th>
			                <th class="table_title">
			                        ${_('Home directory')}
			                </th>
			                <th class="table_title">
			                        ${_('Mobile')}
			                </th>
					<th class="table_title">
						${_('PEAP')}
					</th>
					<th class="table_title">
						${_('SSH')}
					</th>
					<th colspan="3" class="table_title">
						${_('Tools')}
					</th>
				</tr> 

<%
	x = 0
%>
% for m in c.members:
	<%
			x += 1
			peapPossible = h.literal('<img src="/images/icons/notok.png">') if not m.sambaNTPassword else h.literal('<img src="/images/icons/ok.png">')
			sshPublicKey = h.literal('<img src="/images/icons/notok.png">') if not m.sshPublicKey else h.literal('<img src="/images/icons/ok.png">')
	%>
	<tr class="table_row"> 
		<td>${m.uid}</td>
	        <td>${m.sn}</td>
	        <td>${m.gn}</td>
		<td>${m.homeDirectory}</td>
		<td>${m.mobile}</td>
		<td>${peapPossible}</td>
		<td>${sshPublicKey}</td>
		<td><a href="${url(controller='members', action='editMember', member_id=m.uid)}"><img src="/images/icons/pencil.png"></a></td>
		<td><a href="${url(controller='payments', action='listPayments', member_id=m.uid)}"><img src="/images/icons/payment.png"></a></td>
		% if m.validate == True:
		<td><a href="${url(controller='members', action='validateMember', member_id=m.uid)}">validate</a></td>
		<td><a href="${url(controller='members', action='rejectValidation', member_id=m.uid)}">reject-validaton</a></td>
		% endif
        </tr>
% endfor

</table>


<ul class="list-horizontal right">
	<li><a href="/mematool/members/list=10" class="regular button">10</a></li>
	<li><a href="/mematool/members/list=25" class="regular button">25</a></li>
	<li><a href="/mematool/members/list=50" class="regular button">50</a></li>
	<li><a href="/mematool/members/list=75" class="regular button">75</a></li>
	<li><a href="/mematool/members/list=100" class="regular button">100</a></li>
</ul>
<div class="clear">&nbsp;</div>
</article>
</div>
