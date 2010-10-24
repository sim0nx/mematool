<%inherit file="/base.mako" />

<%def name="menu()">
## Then add our page links
<p>
  <a href="${h.url_for(controller='page', action='list', id=None)}">Some additional link</a>
</p>
## Include the parent footer too
${parent.menu()}
</%def>

<table class="table_content" width="95%">
        <tr>
                <td class="table_title">
        </tr>
</table>
