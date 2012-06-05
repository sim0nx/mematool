% if 'pendingMemberValidations' in session and session['pendingMemberValidations'] > 0:
<div class="notice">
${_('There are pending validation requests regarding member profile updates.')}
</div>
% endif
