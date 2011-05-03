<%inherit file="/base.mako" />

% for member in c.members:
	Member: ${member.uid}, uid: ${member.uidNumber} <br>
% endfor
