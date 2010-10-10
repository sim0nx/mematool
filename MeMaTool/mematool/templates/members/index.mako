<%inherit file="/base.mako" />

% for member in c.members:
	Member: ${member.dtusername}, uid: ${member.idmember} <br>
% endfor
