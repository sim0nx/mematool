"SIRNAME";"GIVENNAME";"NATIONALITY";"HOMEPOSTALADDRESS"
% if hasattr(c, 'members') and len(c.members) > 0:
  % for m in c.members:
<%
  if not m.npoMember:
    continue
  m.homePostalAddress = m.homePostalAddress.replace('\n', '@@@@').replace('\r', '')
%>"${m.sn}";"${m.givenName}";"${m.nationality}";"${m.homePostalAddress}"
  % endfor
% endif
