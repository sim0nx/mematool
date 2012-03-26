<%inherit file="/base.mako" />

<div id="content" class="span-19 push-1 last ">
  <header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
  <article>
    ${h.form(url(controller='payments', action='listPayments'), method='post')}
    <table class="table_content">
      <tr>
        <td class="table_title"><label for="year">${_('Year')}</label></td>
        <td>${h.text('year', value=c.year, class_='text')}</td>
      </tr>
    </table>
    <input type="hidden" name="member_id" value="${c.member_id}">
    ${h.end_form()}

    ${h.link_to(_('Bulk add multiple months'),url(controller='payments', action='bulkAdd', member_id=c.member_id))}

    <li><table class="table_content">
      ${parent.flash()}
      <tr>
        <th class="table_title">${_('Date')}</th>
        <th class="table_title">${_('Validated')}</th>
        <th class="table_title">${_('Status')}</th>
        <th class="table_title">${_('Tools')}</th>
      </tr>
      % for i in range(1, 13):
      <%
      p_id = None
      validated = 'no record'
      status = h.literal('<img src="/images/icons/notok.png">')

      if i in c.payments:
        p = c.payments[i]

        p_id = p.id
        validated = h.literal('<img src="/images/icons/notok.png">') if not p.verified else h.literal('<img src="/images/icons/ok.png">')

        if p.status == 0:
          status = h.literal('<img src="/images/icons/ok.png">')
        elif p.status == 2:
          status = '-'
      %>
      <tr class="table_row">
        <td>${str(c.year) + '-' + str(i)}</td>
        <td>${validated}</td>
        <td>${status}</td>
        % if not p_id is None:
          % if p.verified != 1 or (session.has_key('isFinanceAdmin') and session['isFinanceAdmin']):
          <td>${h.link_to(_('Modify'),url(controller='payments', action='editPayment', idPayment=p_id, member_id=c.member_id))}</td>
          % endif
          % if session.has_key('isFinanceAdmin') and session['isFinanceAdmin']:
          <td>${h.link_to(_('Validate'),url(controller='payments', action='validatePayment', idPayment=p_id, member_id=c.member_id))}</td>
          <td>${h.link_to(_('Delete'),url(controller='payments', action='deletePayment', idPayment=p_id, member_id=c.member_id))}</td>
          % endif
        % else:
        <td>${h.link_to(_('Add'),url(controller='payments', action='editPayment', year=c.year, month=i, member_id=c.member_id))}</td>
        % endif
      </tr>
      %endfor
    </table>
    <div class="clear">&nbsp;</div>
  </article>
</div>
