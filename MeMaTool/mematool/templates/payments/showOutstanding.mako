<%inherit file="/base.mako" />

<%def name="actions()">
<p id="actions">
${h.form(url(controller='payments', action='editPayment'), method='post', name='addpayment')}
	${h.select('member_id', '1000', c.member_ids)}
	${h.submit('choose','Add payment')}
${h.end_form()}
</p>
</%def>

<table class="table_content" width="95%">
        <tr>
                <td class="table_title">
        </tr>
</table>
