<%inherit file="/base.mako" />

<%def name="menu()">
## Include the parent footer too
${parent.menu()}
## Then add our page links
<p>
  <a href="${url(controller='page', action='list', id=None)}">Some additional link</a>
</p>
</%def>

<table class="table_content" width="95%">
        <tr>
                <td class="table_title">
        </tr>
</table>
