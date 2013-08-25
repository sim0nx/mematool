<%inherit file="/base.mako" />

<div id="content" class="col-md-18 push-1 last ">
<article>

<div class="alert alert-info">
${_('The user has submitted the following change request.')}<br>
${_('On the left is his old data and on the right the updated one.')}
</div>

<div class="alert alert-warning">
${_('Please carefully review the changes and accept only valid data.')}
</div>

<table class="table_content" width="95%">
  <tr>
    <td>
      <table class="table_content" width="95%">
        <tr>
          <td class="table_title">
            <b>Old data</b>
          </td>
          <td>
            &nbsp;
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('Username')}
          </td>
          <td>
            ${c.member.uid}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('User ID')}
          </td>
          <td>
            ${c.member.uidNumber}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('Surname')}
          </td>
          <td>
            ${c.member.sn}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('Given name')}
          </td>
          <td>
            ${c.member.givenName}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('Address')}
          </td>
          <td>
            ${c.member.homePostalAddress}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('Phone')} (+xxx.yyyyyyyyy)
          </td>
          <td>
            ${c.member.homePhone}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('Mobile')} (+xxx.yyyyyyyyy)
          </td>
          <td>
            ${c.member.mobile}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('E-Mail')}
          </td>
          <td>
            ${c.member.mail}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('XMPP/Jabber/GTalk ID')}
          </td>
          <td>
            ${c.member.xmppID}
          </td>
        </tr>
      </table>
    </td>
    <td>
      <div class="notice">
      <table class="table_content" width="95%">
        <tr>
          <td class="table_title">
            <b>New data</b>
          </td>
          <td>
            &nbsp;
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('Username')}
          </td>
          <td>
            ${c.member.uid}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('User ID')}
          </td>
          <td>
            ${c.member.uidNumber}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('Surname')}
          </td>
          <td>
            ${c.tmpmember.sn}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('Given name')}
          </td>
          <td>
            ${c.tmpmember.gn}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('Address')}
          </td>
          <td>
            ${c.tmpmember.homePostalAddress}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('Phone')} (+xxx.yyyyyyyyy)
          </td>
          <td>
            ${c.tmpmember.phone}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('Mobile')} (+xxx.yyyyyyyyy)
          </td>
          <td>
            ${c.tmpmember.mobile}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('E-Mail')}
          </td>
          <td>
            ${c.tmpmember.mail}
          </td>
        </tr>
        <tr>
          <td class="table_title">
            ${_('XMPP/Jabber/GTalk ID')}
          </td>
          <td>
            ${c.tmpmember.xmppID}
          </td>
        </tr>
      </table>
</div>
    </td>
  </tr>
</table>

</br>
<p>
  <a href="/members/validateMember/?member_id=${c.member.uid}" class="btn btn-success">${_('validate')}</a>
  <a href="/members/rejectValidation/?member_id=${c.member.uid}" class="btn btn-danger">${_('reject validaton')}</a>
</p>

</article>
<div id="make-space" class="prepend-top">&nbsp;</div>
</div>
