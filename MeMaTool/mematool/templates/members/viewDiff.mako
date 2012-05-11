<%inherit file="/base.mako" />

<div id="content" class="span-18 push-1 last ">
<header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
<article>

<table class="table_content" width="95%">
  <tr>
    <td>
      Old data
    </td>
    <td>
      New data
    </td>
  </tr>
</table>

<table class="table_content" width="95%">
  <tr>
    <td>
      <table class="table_content" width="95%">
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
            ${_('Birth Date')} (YYYY-MM-DD)
          </td>
          <td>
            ${c.member.birthDate}
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
      <table class="table_content" width="95%">
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
            ${_('Birth Date')} (YYYY-MM-DD)
          </td>
          <td>
            ${c.tmpmember.birthDate}
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
    </td>
  </tr>
</table>

<p>
  <a href="${url(controller='members', action='validateMember', member_id=c.member.uid)}">validate</a></br>
  <a href="${url(controller='members', action='rejectValidation', member_id=c.member.uid)}">reject-validaton</a>
</p>

</article>
<div id="make-space" class="prepend-top">&nbsp;</div>
</div>
