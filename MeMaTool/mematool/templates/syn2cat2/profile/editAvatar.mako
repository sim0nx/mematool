<%inherit file="/base.mako" />

<h3>${c.heading}</h3>

${h.form(url(controller='profile', action='doEditAvatar'), name='recordform', method='post', multipart=True)}
    <table class="table">
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
        <td>
          <img src="${c.member.avatarUrl}" alt="${_('user profile image')}">
        </td>
        <td>
          ${h.link_to(_('delete avatar'),url(controller='profile', action='doDeleteAvatar'))}
        </td>
      </tr>
      <tr>
        <td>
          ${_('Avatar:')}
        </td>
        <td>
          ${h.file(name='avatar')}
        </td>
      </tr>
      <tr>
        <td></td>
        <td><button type="submit" class="btn">${_('Submit')}</button></td>
    </table>
  ${h.end_form()}
