% if hasattr(c, 'members') and len(c.members) > 0:
  % for m in c.members:
${m.uid};${m.sn};${m.givenName};${m.mail};${m.pgpKey}
  % endfor
% endif
