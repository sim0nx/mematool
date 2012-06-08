<%inherit file="/base.mako" />

${h.form(url(controller='profile', action='doEditAvatar'), name='recordform', method='post', multipart=True)}
  <div id="content" class="span-18 push-1 last ">
  <header style="background:#00ADEF; padding:5px; font-weight:bold; color:#fff;">${c.heading}</header>
  <article>
    <table class="table_content" width="95%">
      % if c.member.validate:
      <tr>
        <td colspan="2">
          <div class="notice">
            ${_('Your account is currently locked for validation')}
          </div>
        </td>
      </tr>
      % endif
      ${parent.all_messages()}
      <tr>
        <td class="table_title">
          <img src="${c.member.avatarUrl}" alt="${_('user profile image')}">
        </td>
        <td>
          &nbsp;
        </td>
      </tr>
      <tr>
        <td class="table_title">
          ${_('Avatar:')}
        </td>
        <td>
          ${h.file(name='avatar')}
        </td>
      </tr>
    </table>
    ${h.submit('submit', _('Submit'), class_='input button right')}
    ${h.link_to(_('delete avatar'),url(controller='profile', action='doDeleteAvatar'))}
  </article>
  ${h.end_form()}
<div id="make-space" class="prepend-top">&nbsp;</div>
</div>
